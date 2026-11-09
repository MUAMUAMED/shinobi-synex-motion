"""Monta index.html: cenas sobrepostas, grão por cima, voz, música (Mixkit) e efeitos (Mixkit) alinhados pelo pico."""
import pathlib
import subprocess

import numpy as np

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SOM = RAIZ / "assets" / "som"
MK = SOM / "mixkit" / "baixados"
DUR = 58.5
CENAS = [("a", 0, 7.3), ("b", 7.05, 10.95), ("c", 10.7, 14.95), ("d", 14.4, 22.6), ("e", 22.35, 28.75),
         ("f", 28.55, 39.45), ("g", 39.1, 49.9), ("h", 49.7, DUR)]

# Apelidos dos efeitos (Mixkit, licença livre; o dado é do Freesound, CC0)
ARQ = {
    "wf": "sfx_1492", "wf2": "sfx_1490", "sw": "sfx_3115", "sweep": "sfx_166", "sweep2": "sfx_174", "acc": "sfx_1464",
    "zoom": "sfx_2627", "vac": "sfx_2608", "logo": "sfx_2902", "logo2": "sfx_2900", "zimp": "sfx_772", "bass": "sfx_2299",
    "fbass": "sfx_2303", "blow": "sfx_2655", "deep": "sfx_1143", "epic": "sfx_2908", "riser": "sfx_790",
    "pop": "sfx_2364", "lpop": "sfx_2358", "click": "sfx_2997", "sclick": "sfx_2582", "glitch": "sfx_2951",
    "glitch2": "sfx_1031", "key": "sfx_2541", "swordw": "sfx_2792", "samurai": "sfx_2789", "strike": "sfx_2166",
    "ninja": "sfx_2146", "knife": "sfx_2184", "slice": "sfx_2152", "page": "sfx_1104", "bigpage": "sfx_1105",
    "paper": "sfx_2380", "scribble": "sfx_2369", "wand": "sfx_3062", "fairy": "sfx_871", "touch": "sfx_3083",
    "unlock": "sfx_2349", "lvl": "sfx_2062", "done": "sfx_2059", "bonus": "sfx_2058", "punch": "sfx_2047",
    "wood": "sfx_2182", "bswitch": "sfx_2301", "tick": "sfx_1046", "dado": "../../orig/dado",
}

# (apelido, instante do impacto, volume[, início no arquivo, duração])
EFEITOS = [
    # A: problema em batida
    ("pop", 0.06, 0.35), ("bass", 0.18, 0.45), ("sclick", 0.44, 0.3), ("sclick", 0.56, 0.3), ("sclick", 0.68, 0.3),
    ("sw", 0.93, 0.35), ("blow", 1.37, 0.4), ("bswitch", 1.76, 0.35), ("acc", 2.24, 0.3), ("zimp", 2.65, 0.5),
    ("sweep", 3.08, 0.35), ("glitch2", 3.12, 0.2), ("acc", 3.56, 0.3), ("blow", 3.69, 0.4), ("sw", 4.32, 0.3),
    ("zimp", 4.57, 0.45), ("sweep", 4.88, 0.3), ("pop", 5.04, 0.22), ("pop", 5.1, 0.18), ("pop", 5.16, 0.18),
    ("pop", 5.22, 0.18), ("pop", 5.28, 0.18), ("wf2", 5.4, 0.4), ("acc", 5.72, 0.3), ("blow", 5.89, 0.35),
    ("zimp", 6.2, 0.55), ("bass", 6.21, 0.5), ("scribble", 6.45, 0.5), ("glitch", 6.73, 0.45), ("vac", 7.0, 0.45),
    # B: Mas... Shinobi Synex
    ("fbass", 7.29, 0.5), ("wf", 7.9, 0.3), ("riser", 9.28, 0.5), ("logo", 9.28, 0.75), ("bass", 9.85, 0.55),
    ("unlock", 9.92, 0.35), ("sw", 10.62, 0.35),
    # C: inspirado em
    ("wf2", 10.86, 0.3), ("sweep", 11.5, 0.3), ("wf", 12.16, 0.45), ("zimp", 12.2, 0.35), ("wf2", 13.2, 0.45),
    ("zimp", 13.24, 0.35), ("deep", 14.62, 0.45),
    # D: +120 NPCs e conceitos
    ("sweep2", 14.56, 0.35), ("pop", 15.62, 0.3),
    ("key", 16.1, 0.15), ("key", 16.22, 0.15), ("key", 16.34, 0.15), ("key", 16.46, 0.15), ("key", 16.58, 0.15),
    ("key", 16.7, 0.15), ("key", 16.82, 0.15), ("key", 16.94, 0.15), ("zimp", 17.13, 0.45),
    ("wf2", 17.94, 0.4), ("blow", 17.97, 0.35), ("tick", 18.05, 0.3, 1.0, 0.8), ("pop", 18.08, 0.2), ("pop", 18.2, 0.2), ("pop", 18.32, 0.2),
    ("sw", 18.82, 0.4), ("blow", 18.85, 0.35), ("wand", 19.0, 0.4), ("lpop", 19.12, 0.3), ("pop", 19.16, 0.2),
    ("pop", 19.3, 0.2), ("pop", 19.44, 0.2),
    ("wf", 19.74, 0.3), ("samurai", 19.77, 0.45), ("fairy", 19.86, 0.3),
    ("sweep", 20.28, 0.35), ("pop", 20.36, 0.2), ("pop", 20.44, 0.2), ("pop", 20.52, 0.2),
    ("sw", 20.7, 0.4), ("paper", 20.76, 0.3), ("paper", 20.83, 0.3), ("paper", 20.9, 0.3), ("paper", 20.97, 0.3),
    ("zimp", 21.6, 0.55), ("wf", 21.64, 0.35), ("vac", 22.16, 0.45),
    # E: amizade, jutsus, poderes, casar
    ("lpop", 23.24, 0.4), ("touch", 23.38, 0.3), ("pop", 23.92, 0.35), ("click", 24.57, 0.6), ("acc", 24.62, 0.3),
    ("click", 25.73, 0.6), ("acc", 25.78, 0.3), ("click", 27.21, 0.6), ("wand", 27.32, 0.45), ("bonus", 27.38, 0.35),
    ("zimp", 27.5, 0.4), ("bigpage", 28.46, 0.55),
    # F: bonecos de palito
    ("page", 28.64, 0.45), ("pop", 28.84, 0.3), ("click", 29.9, 0.5),
    ("wood", 30.2, 0.15), ("wood", 30.7, 0.15), ("wood", 31.2, 0.15), ("wood", 31.7, 0.15), ("wood", 32.2, 0.15),
    ("click", 32.96, 0.5), ("fairy", 33.4, 0.3), ("bswitch", 33.45, 0.3),
    ("wand", 35.1, 0.45), ("unlock", 35.3, 0.45), ("blow", 35.45, 0.4),
    ("knife", 36.48, 0.55), ("slice", 36.72, 0.55), ("blow", 36.85, 0.4), ("punch", 37.1, 0.35),
    ("dado", 37.6, 0.5), ("dado", 38.0, 0.35), ("done", 38.22, 0.4), ("zoom", 39.0, 0.5),
    # G: sistemas
    ("wf2", 39.3, 0.35), ("strike", 40.86, 0.55), ("swordw", 40.95, 0.4), ("zimp", 40.98, 0.5), ("bass", 41.0, 0.45),
    ("samurai", 41.2, 0.45), ("strike", 41.62, 0.45), ("ninja", 41.96, 0.45),
    ("sw", 42.22, 0.35), ("bswitch", 43.55, 0.35), ("lvl", 44.16, 0.45),
    ("wf", 44.4, 0.35), ("page", 44.52, 0.45), ("click", 46.16, 0.6), ("dado", 46.3, 0.5), ("done", 47.05, 0.45),
    ("bonus", 47.08, 0.3), ("sweep", 47.38, 0.35), ("pop", 47.7, 0.2), ("pop", 47.9, 0.2), ("pop", 48.1, 0.2),
    ("zimp", 48.86, 0.45), ("vac", 49.34, 0.4),
    # H: a próxima inovação será você
    ("sw", 49.95, 0.35), ("blow", 50.0, 0.3), ("acc", 50.14, 0.3), ("blow", 50.29, 0.3), ("zimp", 50.63, 0.45),
    ("acc", 51.18, 0.3), ("sclick", 51.3, 0.25), ("sclick", 51.34, 0.25), ("sclick", 51.38, 0.25),
    ("epic", 51.44, 0.7), ("bass", 51.45, 0.5), ("sw", 51.86, 0.3), ("blow", 52.17, 0.3), ("acc", 52.46, 0.3),
    ("zimp", 52.65, 0.4), ("scribble", 52.85, 0.4), ("wf2", 53.4, 0.35), ("lpop", 53.5, 0.35),
    ("riser", 54.4, 0.45), ("logo", 54.4, 0.8), ("bass", 54.97, 0.55), ("unlock", 55.02, 0.35), ("fairy", 55.27, 0.35),
    ("sw", 57.0, 0.3), ("deep", 57.5, 0.3),
]


def decodificar(arq):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(arq), "-ac", "1", "-ar", "11025", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def caminho(apelido):
    return (MK / f"{ARQ[apelido]}.mp3").resolve()


def info(apelido, ms, dur):
    x = decodificar(caminho(apelido))
    total = len(x) / 11025
    dur = min(dur if dur else 2.5, total - ms)
    trecho = np.abs(x[int(ms * 11025): int((ms + dur) * 11025)])
    return float(np.argmax(trecho) / 11025), dur


# Música: "War Cry" (Michael Ramir C., Mixkit). Começa 0,12 s dentro da faixa para um compasso cair no "Shinobi" (9,28 s).
# Abafada (passa-baixa) no problema e na virada final, e abre com tudo no logo.
OFF = 0.12
lp = "if(lt(t,7.2),1,if(lt(t,9.28),1-(t-7.2)/2.08,if(lt(t,49.9),0,if(lt(t,50.2),(t-49.9)/0.3,if(lt(t,54.36),1,0)))))"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(OFF), "-t", str(DUR), "-i", str(MK / "musica_1122.mp3"),
                "-filter_complex",
                f"[0:a]asplit[a][b];[a]lowpass=f=420,lowpass=f=420,volume=1.5,volume='{lp}':eval=frame[l];"
                f"[b]volume='1-({lp})':eval=frame[h];[l][h]amix=inputs=2:normalize=0,"
                f"afade=t=in:d=0.25,afade=t=out:st={DUR - 2.2}:d=2.1",
                "-c:a", "libmp3lame", "-b:a", "192k", str(SOM / "musica.mp3")], check=True)

cache, linhas, livre = {}, [], {}
for i, e in enumerate(EFEITOS):
    nome, t, vol = e[:3]
    ms = e[3] if len(e) > 3 else 0.0
    dur = e[4] if len(e) > 4 else None
    chave = (nome, ms, dur)
    if chave not in cache:
        cache[chave] = info(nome, ms, dur)
    pico, d = cache[chave]
    inicio = t + 0.033 - pico
    corte = ms
    if inicio < 0:
        corte, d, inicio = ms - inicio, d + inicio, 0.0
    d = min(d, DUR - inicio)
    src = caminho(nome).relative_to(RAIZ).as_posix()
    trilha = next(k for k in range(30, 99) if livre.get(k, -1) <= inicio)
    livre[trilha] = inicio + d + 0.01
    linhas.append(f'      <audio id="sfx{i}" src="{src}" data-start="{inicio:.3f}" data-duration="{d:.3f}"'
                  + (f' data-media-start="{corte:.3f}"' if corte > 0 else "") + f' data-volume="{vol}" data-track-index="{trilha}"></audio>')

hosts = "\n".join(
    f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="{1 + n % 2}" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:{n + 1}"></div>'
    for n, (c, a, b) in enumerate(CENAS))
hosts += f'\n      <div id="grao" data-composition-id="grao" data-composition-src="compositions/grao.html" data-start="0" data-duration="{DUR}" data-track-index="5" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:50;pointer-events:none"></div>'
(RAIZ / "index.html").write_text(f"""<!doctype html>
<html lang="pt-BR" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <script src="assets/palavras.js"></script>
    <script src="assets/icones.js"></script>
    <script src="assets/recriados.js"></script>
    <script src="assets/lib.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #0b0a10; }}
      #root {{ position: relative; width: 100%; height: 100%; background: #0b0a10; font-family: "Outfit", sans-serif; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
      <audio id="narracao" src="assets/som/narracao.mp3" data-start="0" data-duration="55.68" data-volume="1" data-track-index="10"></audio>
      <audio id="musica" src="assets/som/musica.mp3" data-start="0" data-duration="{DUR}" data-volume="0.2" data-track-index="11"></audio>
{chr(10).join(linhas)}
{hosts}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""", encoding="utf-8")
print("ok", len(linhas), "efeitos")
