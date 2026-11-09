"""Baixa os áudios escolhidos no Openverse (efeitos CC0 do Freesound e candidatos de música CC BY do Jamendo)."""
import json
import pathlib
import urllib.request

R = pathlib.Path(__file__).resolve().parents[1] / "assets" / "som"
F = "https://cdn.freesound.org/previews/"
EFEITOS = {
    "whoosh1": ("60/60026_71257-hq.mp3", "Swosh swoosh whoosh air sound", "qubodup"),
    "whoosh2": ("60/60007_71257-hq.mp3", "Swipe Whoosh", "qubodup"),
    "whoosh3": ("220/220191_4100837-hq.mp3", "Space Swoosh - brighter", "GameAudio"),
    "whoosh_grave": ("351/351256_2247456-hq.mp3", "Deep Whoosh #1", "Kinoton"),
    "riser": ("244/244249_3986112-hq.mp3", "impact riser 01", "soramoosic"),
    "dado": ("353/353974_1815993-hq.mp3", "rolling dice 2", "nettimato"),
    "corte1": ("147/147288_1401157-hq.mp3", "Sword Slash 1", "smokebomb99"),
    "corte2": ("147/147287_1401157-hq.mp3", "Sword Slash 2", "smokebomb99"),
    "facada": ("380/380268_3294528-hq.mp3", "Freezer Ice Stab Knife 03", "Glitchedtones"),
    "papel1": ("82/82377_605154-hq.mp3", "paper flip 1", "gynation"),
    "papel2": ("82/82378_605154-hq.mp3", "paper flip 2", "gynation"),
    "papel3": ("82/82379_605154-hq.mp3", "paper flip 3", "gynation"),
    "brilho": ("462/462095_6142149-hq.mp3", "Sparkling Star 01", "MATRIXXX_"),
    "impacto1": ("512/512389_3997858-hq.mp3", "Bass Impact - Ki_01", "Kievinay"),
    "impacto2": ("617/617043_887696-hq.mp3", "Bass Impact 3", "D4XX"),
    "clique": ("456/456394_6339135-hq.mp3", "Click mouse computer", "Webs206"),
    "glitch": ("277/277053_5048136-hq.mp3", "glitch sound 1", "dotY21"),
}
MUSICAS = {
    "m_dnb": ("https://prod-1.storage.jamendo.com/?trackid=1406196&format=mp32", "Helike [Drum and Bass]", "Hardcore Scm"),
    "m_techno": ("https://prod-1.storage.jamendo.com/?trackid=1367851&format=mp32", "Retro Futurism", "Notorious Twins"),
    "m_trailer": ("https://prod-1.storage.jamendo.com/?trackid=1308697&format=mp32", "Fusion - Dark Epic Trailer", "E. Erkut"),
}


def baixar(url, destino):
    if destino.exists():
        return
    r = urllib.request.Request(url, headers={"User-Agent": "motion-video-tool/1.0"})
    destino.write_bytes(urllib.request.urlopen(r, timeout=180).read())


R.mkdir(parents=True, exist_ok=True)
(R / "orig").mkdir(exist_ok=True)
for n, (u, t, a) in EFEITOS.items():
    baixar(F + u, R / "orig" / f"{n}.mp3")
for n, (u, t, a) in MUSICAS.items():
    baixar(u, R / "orig" / f"{n}.mp3")
json.dump({"efeitos": EFEITOS, "musicas": MUSICAS}, open(R / "origem.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(list((R / "orig").glob("*.mp3"))))
