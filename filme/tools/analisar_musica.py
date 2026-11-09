"""Mede BPM, energia por segundo e o melhor trecho de 58 s de cada música candidata."""
import subprocess
import sys

import numpy as np

SR = 11025


def carregar(arq):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", arq, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def analisar(arq, dur=58.0):
    x = carregar(arq)
    hop = 256
    n = len(x) // hop
    quadros = x[: n * hop].reshape(n, hop)
    rms = np.sqrt((quadros ** 2).mean(axis=1) + 1e-12)
    # fluxo de energia em banda larga como envelope de ataques
    env = np.maximum(np.diff(np.log(rms + 1e-6), prepend=0), 0)
    fps = SR / hop
    seg = int(fps)
    energia = np.array([rms[i:i + seg].mean() for i in range(0, n - seg, seg)])
    # BPM por autocorrelação do envelope em uma janela central
    meio = env[len(env) // 3: len(env) // 3 + int(60 * fps)]
    meio = meio - meio.mean()
    ac = np.correlate(meio, meio, "full")[len(meio) - 1:]
    lags = np.arange(len(ac)) / fps
    validos = (lags > 60 / 190) & (lags < 60 / 70)
    lag = lags[validos][np.argmax(ac[validos])]
    bpm = 60 / lag
    # trecho de 58 s com energia mais alta e mais constante
    L = int(dur)
    melhor, inicio = -1, 0
    for i in range(0, len(energia) - L):
        j = energia[i:i + L]
        nota = j.mean() - 0.6 * j.std()
        if nota > melhor:
            melhor, inicio = nota, i
    perfil = (energia / energia.max() * 9).round().astype(int)
    print(f"{arq.split('/')[-1]}: {len(x) / SR:.0f} s, BPM ~{bpm:.1f}, melhor trecho {inicio}-{inicio + L} s")
    print("  energia por s:", "".join(str(v) for v in perfil))


for a in sys.argv[1:]:
    analisar(a)
