"""Catálogo da Mixkit (música e efeitos grátis, licença Mixkit, sem crédito obrigatório).

Uso:
  python tools/mixkit.py catalogo            -> assets/som/mixkit/catalogo.json
  python tools/mixkit.py baixar ID [ID...]   -> assets/som/mixkit/baixados/<tipo>_<id>.mp3
"""
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"}
RAIZ = os.path.join(os.path.dirname(__file__), "..", "assets", "som", "mixkit")
CAT = os.path.join(RAIZ, "catalogo.json")

SFX = ["whoosh", "swoosh", "transition", "swipe", "sword", "impact", "hit", "punch", "boom", "bass",
       "pop", "click", "mouse-click", "glitch", "typing", "keyboard", "magic", "sparkle", "shine", "riser",
       "cinematic", "paper", "dice", "game", "bell", "gong", "stamp", "slash", "knife", "drum", "wind",
       "fire", "camera", "notification", "reward", "coin", "level-up", "page", "scroll", "achievement"]
MUSICA = ["tag/trap", "tag/action", "tag/energetic", "electronic", "cinematic", "hip-hop", "tag/sport",
          "tag/asian", "tag/epic", "tag/upbeat", "tag/intense", "tag/aggressive", "tag/dramatic"]


def get(u):
    # a Mixkit limita pedidos seguidos (HTTP 429): espera entre páginas e tenta de novo
    for tentativa in range(4):
        time.sleep(2.5 + tentativa * 15)
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
    raise RuntimeError("429 persistente: " + u)


def sfx_da_pagina(h, cat):
    itens = []
    for b in h.split('class="item-grid__item"')[1:]:
        u = re.search(r'data-audio-player-preview-url-value="([^"]+)"', b)
        i = re.search(r'data-audio-player-item-id-value="(\d+)"', b)
        t = re.search(r'item-grid-card__title">\s*(.*?)\s*</h2>', b, re.S)
        d = re.search(r'data-test-id="duration">\s*([\d:]+)', b)
        tags = re.findall(r'meta-links__link"[^>]*href="/free-sound-effects/([^/]+)/"', b)
        if u and i:
            m, s = (d.group(1).split(":") if d else ("0", "0"))
            itens.append({"tipo": "sfx", "id": i.group(1), "titulo": html.unescape(t.group(1)) if t else "",
                          "dur": int(m) * 60 + int(s), "url": u.group(1), "cats": sorted(set(tags + [cat]))})
    return itens


def musica_da_pagina(h, cat):
    itens = []
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            d = json.loads(m)
        except ValueError:
            continue
        for g in d.get("@graph", []):
            if g.get("@type") != "ItemList":
                continue
            for it in g["itemListElement"]:
                if it.get("@type") != "MusicRecording":
                    continue
                dm = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", it.get("duration", ""))
                dur = int(dm.group(1) or 0) * 60 + int(dm.group(2) or 0) if dm else 0
                mid = re.search(r"/music/(\d+)/", it["url"]).group(1)
                itens.append({"tipo": "musica", "id": mid, "titulo": it.get("name", ""), "artista": it.get("byArtist", ""),
                              "genero": it.get("genre", ""), "dur": dur, "url": it["url"], "cats": [cat]})
    return itens


def catalogo():
    os.makedirs(RAIZ, exist_ok=True)
    todos = json.load(open(CAT, encoding="utf-8")) if os.path.exists(CAT) else {}
    feitos = {c for v in todos.values() for c in v["cats"]}
    for c in SFX:
        if c in feitos:
            continue
        for p in (1, 2):
            u = f"https://mixkit.co/free-sound-effects/{c}/" + (f"?page={p}" if p > 1 else "")
            try:
                for it in sfx_da_pagina(get(u), c):
                    k = "sfx_" + it["id"]
                    if k in todos:
                        todos[k]["cats"] = sorted(set(todos[k]["cats"] + it["cats"]))
                    else:
                        todos[k] = it
            except Exception as e:  # página inexistente
                print("sfx", c, p, e)
                break
    for c in MUSICA:
        if c in feitos:
            continue
        for p in (1, 2, 3):
            u = f"https://mixkit.co/free-stock-music/{c}/" + (f"?page={p}" if p > 1 else "")
            try:
                novos = musica_da_pagina(get(u), c)
            except Exception as e:
                print("musica", c, p, e)
                break
            if not novos:
                break
            for it in novos:
                k = "musica_" + it["id"]
                if k in todos:
                    todos[k]["cats"] = sorted(set(todos[k]["cats"] + it["cats"]))
                else:
                    todos[k] = it
    json.dump(todos, open(CAT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len([v for v in todos.values() if v["tipo"] == "sfx"]), "efeitos,",
          len([v for v in todos.values() if v["tipo"] == "musica"]), "músicas")


def baixar(ids):
    cat = json.load(open(CAT, encoding="utf-8"))
    pasta = os.path.join(RAIZ, "baixados")
    os.makedirs(pasta, exist_ok=True)
    for k in ids:
        it = cat[k]
        dest = os.path.join(pasta, f"{k}.mp3")
        if not os.path.exists(dest):
            open(dest, "wb").write(urllib.request.urlopen(urllib.request.Request(it["url"], headers=UA), timeout=60).read())
        print(dest, it["titulo"])


if __name__ == "__main__":
    if sys.argv[1] == "catalogo":
        catalogo()
    else:
        baixar(sys.argv[2:])
