# O estilo em números

As regras completas estão em `skill/motion-referencias/references/`:
- `modelos.md`: os 5 modelos de edição.
- `movimentos.md`: catálogo de transições com os quadros medidos.
- `fichas.md`: uma ficha por referência.
- `preferencias.md`: o que a pessoa aprova.

Abaixo está o resumo do que foi aplicado no vídeo aprovado.

## Ritmo
- **Narração:** cerca de 2,7 palavras por segundo, falada rápido.
- **Palavras-relâmpago:** nos trechos de impacto (problema, conceitos, final), cada palavra é um quadro de 0,25 a 0,9 s, e o ritmo acelera junto com a fala.
- **Entrada de palavra:** chega 14% a 40% maior e desfocada (8 px) e assenta em 0,12 a 0,13 s com `expo.out`.
- **Ritmo de 3 tempos:** impacto em 2 a 4 quadros, assentamento em 6 a 10 quadros e deriva lenta até o fim. Nada fica parado: escala de 1 para 1,05 a 1,12, mais uma leve rotação.

## Cor
| Uso | Cor |
|---|---|
| Noite (fundo escuro) | `#0b0a10` |
| Papel (fundo claro) | `#f2efe8` |
| Laranja Synex (marca) | `#ff5a1f` |
| Vermelho, só no problema | `#ff2b3a` |
| Azul rotina e missões | `#1f4fd6` |
| Verde vida e amizade | `#2f9e44` / `#13a862` |
| Violeta jutsus | `#6a3df0` |
| Rosa casamento | `#ff4f8b` |

- **Alternância:** a cada palavra o fundo troca entre claro, escuro e a cor do assunto, com corte seco.
- **Vermelho e laranja:** o vermelho só aparece no problema. A marca, em laranja, entra quando o logo aparece.

## Tipografia
- **Fonte:** Outfit, 800 a 900, com espaçamento de letras −0,045em nas palavras gigantes.
- **Palavra gigante:** de 240 a 420 px. A palavra pequena empilhada em cima tem 110 a 120 px ("tá todo / MUNDO").
- **Fundo:** faixas de palavras gigantes em contorno (`-webkit-text-stroke`, 15% a 40% de opacidade) correm em sentidos opostos.

## Transições usadas (cena → cena)
| De → para | Como |
|---|---|
| Problema → solução | Tudo implode num ponto vermelho, que vira laranja no "Mas" |
| Ponto → logo | O ponto foge da multidão cinza, cresce e explode em tinta laranja. O logo entra com anéis, confete e raios girando |
| Logo → mecânicas | Íris noturna saindo do símbolo; o shuriken vira engrenagem |
| Gameplays → NPCs | A engrenagem cresce e a parede de NPCs abre pelo furo dela |
| Conceitos → relações | Tudo implode num ponto, e o ponto vira a primeira pílula (`clip-path inset`) |
| Casamento → história | A página vira (`rotationY`) para o palco de papel |
| Dado → sistemas | Zoom através da face do dado |
| Sistemas → final | Colapsam num ponto, e o ponto abre a primeira palavra em íris |
| Final | Tinta laranja, logo com giro duplo, anéis e confete, e por fim só o símbolo |

## Elementos
- **Ícones:** game-icons.net, em silhueta na cor do tema. Emoji nunca: dá cara de IA.
- **Bonecos de palito:** no estilo "Animator vs Animation", a 12 quadros por segundo e arrastados por um cursor (`compositions/f.html`).
- **Personagens do jogo:** só nos +120 NPCs. Nos conceitos entram só os rostos e expressões das NPCs mulheres (`filme/assets/elas/`), sempre com um dado real da ficha delas.
- **Chibi:** imagem fixa, uma expressão por cena, com balanço leve.
- **Poeira de película:** por cima de tudo (`compositions/grao.html`).
