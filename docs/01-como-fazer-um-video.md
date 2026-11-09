# Como fazer um vídeo destes

Este é o processo que gerou o vídeo aprovado. Siga na ordem: cada etapa depende da anterior.

## 0. Material de entrada
- **Roteiro (copy)** fechado, em português do Brasil, falado rápido. O do Shinobi Synex está em [`02-prompts.md`](02-prompts.md).
- **Referências** de motion design: vídeos que a pessoa quer imitar. Ela pensa por referência ("nesse estilo").
- **Assets do produto**: logo, personagens e telas reais. Personagens do sistema aparecem só onde o assunto são eles; no resto, use ícones ou elementos desenhados.
- **Narradora**: chibi em imagem fixa (`filme/assets/chibi/*.png`), uma expressão por cena e nunca com a boca abrindo e fechando.

## 1. Destrinchar as referências
```bash
python skill/motion-referencias/scripts/destrinchar.py VIDEO.mp4 --saida analise/<nome>
python skill/motion-referencias/scripts/comparar.py analise/<nome>/resumo.md
```
- O script mede todos os quadros e gera:
  - `resumo.md`: cenas, cortes por minuto, brilho e cores.
  - `eventos.json`: cortes, flashes, implosões e impactos.
  - Folhas com todos os quadros, uma por segundo.
- Depois **olhe** as folhas, porque o número não vê a ideia.
- As leituras prontas das 9 referências estão em `analise/*/resumo.md` e `skill/motion-referencias/references/leitura/*.md`.
- O resumo de cada uma está em `skill/motion-referencias/references/fichas.md`.

## 2. Gerar a voz antes de animar
- **Ferramenta:** ElevenLabs, endpoint `/v1/text-to-speech/{voice_id}/with-timestamps`. O script está em [`voz/gerar_voz_aw1.py`](../voz/gerar_voz_aw1.py).
- **Configuração aprovada:**
  - Voz `aw1` (`xeY9slKb5XBrj6sLUV4S`, da conta da pessoa).
  - Modelo `eleven_v4`, estabilidade 0,52, similaridade 0,75.
  - Tag `[fast-paced]` no começo do texto.
  - Rende cerca de 2,7 palavras por segundo.
- **Saída:** o tempo de cada palavra vai para `voz/aw1.json` e vira `filme/assets/palavras.js`, com `window.W[i]` (início) e `window.WE[i]` (fim).
- **Regra:** toda animação é marcada por `W[índice]`, e o texto entra na palavra falada, nunca antes.
- **Volume:** normalize a narração em −16 LUFS (`filme/assets/som/narracao.mp3`).

## 3. Escrever o SPEC
Antes de codar, faça uma tabela de cenas com o tempo pela voz, a fala, o que acontece e qual referência foi usada. Veja `filme/SPEC.md`. Regras:
- **Fio condutor:** escolha um que passe por todas as cenas. Aqui é um ponto vermelho que vira laranja e atravessa o filme: implode no fim de uma cena e nasce na seguinte.
- **Sem corte seco:** as cenas se sobrepõem de 0,1 a 0,3 s, e a nova cobre a anterior por íris (`clip-path` em círculo), tinta, corte diagonal, virada de página ou zoom através de um objeto.

## 4. Montar no HyperFrames
Estrutura de `filme/`:
- `index.html`: gerado por `tools/montar.py`. Monta as cenas sobrepostas, a camada de grão, a voz, a música e os efeitos.
- `compositions/<cena>.html`: uma cena por arquivo, dentro de `<template>`. Cada cena tem uma timeline GSAP pausada registrada em `window.__timelines[id]`. Os tempos dentro da cena são globais: `S` é o início da cena e o código usa `t - S`.
- `assets/lib.js`: a biblioteca de movimento, descrita abaixo.

Funções de `lib.js`:

| Função | O que faz |
|---|---|
| `L.k(tl, sel, S, [[t,{props},ease],...])` | Quadros-chave em tempo global |
| `L.batida(tl, S, quadros, fim)` | Uma palavra por quadro e o fundo troca a cada palavra (o estilo da referência de tipografia) |
| `L.pop`, `L.palavra`, `L.impacto`, `L.carimbo` | Entradas de palavra e de selo |
| `L.ecos` | Cópias em contorno que crescem atrás da palavra |
| `L.vivo` | Deriva lenta, para nada ficar parado |
| `L.treme` | Tremida de câmera |
| `L.iris` | Transição em círculo |
| `L.implode` | Implosão até um ponto |
| `L.anel` | Anel que abre e some |
| `L.passos` | Animação a 12 quadros por segundo (bonecos de palito e recorte) |
| `L.cursor` | Mouse que arrasta e clica |
| `L.confete`, `L.poeira` (canvas) | Partículas |
| `L.drive` | Liga qualquer desenho de canvas ao tempo da timeline |
| `L.rng` | Aleatório com semente, para o render sair sempre igual |
| `L.icones` | Desenha os ícones do game-icons.net (`<svg data-ic="nome">`) |

`compositions/grao.html` cobre o filme inteiro com poeira de película, trocada 15 vezes por segundo, para todo quadro ter movimento.

## 5. Som
- **Música:** Mixkit. Meça a energia por meio segundo e a grade de batidas (`tools/analisar_musica.py`), porque ela é escolhida sem ouvir. Escolha o ponto de início para um compasso cair no logo. Abafe com passa-baixa no "problema" e na virada final e abra tudo no logo. Fica em volume 0,2 sob a voz. Veja o bloco `OFF` e `lp` em `tools/montar.py`.
- **Efeitos:** Mixkit, um em cada ação visível: whoosh em toda troca de quadro, impacto em toda palavra gigante, pop em cada elemento que estala, clique no mouse e espada nas lutas.
  - Cada efeito é posicionado pelo **pico** do som: `início = instante do impacto + 0,033 − pico`.
  - As faixas de áudio não se sobrepõem.
- **Mix final:** normalize em −14 LUFS (`loudnorm`), com pico abaixo de −1,5 dB.

## 6. Revisar
1. `npx hyperframes check --json`: zero erros. São aceitos os avisos `line_unread` das palavras-relâmpago, porque são de propósito.
2. Renderize e faça folhas a 3 quadros por segundo do arquivo final (`ffmpeg ... fps=3,tile=6x5`). Olhe tudo:
   - quadros pretos entre cenas;
   - elementos de uma cena vazando na outra;
   - textos pequenos demais;
   - trechos parados.
3. Amplie os encaixes finos quadro a quadro (`fps=30,tile=7x3`).
4. Meça o som (`ebur128`) e diga que ele foi medido, não ouvido.

## 7. Entregar
Gere um MP4 final e uma cópia leve (menos de 30 MB, `-b:v 3300k`) para o celular.
