#!/usr/bin/env python3
"""Sugere o modelo de edição mais próximo a partir de um resumo.md do destrinchar.py.

Uso:
  python comparar.py PASTA_OU_RESUMO            mostra as referências mais parecidas
  python comparar.py --gerar PASTA_ANALISES     recria assets/referencias.json
  python comparar.py --testar                   confere cada referência contra as outras
"""
import json
import math
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parents[1] / "assets" / "referencias.json"
MODELOS = {"beaky": "Branco contínuo", "open-manager": "Branco contínuo", "zei": "Branco contínuo",
           "cendap": "Bloco de cor", "gespat": "Bloco de cor", "hakuna": "Neon escuro",
           "season-cloud": "Neon escuro", "voltz": "Imersivo de objetos"}
# Peso maior no que mais separa os modelos: claro ou escuro, e depois ritmo
PESOS = {"brilho": 2.0, "cortes_min": 1.0, "cena_mediana": 0.8, "pretos_min": 0.8, "chicotes_min": 0.3}
ESCALA = {"brilho": 100.0, "cortes_min": 15.0, "cena_mediana": 1.5, "pretos_min": 15.0, "chicotes_min": 6.0}


def ler(caminho):
    p = pathlib.Path(caminho)
    if p.is_dir():
        p = p / "resumo.md"
    t = p.read_text(encoding="utf-8")
    dur = float(re.search(r"frames medidos, ([\d.]+) s", t).group(1))
    ev = re.search(r"Eventos: (.*)", t).group(1)
    conta = lambda nome: int((re.search(nome + r" (\d+)", ev) or [0, 0])[1])
    return {"brilho": float(re.search(r"brilho médio (\d+)", t).group(1)),
            "cortes_min": float(re.search(r"(\d+) cortes por minuto", t).group(1)),
            "cena_mediana": float(re.search(r"duração mediana ([\d.]+) s", t).group(1)),
            "pretos_min": 60 * conta("preto") / dur, "chicotes_min": 60 * conta("chicote") / dur}


def dist(a, b):
    return math.sqrt(sum(PESOS[k] * ((a[k] - b[k]) / ESCALA[k]) ** 2 for k in PESOS))


def main():
    a = sys.argv[1:]
    if a[:1] == ["--gerar"]:
        ref = {d.name: dict(ler(d), modelo=MODELOS.get(d.name, "?")) for d in sorted(pathlib.Path(a[1]).iterdir()) if (d / "resumo.md").exists()}
        BASE.parent.mkdir(exist_ok=True)
        BASE.write_text(json.dumps(ref, ensure_ascii=False, indent=1), encoding="utf-8")
        print("salvo", BASE, len(ref))
        return
    ref = json.loads(BASE.read_text(encoding="utf-8"))
    if a[:1] == ["--testar"]:
        certos = 0
        for n, v in ref.items():
            viz = min((o for o in ref if o != n), key=lambda o: dist(v, ref[o]))
            ok = ref[viz]["modelo"] == v["modelo"]
            certos += ok
            print(f"{n:14} -> {viz:14} {ref[viz]['modelo']:20} {'ok' if ok else 'DIFERENTE (' + v['modelo'] + ')'}")
        print(f"{certos} de {len(ref)} no mesmo modelo")
        return
    v = ler(a[0])
    print({k: round(x, 2) for k, x in v.items()})
    for n in sorted(ref, key=lambda o: dist(v, ref[o]))[:3]:
        print(f"{n:14} {ref[n]['modelo']:20} distância {dist(v, ref[n]):.2f}")
    print("Confirme olhando a visao-geral.jpg: o número não vê a ideia.")


if __name__ == "__main__":
    main()
