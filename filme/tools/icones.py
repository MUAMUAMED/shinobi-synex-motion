"""Baixa ícones do game-icons.net (CC BY 3.0) e gera assets/icones.js com os desenhos sem o fundo preto."""
import json
import pathlib
import re
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PASTA = RAIZ / "assets" / "icones"
LISTA = {
    "shuriken": "darkzaitzev/shuriken", "shuriken2": "darkzaitzev/star-shuriken", "ninja": "darkzaitzev/ninja-head",
    "ninja_corre": "darkzaitzev/running-ninja", "ninja_pose": "darkzaitzev/ninja-heroic-stance", "mascara": "lorc/ninja-mask",
    "fumaca": "darkzaitzev/smoke-bomb", "katana": "delapouite/katana", "pergaminho": "lorc/scroll-unfurled",
    "pergaminho_pena": "delapouite/scroll-quill", "pergaminho_fechado": "lorc/tied-scroll", "pagode": "delapouite/pagoda",
    "bambu": "delapouite/bamboo", "aperto": "delapouite/shaking-hands", "anel": "delapouite/diamond-ring",
    "terceiro_olho": "lorc/third-eye", "raio": "lorc/lightning-branches", "espadas": "lorc/crossed-swords",
    "choque": "lorc/sword-clash", "forca": "lorc/muscle-up", "biceps": "delapouite/biceps", "trofeu": "lorc/trophy",
    "mapa": "lorc/treasure-map", "d20": "delapouite/dice-twenty-faces-twenty", "amanhecer": "lorc/sunrise",
    "lua": "lorc/moon", "noite": "lorc/night-sky", "bigorna": "lorc/anvil", "ampulheta": "lorc/hourglass",
    "identidade": "delapouite/id-card", "calendario": "delapouite/calendar", "meditacao": "lorc/meditation",
    "folha": "lorc/falling-leaf", "lanterna": "delapouite/asian-lantern", "oni": "delapouite/oni", "raposa": "lorc/fox-head",
    "portao": "delapouite/temple-gate", "bonsai": "delapouite/bonsai-tree", "coracao": "skoll/hearts",
    "balao": "skoll/talk", "erva": "delapouite/herbs-bundle", "cutelo": "delapouite/cleaver",
    "onda": "lorc/big-wave", "navio": "delapouite/sailboat", "espiral": "lorc/magic-swirl",
    "arpao": "lorc/harpoon-trident",
}


def baixar(caminho):
    u = f"https://raw.githubusercontent.com/game-icons/icons/master/{caminho}.svg"
    r = urllib.request.Request(u, headers={"User-Agent": "motion-video-tool/1.0"})
    return urllib.request.urlopen(r, timeout=60).read().decode("utf-8")


PASTA.mkdir(parents=True, exist_ok=True)
saida, falhas = {}, []
for nome, caminho in LISTA.items():
    try:
        svg = baixar(caminho)
    except Exception as e:
        falhas.append((nome, caminho, str(e)[:60]))
        continue
    (PASTA / f"{nome}.svg").write_text(svg, encoding="utf-8")
    caminhos = [d for d in re.findall(r'<path[^>]*\sd="([^"]+)"', svg) if not d.startswith("M0 0h512v512H0z")]
    saida[nome] = caminhos
(RAIZ / "assets" / "icones.js").write_text("window.ICONES=" + json.dumps(saida) + ";", encoding="utf-8")
json.dump({k: v for k, v in LISTA.items() if k in saida}, open(PASTA / "origem.json", "w", encoding="utf-8"), indent=1)
print("ok", len(saida), "falhas", falhas)
