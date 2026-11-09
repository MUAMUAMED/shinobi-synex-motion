"""Lista candidatos de música e efeitos no Openverse (licenças abertas)."""
import json
import sys
import urllib.parse
import urllib.request

BUSCAS = {
    "musica": [("energetic electronic trailer", "music"), ("upbeat hybrid orbital drum and bass", "music"), ("epic japanese taiko electronic", "music"), ("dubstep energetic instrumental", "music")],
    "sfx": [("whoosh fast", "sound_effect"), ("swoosh transition", "sound_effect"), ("riser build up", "sound_effect"), ("dice roll", "sound_effect"), ("keyboard typing", "sound_effect"), ("sword slash", "sound_effect"), ("paper rustle", "sound_effect"), ("sparkle magic", "sound_effect"), ("bass impact hit", "sound_effect"), ("ui click", "sound_effect"), ("pop bubble", "sound_effect"), ("glitch digital", "sound_effect"), ("wedding bell chime", "sound_effect")],
}


def buscar(q, cat, n=8):
    p = {"q": q, "license": "cc0,by", "page_size": n, "category": cat}
    u = "https://api.openverse.org/v1/audio/?" + urllib.parse.urlencode(p)
    r = urllib.request.Request(u, headers={"User-Agent": "motion-video-tool/1.0"})
    with urllib.request.urlopen(r, timeout=60) as f:
        return json.load(f)["results"]


for tipo in sys.argv[1:]:
    for q, cat in BUSCAS[tipo]:
        print("==", q)
        try:
            for x in buscar(q, cat):
                print(f"{x['id']} | {x['title'][:50]} | {x.get('creator', '')[:20]} | {x['license']} | {(x.get('duration') or 0) / 1000:.1f}s | {x.get('filetype')} | {x.get('source')} | {x['url']}")
        except Exception as e:
            print("ERRO", e)
