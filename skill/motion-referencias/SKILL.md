---
name: motion-referencias
description: Destrincha vídeos de referência de motion design frame a frame, identifica o modelo de edição e recria esse estilo em novos vídeos com HyperFrames. Use sempre que a pessoa mandar um vídeo, link ou pasta de referência e pedir "nesse estilo", "igual a esse", "recria", "faz parecido" ou "analisa essa edição", e também em qualquer vídeo promocional, anúncio, vinheta, apresentação de produto, app, servidor ou marca em motion design, mesmo que não cite referência. Traz 5 modelos de edição, catálogo de transições com frames medidos, biblioteca de animação e as preferências já dadas pela pessoa.
---

# Motion a partir de referências

A pessoa pensa em vídeos por referência: "quero nesse estilo". O trabalho é transformar a referência em decisões medidas e depois montar o vídeo com a coreografia dela e o conteúdo novo.

O erro mais caro já cometido aqui foi montar um layout próprio "inspirado" em vez de reaproveitar a coreografia real: essa versão foi recusada, e a feita com os keyframes da referência virou a base dos ajustes. Copie o movimento, troque o conteúdo.

## Fluxo

### 1. Destrinchar a referência

```bash
python <skill>/scripts/destrinchar.py VIDEO --saida <projeto>/analise/<nome>
python <skill>/scripts/comparar.py <projeto>/analise/<nome>/resumo.md
```

Isso mede todos os frames e gera `resumo.md`, `eventos.json`, `cenas.json`, `visao-geral.jpg`, `eventos/*.jpg` (quadro a quadro em volta dos eventos fortes) e `todos/*.jpg` (todos os frames, uma folha por segundo).

Depois **olhe**, porque o número não vê a ideia:
1. `visao-geral.jpg`, sempre.
2. Pelo menos 6 folhas de `eventos/`, priorizando implosão, impacto, chicote, estrobo e flash.
3. Em `todos/`, os segundos que você vai copiar de perto.

`corte` conta só trocas bruscas. Em vídeos de transição contínua (Beaky, Open Manager) ele subestima muito as mudanças de cena, e a etiqueta de `implosao` ou `impacto` pode errar. Confirme na imagem antes de copiar um valor.

Diga à pessoa quantos frames mediu e quantos realmente olhou. Medir não é ver.

### 2. Escolher o modelo

Leia `references/modelos.md`. `comparar.py` é só uma pista: no teste, cada referência comparada às outras caiu no modelo certo em 5 de 8 casos. Ele separa bem claro de escuro e ritmo, mas confunde Neon com Imersivo e Zei com Bloco de cor. A imagem decide. Modelos: **Branco contínuo**, **Bloco de cor**, **Neon escuro**, **Imersivo de objetos** e **Recorte**. Um vídeo pode usar um modelo base e um trecho de outro, como o Recorte dentro do Imersivo.

Para uma referência das 8 já estudadas, leia a ficha em `references/fichas.md`.

### 3. Fechar a narração antes das cenas

O tempo do vídeo sai da voz, então gere a narração com tempo por palavra antes de animar. Ritmo de referência: cerca de 2,9 palavras por segundo com poucas pausas (estimativa a partir da transcrição do Voltz).

Se a voz mudar depois, não reescreva tempos. Use `FX.tl(S)` e `window.TMAP` (`assets/fx.js`): as cenas continuam descritas no tempo antigo e o mapa converte tudo pelas palavras.

### 4. Montar

Use `references/movimentos.md` para o catálogo e `assets/fx.js` como biblioteca. Para fidelidade máxima, parta das cenas prontas em `assets/voltz-composicoes/` e do gerador em `assets/exemplo-gerador.py`: eles guardam os keyframes frame a frame da Voltz.

Em HyperFrames, siga as regras da skill `hyperframes`. Regras do estilo:
- Uma ideia por tela, com texto pequeno e centralizado na maioria das vezes. Texto gigante é evento raro.
- Cada cena nasce de um elemento ou impacto da anterior. Evite corte parado.
- Ritmo de 3 tempos: impacto (2 a 4 frames), assentamento (6 a 10 frames), deriva lenta até o fim.
- Elementos não ficam estacionados. Se a apresentadora fica no mesmo canto a cena inteira, está errado.
- Texto entra na palavra falada, não antes.

### Filme novo, sem reaproveitar uma referência
Quando a pessoa pedir um filme "com tudo que tem de referência", não parta da Voltz. O que funcionou no filme do Shinobi Synex (`D:\shinobi-rpg-video\synex-film`, base em `assets/filme-exemplo/`):
- Um objeto protagonista (um ponto) atravessa o filme e vira cada coisa: logo, engrenagem, pílula, cursor de texto.
- Cenas sobrepostas no tempo: a cena seguinte começa 0,1 a 0,3 s antes, com fundo transparente, e cobre a anterior por íris, tinta, corte, virada de página ou zoom através de um objeto. Nenhum corte seco entre cenas.
- Tempos pela voz: `assets/palavras.js` gera `W[i]` (início de cada palavra); as cenas usam `W[61]` em vez de números soltos.
- Efeitos sonoros posicionados pelo pico de cada arquivo (`montar.py`), e música recortada para a subida cair no momento do logo.
- Música e efeitos de licença aberta via API do Openverse (Jamendo para música CC BY, Freesound para efeitos CC0) quando o catálogo do HyperFrames não está disponível. Registre os créditos.

Armadilhas já encontradas:
- `L.k` aplica o primeiro quadro-chave na montagem. Duas chamadas de `L.k` no mesmo elemento, com propriedades diferentes, sobrescrevem o estado inicial uma da outra. Use `tl.fromTo` para o segundo movimento.
- Um `tl.set` no meio de um tween do mesmo elemento é desfeito pelo tween. Coloque o `set` depois do fim dele.
- Elementos com `z-index` dentro de um container sem `z-index` sobem acima de textos de outras camadas. Dê `z-index: 0` ao container.
- Quadros-chave fora de ordem no tempo geram aviso `gsap_tween_tail` no check; corrija, porque o movimento pula.

### 5. Aplicar as preferências da pessoa

Leia `references/preferencias.md` antes de escolher imagens, voz e texto. Ela guarda correções já dadas. Atualize esse arquivo quando vier uma correção nova.

### 6. Revisar

1. `npx hyperframes check --json`.
2. Renderize e faça uma folha a 2 quadros por segundo do arquivo final. O `snapshot` pode devolver quadros em branco por corrida de carregamento; o render é o que vale.
3. Amplie os encaixes finos, como objeto sobre olho ou sobre personagem.
4. Normalize o áudio perto de -15 LUFS e meça.
5. Diga que o som foi medido, não ouvido.

## Arquivos

| Arquivo | Quando ler |
|---|---|
| `references/modelos.md` | Sempre, para escolher o modelo |
| `references/movimentos.md` | Ao montar cenas e transições |
| `references/fichas.md` | Quando a referência for uma das 8 estudadas |
| `references/leitura/*.md` | Linha do tempo por frames de cada referência, antes de copiar um trecho |
| `references/preferencias.md` | Sempre, antes de imagens, voz e texto |
| `scripts/destrinchar.py` | Para qualquer referência nova |
| `scripts/comparar.py` | Para sugerir o modelo mais próximo |
| `assets/referencias.json` | Números das 8 referências, usados pelo comparador |
| `assets/fx.js` | Biblioteca de animação |
| `assets/voltz-composicoes/` | Cenas verticais com keyframes da Voltz |
| `assets/exemplo-gerador.py` | Vídeo 16:9 completo usando os keyframes da Voltz |
