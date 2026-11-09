"""Gera a narração completa na voz aw1, com os ajustes da amostra aprovada (v4, estabilidade 52, similaridade 75)."""
import base64
import json
import pathlib
import urllib.error
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "assets" / "audio" / "tomadas"
ENV = RAIZ.parent / ".env"

TEXTO = (
    "[fast-paced] Sério... Tá todo mundo cansado daqueles RPs genéricos de Naruto, "
    "são sempre as mesmas coisas e nenhuma inovação! "
    "Mas foi fugindo dessa moda que surgiu o Shinobi Synex! "
    "Inspirado nas mecânicas de Red Dead Redemption e Kingdom Come Deliverance, "
    "o Shinobi Synex conta com mais de cento e vinte NPCs com rotinas, personalidades, "
    "histórias e vidas completamente diferentes! "
    "Você pode fazer amizade com eles, aprender Jutsus, receber poderes "
    "e até mesmo se casar com eles! "
    "É sério, você pode em um dia aleatório estar andando no meio da floresta "
    "e um homem misterioso aparecer e te dar dois Rinnegans! "
    "Ou duas facadas, depende muito da sua sorte! "
    "Além disso, Synex possui um combate dinâmico, treinos que realmente te desafiam, "
    "missões que funcionam exatamente como um RPG de mesa "
    "e vários outros sistemas inovadores! "
    "Mas a próxima inovação será você que vai fazer nessa história, "
    "seja bem-vindo ao Shinobi Synex!"
)


def chave():
    for linha in ENV.read_text(encoding="utf-8").splitlines():
        if linha.startswith("ELEVENLABS_API_KEY="):
            return linha.split("=", 1)[1].strip()
    raise SystemExit("chave não encontrada")


def api(url, corpo=None):
    h = {"xi-api-key": chave(), "User-Agent": "synex-video/1.0"}
    if corpo:
        h["Content-Type"] = "application/json"
    pedido = urllib.request.Request(url, data=json.dumps(corpo).encode("utf-8") if corpo else None, headers=h)
    try:
        with urllib.request.urlopen(pedido, timeout=300) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"ElevenLabs {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")


def palavras(al):
    saida, atual, ini, fim, col = [], "", None, None, False
    for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c == "[":
            col = True
        if col:
            col = c != "]"
            continue
        if c.isspace():
            if atual:
                saida.append({"w": atual, "s": round(ini, 3), "e": round(fim, 3)})
            atual, ini = "", None
            continue
        ini = a if ini is None else ini
        atual, fim = atual + c, b
    if atual:
        saida.append({"w": atual, "s": round(ini, 3), "e": round(fim, 3)})
    return saida


vozes = api("https://api.elevenlabs.io/v2/voices?" + urllib.parse.urlencode({"search": "aw1", "page_size": 20}))["voices"]
print([(v["voice_id"], v["name"], v.get("category")) for v in vozes])
exatas = [v for v in vozes if v["name"].strip().lower() == "aw1"] or vozes
if len(exatas) != 1:
    raise SystemExit("não achei uma única voz aw1")
d = api(f"https://api.elevenlabs.io/v1/text-to-speech/{exatas[0]['voice_id']}/with-timestamps?output_format=mp3_44100_128",
        {"text": TEXTO, "model_id": "eleven_v4", "voice_settings": {"stability": 0.52, "similarity_boost": 0.75}})
SAIDA.mkdir(parents=True, exist_ok=True)
(SAIDA / "aw1.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
lista = palavras(d.get("alignment") or d["normalized_alignment"])
(SAIDA / "aw1.json").write_text(json.dumps(lista, ensure_ascii=False), encoding="utf-8")
print(f"{len(lista)} palavras, {lista[-1]['e']:.1f} s, {len(lista) / lista[-1]['e']:.2f} palavras/s")
print(" ".join(f"{p['w']}@{p['s']}" for p in lista[:30]))
