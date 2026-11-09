# Shinobi Synex: kit de motion design

Este repositório explica, para outra IA (ou pessoa), como produzir vídeos promocionais em motion design no estilo que foi aprovado aqui. Ele traz o vídeo final, o roteiro, o prompt da voz, o código de cada cena, as regras de estilo e a análise quadro a quadro das referências.

O caso pronto é o vídeo do **Shinobi Synex**, um RPG de Naruto jogado no Discord: 58,5 s, 16:9, 1920x1080, 30 fps, com narração em português do Brasil.

## Comece por aqui

| Ordem | Arquivo | Para quê |
|---|---|---|
| 1 | [`video/shinobi-synex-filme-v3.mp4`](video/shinobi-synex-filme-v3.mp4) e as folhas `video/quadros-*.jpg` | Ver o resultado aprovado (3 quadros por segundo nas folhas) |
| 2 | [`docs/01-como-fazer-um-video.md`](docs/01-como-fazer-um-video.md) | O processo inteiro, do roteiro ao arquivo final |
| 3 | [`docs/02-prompts.md`](docs/02-prompts.md) | Roteiro, prompt da voz na ElevenLabs e os pedidos da pessoa, palavra por palavra |
| 4 | [`skill/motion-referencias/references/preferencias.md`](skill/motion-referencias/references/preferencias.md) | O que a pessoa aprova e o que ela recusou. Leia antes de criar |
| 5 | [`docs/03-estilo.md`](docs/03-estilo.md) | O estilo visual em números: ritmo, cores, transições, tipografia |
| 6 | [`filme/`](filme/) | Projeto HyperFrames completo do vídeo (HTML + GSAP), cena por cena |
| 7 | [`skill/motion-referencias/`](skill/motion-referencias/) | Skill do Claude Code: analisa referências e guia a criação |
| 8 | [`docs/04-historico.md`](docs/04-historico.md) | Versões, o que foi recusado e por quê |
| 9 | [`docs/05-licencas.md`](docs/05-licencas.md) | Origem e licença de cada música, efeito, ícone e imagem |

## Em uma frase, o estilo
Palavras grandes que trocam a cada palavra falada, fundo que alterna claro, escuro e cor da marca, cada cena nascendo de um elemento da anterior (ponto, íris, tinta, corte), algo se mexendo em todo quadro, bonecos de palito nas histórias cômicas, chibi narradora sempre em imagem fixa, e música e efeitos no tempo das palavras.

## Ferramentas
- **HyperFrames** (`npx hyperframes`, versão 0.9.17): renderiza HTML com timeline GSAP em vídeo, quadro a quadro, sempre igual. Comandos: `check --json`, `render -o arquivo.mp4`, `snapshot`.
- **GSAP 3.15** pelo CDN, com timelines pausadas e sem `Math.random` (há gerador com semente em `L.rng`).
- **ElevenLabs** para a voz, com tempo por palavra (`with-timestamps`). Esse tempo vira `filme/assets/palavras.js` e marca o relógio de todas as cenas.
- **Python 3 + numpy + ffmpeg** para analisar referências, alinhar efeitos pelo pico do som, recortar a música e normalizar em −14 LUFS.
- **Mixkit** (mixkit.co) para música e efeitos grátis; **game-icons.net** para ícones (CC BY 3.0).

## O que não está aqui (e como recuperar)
- **Vídeos de referência de terceiros** (Beaky, Cendap, GesPat, Hakuna, Open Manager, Season Cloud, Voltz, Zei e um vídeo de tipografia do Instagram): não são nossos. A leitura deles está em texto e números em `analise/` e em `skill/motion-referencias/references/leitura/`.
- **Trechos de gameplay** de Red Dead Redemption 2 e Kingdom Come: Deliverance (`filme/assets/video/rdr.mp4` e `kcd.mp4`): recorte 4 s de qualquer gameplay e salve nesses nomes.
- **Música e efeitos da Mixkit**: a licença não permite redistribuir os arquivos soltos. Baixe de novo com `python filme/tools/mixkit.py baixar <ids>`; os ids usados estão em `filme/tools/montar.py`.
- **Chave da ElevenLabs**: nunca vai para o repositório. Fica num `.env` local (`ELEVENLABS_API_KEY=...`).

## Como renderizar o filme daqui
```bash
cd filme
python tools/mixkit.py catalogo          # opcional: o catálogo já está em assets/som/mixkit
python tools/mixkit.py baixar $(cat assets/som/mixkit/ids.txt)   # música + 45 efeitos
python tools/montar.py                   # gera index.html, recorta a música e posiciona os 165 efeitos
npx hyperframes check --json
npx hyperframes render -o filme.mp4
ffmpeg -i filme.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k final.mp4
```
