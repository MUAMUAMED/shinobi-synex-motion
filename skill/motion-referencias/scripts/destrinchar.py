#!/usr/bin/env python3
"""Destrincha um vídeo de referência de motion design, medindo TODOS os frames.

Uso: python destrinchar.py VIDEO --saida PASTA [--sem-mosaicos]

Gera em PASTA:
  frames.csv        uma linha por frame: mudança, brilho, saturação, nitidez, movimento, zoom, giro, etiquetas
  eventos.json      cortes, flashes, estrobos, implosões, impactos, chicotes, trechos parados
  cenas.json        cenas (entre cortes) com duração, paleta e movimento dominante
  resumo.md         números do ritmo e da cor, para decidir o estilo
  visao-geral.jpg   um quadro a cada 0,5 s com o tempo escrito
  eventos/*.jpg     quadro a quadro em volta dos 24 eventos mais fortes
  todos/*.jpg       todos os frames do vídeo, 1 s por folha (só com mosaicos)

Limites: as medidas são imagem pura. "Implosão" e "impacto" são inferidos do fluxo óptico,
então confira olhando as folhas de eventos antes de copiar valores.
"""
import argparse
import csv
import json
import math
import pathlib

import cv2
import numpy as np

W_AN, H_AN = 180, 320  # tamanho de análise; ajustado à proporção do vídeo


def paleta(img, k=4):
    px = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).reshape(-1, 3).astype(np.float32)
    px = px[:: max(1, len(px) // 4000)]
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    cv2.setRNGSeed(7)
    _, lab, cen = cv2.kmeans(px, k, None, crit, 2, cv2.KMEANS_PP_CENTERS)
    cont = np.bincount(lab.flatten(), minlength=k)
    ordem = np.argsort(-cont)
    return [("#%02x%02x%02x" % tuple(int(v) for v in cen[i]), round(float(cont[i]) / len(px), 3)) for i in ordem]


def medir(caminho):
    cap = cv2.VideoCapture(str(caminho))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    w0, h0 = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    if w0 >= h0:
        w, h = 320, max(2, int(320 * h0 / w0))
    else:
        w, h = max(2, int(320 * w0 / h0)), 320
    xs, ys = np.meshgrid(np.arange(w // 2) - w / 4, np.arange(h // 2) - h / 4)
    linhas, prev, prev_p, n = [], None, None, 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        p = cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA)
        g = cv2.cvtColor(p, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(p, cv2.COLOR_BGR2HSV)
        reg = {"f": n, "t": round(n / fps, 3), "brilho": float(g.mean()), "sat": float(hsv[..., 1].mean()),
               "nitidez": float(cv2.Laplacian(g, cv2.CV_32F).var()),
               "mud": 0.0, "pan_x": 0.0, "pan_y": 0.0, "zoom": 0.0, "giro": 0.0, "mov": 0.0}
        peq = cv2.resize(g, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
        if prev is not None:
            reg["mud"] = float(np.abs(p.astype(np.int16) - prev.astype(np.int16)).mean())
            fl = cv2.calcOpticalFlowFarneback(prev_p, peq, None, 0.5, 2, 13, 2, 5, 1.1, 0)
            u, v = fl[..., 0], fl[..., 1]
            r2 = float((xs * xs + ys * ys).sum())
            reg.update(pan_x=float(u.mean()) * 2, pan_y=float(v.mean()) * 2,
                       zoom=float(((u - u.mean()) * xs + (v - v.mean()) * ys).sum() / r2),
                       giro=float(((v - v.mean()) * xs - (u - u.mean()) * ys).sum() / r2),
                       mov=float(np.hypot(u, v).mean()) * 2)
        linhas.append(reg)
        prev, prev_p = p, peq
        n += 1
    cap.release()
    return {"fps": fps, "w": int(w0), "h": int(h0), "frames": linhas}


def achar_eventos(F, fps):
    mud = np.array([x["mud"] for x in F])
    bri = np.array([x["brilho"] for x in F])
    zoom = np.array([x["zoom"] for x in F])
    pan = np.array([math.hypot(x["pan_x"], x["pan_y"]) for x in F])
    nit = np.array([x["nitidez"] for x in F])
    mov = np.array([x["mov"] for x in F])
    n = len(F)
    ev = []
    base = np.median(mud) + 1e-6
    corte_lim = max(18.0, base * 6)
    cortes = [i for i in range(1, n) if mud[i] > corte_lim and mud[i] >= mud[max(0, i - 2):i + 3].max()]

    # Flashes: brilho salta e volta em poucos frames
    i = 1
    while i < n - 1:
        ja = bri[max(0, i - 3):i].min()
        if bri[i] - ja > 55 and bri[i] > 120:
            fim = i
            while fim < n - 1 and bri[fim + 1] > ja + 40 and fim - i < 15:
                fim += 1
            if fim - i <= 12:
                ev.append({"tipo": "flash", "de": i, "ate": fim, "forca": round(float(bri[i] - ja), 1)})
                i = fim
        i += 1

    # Estrobo: brilho oscila várias vezes em menos de 1 s
    d = np.diff(bri)
    i = 0
    while i < n - int(fps):
        jan = d[i:i + int(fps)]
        troca = int((np.sign(jan[:-1]) * np.sign(jan[1:]) < 0)[np.abs(jan[:-1]) > 12].sum())
        if troca >= 4:
            ev.append({"tipo": "estrobo", "de": i, "ate": i + int(fps), "forca": troca})
            i += int(fps)
        i += 1

    # Parte do preto
    escuro = bri < 8
    i = 0
    while i < n:
        if escuro[i]:
            j = i
            while j + 1 < n and escuro[j + 1]:
                j += 1
            if j - i >= 2:
                ev.append({"tipo": "preto", "de": i, "ate": j, "forca": j - i + 1})
            i = j
        i += 1

    z_lim = max(0.012, float(np.percentile(np.abs(zoom), 92)))
    for c in cortes:
        # Implosão: encolhe acelerando nos frames antes do corte
        ant = zoom[max(1, c - 6):c]
        if len(ant) >= 3 and ant.mean() < -z_lim * 0.7:
            ev.append({"tipo": "implosao", "de": max(1, c - 6), "ate": c, "forca": round(float(-ant.mean()), 4)})
        # Impacto: nasce grande e desfocado e assenta depois do corte
        dep = zoom[c + 1:c + 9]
        if len(dep) >= 3 and dep.mean() < -z_lim * 0.5 and nit[c + 1:c + 4].mean() < nit[c + 5:c + 12].mean() if len(nit[c + 5:c + 12]) else False:
            ev.append({"tipo": "impacto", "de": c, "ate": min(n - 1, c + 9), "forca": round(float(-dep.mean()), 4)})
        ev.append({"tipo": "corte", "de": c, "ate": c, "forca": round(float(mud[c]), 1)})

    # Chicote: movimento lateral forte em sequência
    pan_lim = max(6.0, float(np.percentile(pan, 96)))
    i = 1
    while i < n:
        if pan[i] > pan_lim:
            j = i
            while j + 1 < n and pan[j + 1] > pan_lim * 0.6:
                j += 1
            if j - i >= 2:
                ev.append({"tipo": "chicote", "de": i, "ate": j, "forca": round(float(pan[i:j + 1].max()), 1),
                           "dir": "horizontal" if abs(np.mean([F[k]["pan_x"] for k in range(i, j + 1)])) > abs(np.mean([F[k]["pan_y"] for k in range(i, j + 1)])) else "vertical"})
            i = j
        i += 1

    # Parado: sem mudança visível por pelo menos 1 s
    i = 0
    while i < n:
        if mud[i] < 0.6 and mov[i] < 0.25:
            j = i
            while j + 1 < n and mud[j + 1] < 0.6 and mov[j + 1] < 0.25:
                j += 1
            if j - i >= fps:
                ev.append({"tipo": "parado", "de": i, "ate": j, "forca": j - i + 1})
            i = j
        i += 1
    ev.sort(key=lambda e: (e["de"], e["tipo"]))
    for e in ev:
        e["t"] = round(e["de"] / fps, 2)
    return ev, cortes


def cenas(caminho, F, cortes, fps):
    lim = [0] + cortes + [len(F)]
    cap = cv2.VideoCapture(str(caminho))
    saida = []
    for a, b in zip(lim, lim[1:]):
        if b <= a:
            continue
        m = (a + b) // 2
        cap.set(cv2.CAP_PROP_POS_FRAMES, m)
        ok, fr = cap.read()
        trecho = F[a:b]
        zoom = float(np.mean([x["zoom"] for x in trecho]))
        px = float(np.mean([x["pan_x"] for x in trecho]))
        py = float(np.mean([x["pan_y"] for x in trecho]))
        mov = float(np.mean([x["mov"] for x in trecho]))
        nome = "parada"
        if mov > 0.3:
            nome = "aproxima" if zoom > 0.002 else "afasta" if zoom < -0.002 else ("lateral" if abs(px) > abs(py) else "vertical")
        saida.append({"de": a, "ate": b - 1, "t": round(a / fps, 2), "dur": round((b - a) / fps, 2), "movimento": nome,
                      "brilho": round(float(np.mean([x["brilho"] for x in trecho])), 1),
                      "paleta": paleta(cv2.resize(fr, (96, 96))) if ok else []})
    cap.release()
    return saida


def folha(cap, frames, cols, largura, destino, rotulo=None):
    img = []
    for f in frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, f)
        ok, fr = cap.read()
        if not ok:
            continue
        h = int(fr.shape[0] * largura / fr.shape[1])
        p = cv2.resize(fr, (largura, h), interpolation=cv2.INTER_AREA)
        tx = rotulo(f) if rotulo else str(f)
        cv2.putText(p, tx, (4, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(p, tx, (4, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
        img.append(p)
    if not img:
        return
    while len(img) % cols:
        img.append(np.zeros_like(img[0]))
    cv2.imwrite(str(destino), np.vstack([np.hstack(img[i:i + cols]) for i in range(0, len(img), cols)]), [cv2.IMWRITE_JPEG_QUALITY, 82])


def resumo(nome, dados, ev, cen):
    F, fps = dados["frames"], dados["fps"]
    cont = {}
    for e in ev:
        cont[e["tipo"]] = cont.get(e["tipo"], 0) + 1
    dur = len(F) / fps
    durs = [c["dur"] for c in cen]
    bri = np.array([x["brilho"] for x in F])
    mud = np.array([x["mud"] for x in F])
    energia = [round(float(mud[int(s * fps):int((s + 1) * fps)].mean()), 1) for s in range(int(dur))]
    cor = {}
    for c in cen:
        for hexa, p in c["paleta"]:
            cor[hexa] = cor.get(hexa, 0) + p * c["dur"]
    linhas = [f"# {nome}", "",
              f"- {dados['w']}x{dados['h']}, {fps:g} fps, {len(F)} frames medidos, {dur:.1f} s",
              f"- Família: {'clara' if bri.mean() > 110 else 'escura' if bri.mean() < 70 else 'mista'} (brilho médio {bri.mean():.0f} de 255)",
              f"- Cenas: {len(cen)}; duração mediana {np.median(durs):.2f} s; {60 * len(cen) / dur:.0f} cortes por minuto",
              f"- Eventos: " + ", ".join(f"{k} {v}" for k, v in sorted(cont.items())),
              f"- Tempo parado: {sum(e['ate'] - e['de'] + 1 for e in ev if e['tipo'] == 'parado') / fps:.1f} s",
              f"- Mudança média por segundo: {energia}",
              "", "## Cenas", "", "| Início (s) | Dura (s) | Movimento | Brilho | Cores |", "|---|---|---|---|---|"]
    for c in cen:
        linhas.append(f"| {c['t']} | {c['dur']} | {c['movimento']} | {c['brilho']} | {' '.join(h for h, _ in c['paleta'][:3])} |")
    return "\n".join(linhas) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--sem-mosaicos", action="store_true")
    a = ap.parse_args()
    v, s = pathlib.Path(a.video), pathlib.Path(a.saida)
    (s / "eventos").mkdir(parents=True, exist_ok=True)
    d = medir(v)
    F, fps = d["frames"], d["fps"]
    ev, cortes = achar_eventos(F, fps)
    cen = cenas(v, F, cortes, fps)
    with open(s / "frames.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(F[0].keys()))
        w.writeheader()
        for x in F:
            w.writerow({k: round(val, 4) if isinstance(val, float) else val for k, val in x.items()})
    (s / "eventos.json").write_text(json.dumps(ev, ensure_ascii=False, indent=0), encoding="utf-8")
    (s / "cenas.json").write_text(json.dumps(cen, ensure_ascii=False, indent=0), encoding="utf-8")
    (s / "resumo.md").write_text(resumo(v.stem, d, ev, cen), encoding="utf-8")
    cap = cv2.VideoCapture(str(v))
    n = len(F)
    folha(cap, list(range(0, n, max(1, int(fps / 2)))), 14, 130, s / "visao-geral.jpg", lambda f: f"{f / fps:.1f}s")
    # 24 eventos mais fortes, sem repetir o mesmo trecho: variedade de tipos primeiro
    pesos = {"implosao": 5, "impacto": 5, "estrobo": 4, "flash": 4, "chicote": 3, "preto": 2, "corte": 1}
    fortes, usados = [], []
    for e in sorted([e for e in ev if e["tipo"] in pesos], key=lambda e: (-pesos[e["tipo"]], -float(e["forca"]))):
        if all(abs(e["de"] - u) > fps for u in usados):
            fortes.append(e)
            usados.append(e["de"])
        if len(fortes) == 24:
            break
    for e in sorted(fortes, key=lambda e: e["de"]):
        a0 = max(0, e["de"] - 6)
        folha(cap, list(range(a0, min(n, a0 + 24))), 12, 120, s / "eventos" / f"{e['de']:05d}_{e['tipo']}.jpg", lambda f: f"{f}")
    if not a.sem_mosaicos:
        (s / "todos").mkdir(exist_ok=True)
        passo = int(round(fps))
        for i in range(0, n, passo):
            folha(cap, list(range(i, min(n, i + passo))), 15, 110, s / "todos" / f"{i // passo:03d}s.jpg", lambda f: f"{f}")
    cap.release()
    print(resumo(v.stem, d, ev, cen).split("## Cenas")[0])


if __name__ == "__main__":
    main()
