# Shinobi Synex: filme novo

1920x1080, 30 fps, 58,5 s. Voz `aw1` (narracao.mp3). Sem a base da Voltz: cada cena usa técnicas de várias referências.

## Ideia que conecta tudo
Um ponto vermelho nasce do fim do problema e vira laranja no "Mas". Esse ponto é o chakra do Synex: foge da multidão, explode no logo, vira o shuriken, o shuriken vira engrenagem, a engrenagem abre a porta para os NPCs, os NPCs viram um ponto que vira pílula, e assim por diante. Nenhuma cena entra por corte seco.

## Cor
- Noite `#0b0a10`, papel `#efe9dc`, laranja Synex `#ff5a1f`.
- Vermelho `#ff2b3a` só no problema (cena A).
- Uma cor por assunto: verde amizade, violeta jutsus, rosa casamento, azul missões, verde treinos.

## Cenas (tempo pela voz)
| Cena | Tempo | Fala | O que acontece | Referência |
|---|---|---|---|---|
| A | 0-7,3 | "Sério... nenhuma inovação!" | Chibi desconfiada; cartões de RP iguais se copiam em grade; tudo implode num ponto vermelho | Hakuna perspectiva, Cendap repetição, GesPat implosão |
| B | 7,1-10,9 | "Mas foi fugindo... Shinobi Synex!" | Ponto vira laranja, foge da multidão cinza, cresce e explode em tinta; logo com anéis | Beaky tinta e anéis, Season problema e solução |
| C | 10,7-15 | "Inspirado... Deliverance," | Shuriken vira engrenagem; painéis diagonais com as gameplays | Open Manager painel diagonal |
| D | 14,4-22,6 | "conta com +120 NPCs... diferentes!" | Entrada pelo furo da engrenagem; parede de cartões em perspectiva; contador; câmera em 4 cartões; cartões viram | Hakuna catálogo, Cendap contador |
| E | 22,3-28,8 | "Você pode fazer amizade... casar com eles!" | Ponto vira pílula; cursor clica no "+" e empilha pílulas; cor muda por pílula; íris rosa do anel | Beaky pílulas, Open cursor, Zei íris |
| F | 28,5-39,5 | "É sério... sorte!" | Página vira para o palco de papel; bonecos articulados arrastados pelo mouse; Rinnegans, facadas, dado | Animação em Recorte |
| G | 39,1-49,9 | "Além disso... inovadores!" | Mergulho na face do dado; combate com barras de vida; treino com barra; íris azul das missões; clique rola o D20; órbitas de sistemas | Zoom through, Season órbitas, Zei íris |
| H | 49,7-58,5 | "Mas a próxima... Shinobi Synex!" | Ponto vira cursor de texto; "VOCÊ" com zoom radial; chibi acenando; logo repetido com detalhe novo; fica só o símbolo | Cendap editor e zoom, Beaky logo repetido |

## Som
- Música: "Helike [Drum and Bass]", Hardcore Scm (Jamendo, CC BY), a partir de 86,52 s, para a subida cair no "Shinobi" (9,28 s). Volume baixo sob a voz.
- Efeitos CC0 do Freesound: whoosh, impacto, riser, papel, corte, facada, dado, clique, brilho, glitch.

## Estado (05/11/2026)
- Prontos: `assets/lib.js`, `assets/palavras.js`, cenas `a.html` e `b.html`, música e efeitos baixados em `assets/som/orig`.
- Faltam: cenas C a H, `index.html` com as cenas sobrepostas (A 0-7,3; B 7,05-10,95; C 10,7-14,95; D 14,4-22,6; E 22,35-28,75; F 28,55-39,45; G 39,1-49,9; H 49,7-58,5), recorte da música (início 86,52 s, com fades), posições dos efeitos, render e revisão.
- Nada foi renderizado ainda.

## Proibido aqui
- Boca da chibi abrindo e fechando: ela é sempre uma imagem fixa por cena.
- Personagens do sistema fora dos +120.
- Corte seco entre cenas.

## Versão 3 (05/11/2026)
- Arquivo final: `shinobi-synex-filme-v3.mp4` (58,5 s, −14 LUFS, pico −2,4 dB). Há também `shinobi-synex-filme-v3-leve.mp4`, de 23 MB, para o celular.
- Estilo da referência `snapinsta`: uma palavra grande por quadro com troca de fundo nas cenas A, D (conceitos) e H. As outras cenas ganharam faixas de palavras gigantes correndo, raios girando e deriva lenta. A camada `grao.html` põe poeira de película no filme inteiro.
- Conceitos com quatro NPCs mulheres: Kaede Isana (rotina), Karinna Uzumaki, a mítica (personalidade), Yūgao Sarutobi (história) e Sari Kazekage (vida). As imagens estão em `assets/elas/`.
- Som da Mixkit: música "War Cry" e 62 efeitos, catalogados com `tools/mixkit.py`. A música fica abafada no problema (0 a 9,3 s) e na virada final (49,9 a 54,4 s).
- Sobras conhecidas: a música foi escolhida e mixada sem ser ouvida, e o fim (57,3 a 58,5 s) é só o símbolo girando no escuro.
