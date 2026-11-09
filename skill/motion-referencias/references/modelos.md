# Os 5 modelos de edição

Números medidos em todos os 9.804 frames das 8 referências. "Cortes por minuto" conta só trocas bruscas, por isso os vídeos contínuos ficam baixos.

## Como decidir

| Pergunta | Resposta | Modelo |
|---|---|---|
| Fundo escuro com brilho forte em uma cor? | Sim | Neon escuro |
| Fundo escuro, com objetos 3D que viram outros objetos e cor mudando por cena? | Sim | Imersivo de objetos |
| Fundo branco e tudo emenda sem corte? | Sim | Branco contínuo |
| Telas inteiras de cor, tipografia gigante e cortes secos? | Sim | Bloco de cor |
| Papel, mão ou mouse arrastando figuras em movimento picado? | Sim | Recorte |

## Branco contínuo

- **Referências:** Beaky, Open Manager, Zei.
- **Números:** brilho 227 a 238; cena mediana de 1,6 a 3,1 s; 12 a 23 cortes por minuto.
- **Sensação:** calmo e organizado, um produto explicado sem pressa.
- **Fundo:** branco ou cinza claríssimo, com círculos enormes translúcidos e blur suave.
- **Cor:** uma da marca, às vezes em tela cheia como respiro.
- **Elementos:** telas de produto limpas, pílulas empilhadas, ícones de apps com blur de profundidade, anéis finos, cursor.
- **Transição típica:** cartão em tela cheia vira ícone; cor funde para branco enquanto os elementos entram.
- **Use para:** SaaS, app, ferramenta, educação.
- **Variação:** Zei é o mais híbrido, com painéis azuis e íris frequentes. Por isso cai perto de Bloco de cor nos números.

## Bloco de cor

- **Referências:** Cendap, GesPat.
- **Números:** brilho 222 a 228; cena mediana de 0,55 a 0,77 s; 33 a 34 cortes por minuto. É o mais rápido entre os claros.
- **Sensação:** enérgico e direto, com cara de anúncio.
- **Fundo:** alterna branco e cor cheia, com painéis diagonais.
- **Tipografia:** gigante e cortada pela tela ("pre/cisa", "Tele/Medicina"), palavra repetida ao fundo, grade de layout com rótulo falso de pixels.
- **Elementos:** mão de desenho clicando, ilustrações chapadas (GesPat), objetos 3D recortados, celular na mão.
- **Transição típica:** painel empurra a cena; flash branco com letra-fantasma e zoom radial.
- **Use para:** saúde, governo, serviços, oferta com benefício claro.

## Neon escuro

- **Referências:** Hakuna, Season Cloud.
- **Números:** brilho 29 a 31; cena mediana de 0,83 a 1,19 s; 39 a 44 cortes por minuto; 11 a 15 mergulhos no preto.
- **Sensação:** gamer e tecnológica.
- **Fundo:** preto com uma cor neon (magenta, violeta). Vermelho só para o problema.
- **Texto:** branco com halo forte.
- **Elementos:** catálogo em perspectiva com primeiro plano desfocado, flash horizontal, grade, anéis, aberração cromática nas bordas.
- **Transição típica:** sai para o preto por 2 a 4 frames e volta do escuro, desfocado.
- **Use para:** games, hospedagem, loja digital.

## Imersivo de objetos

- **Referência:** Voltz.
- **Números:** brilho 32; cena mediana de 0,97 s; 37 cortes por minuto; 6 flashes e 14 mergulhos no preto.
- **Sensação:** cada frase é um brinquedo que se transforma.
- **Fundo:** preto, mudando para tela cheia de cor (azul, rosa, roxo, laranja) em momentos específicos.
- **Texto:** pequeno, centralizado, palavra por palavra.
- **Elementos:** bola vira pílula, que vira "+", que vira cartão de vidro; confete em fitinhas; raios; contador; digitação gigante com cursor.
- **Transição típica:** objeto gira em 3D, achata e dá lugar ao próximo.
- **Use para:** comunidade, Discord, entretenimento, lançamentos.
- **Base pronta:** `assets/voltz-composicoes/`.

## Recorte

- **Referência:** vídeo "Animação em Recorte" (Muller Junio), 16,7 s.
- **Números:** 12 fps e uma tomada só, sem nenhum corte; câmera parada. O efeito vem da taxa baixa, então renderize esse trecho com poses de 2 a 3 frames.
- **Sensação:** feito à mão, cômico.
- **Fundo:** folha clara sobre escuro, com cantos de papel vermelhos.
- **Movimento:** picado (`steps(n)` no GSAP), pequenos giros, figuras com borda branca, mão ou mouse visível.
- **Use para:** piadas e cenas narrativas curtas dentro de outro modelo.
