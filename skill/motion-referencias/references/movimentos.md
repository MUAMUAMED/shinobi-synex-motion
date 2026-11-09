# Catálogo de movimentos

`f` é o frame do vídeo original, a 30 fps. Os trechos abaixo foram vistos quadro a quadro; curvas e valores de animação são estimativas para ajustar olhando o resultado.

## Base

| Movimento | Duração | Curva | Valores |
|---|---|---|---|
| Implosão de saída | 5 a 8 f | `power3.in` | escala 1 → 0,05 |
| Impacto de entrada | 8 a 12 f | `expo.out` | escala 2,3 → 1, blur 22px → 0 |
| Deriva | cena toda | linear | escala 1 → 1,05 ou 1 → 0,95 |
| Palavra | 6 a 8 f | `power2.out` | x +30, y +16, blur 7px → 0 |
| Letra em onda | 12 a 18 f | `back.out` | y 40% → 0, atraso de 1 a 2 f |
| Anel | 15 a 25 f | `power2.out` | escala 0,25 → 1,5, opacidade 1 → 0 |
| Carimbo | 4 f | `back.out(2.4)` | escala 1,4 → 1 |
| Recorte | - | `steps(3 a 6)` | giro de ±4° |

No código: `FX.w`, `FX.hit`, `FX.out`, `FX.ring`, `FX.stamp`, `FX.k`, `FX.pk`.

## Transições

### Tela vira ícone (Open Manager f368-391)
- `f368-371`: a cena azul em tela cheia, com o conteúdo sumindo.
- `f372-376`: cantos arredondam e o retângulo encolhe até uns 40% da largura.
- `f377-379`: nascem círculos claros atrás; o retângulo achata.
- `f380-385`: vira ícone e cresce; a seta aparece.
- `f379-391`: o selo vermelho conta 39 até 85.

### Tela vira cápsula e ponto (GesPat f298-306)
- `f298-299`: mapa ganha cantos arredondados.
- `f300-305`: cápsula encolhe até um ponto.
- `f306-311`: a próxima cena surge por fusão, vinda do branco.

### Painel diagonal com fusão e grade (Cendap f762-785)
- `f762-769`: painel branco diagonal sobe devagar sobre o vermelho.
- `f770-773`: a cena inteira clareia para branco.
- `f774-775`: aparecem guias finas de layout.
- `f776-780`: "Tele" entra letra por letra, com "a" pequeno ao lado.
- `f777-785`: rótulo falso conta de 170 a 269 px, enquanto as guias se ajustam.

### Flash com letra-fantasma e zoom radial (Cendap f818-841)
- `f818-819`: branco.
- `f820`: uma letra gigante e clara pisca.
- `f822-825`: a cena entra com zoom radial forte.
- `f826-832`: encolhe com rebote; a palavra repetida aparece atrás.
- `f833-841`: assenta e cresce devagar.

### Cor funde para branco com ícones (Beaky f244-267)
- `f244-248`: texto e bolinha somem no roxo.
- `f249-252`: o roxo clareia para lilás e branco.
- `f252-260`: ícones enormes e desfocados entram pelas bordas, recuando até o foco.
- `f254-260`: "isso" passa de desfocado a nítido, ao lado de "Tudo".

### Riscos de luz e anel (Zei f304-327)
- `f304-312`: cartões sobem, ganhando blur; riscos verticais finos sobem junto.
- `f312-318`: um anel abre de baixo para o centro, com o risco como coluna de luz.
- `f316-322`: as palavras chegam em alturas diferentes e se alinham.
- `f323-327`: sublinhado se desenha; um ponto orbita.

### Volta do preto em profundidade (Hakuna f176-199)
- `f176-177`: preto.
- `f178-181`: cartões em perspectiva chegam desfocados e descendo.
- `f182-187`: focam; o texto inclinado acompanha o plano.
- `f188-199`: deriva lenta, com objetos de primeiro plano desfocados.

### Produto com chicote e pílulas (Season Cloud f385-408)
- `f385-393`: círculo brilhante do produto balança na borda.
- `f394-399`: a câmera atravessa de um lado a outro, com blur.
- `f398-404`: pílula com brilho entra pela lateral esticada e assenta.
- Durante tudo: faixa de aberração cromática na base.

### Objetos da Voltz
- **Bola → lasca → pílula:** bola sobe em arco, afina até virar lasca, e a pílula abre em `rotationY` de 86° a 0°.
- **Pílula → "+":** inclina até -22°, encolhe e clareia; o "+" nasce no mesmo lugar.
- **Vidro com confete:** escala 0,3 a 1,22, `skewY` de -9° a +7°, com estrela branca no centro e botão mudando de cor.
- **Peça branca girando:** gira como cubo com clarão atrás, troca o conteúdo no meio do giro e achata em `scaleY`.
- **Mosaico e contador:** perto até o número fechar, corte seco para aberto.
- **Digitação gigante:** texto de 300px atrás de uma máscara, com o cursor fixo; o texto corre para a esquerda.
- **Estrobo:** dita a opacidade do escuro por frame (`assets/voltz-composicoes/d.html`).
- **Linha que costura:** traço curvo desenhado sob as palavras, que depois foge e leva à próxima cena.

## Padrões da leitura completa

Vistos ao olhar todos os segundos com mudança dos 8 vídeos. "Onde" cita exemplos, não todas as ocorrências.

### Costuras

| Costura | Como fazer | Onde |
|---|---|---|
| Implosão a um ponto | Cena encolhe em 4 a 8 f; a seguinte entra em até 3 f | GesPat f700-1062, Season f342, f528 |
| Íris abrindo | Círculo nasce dentro da cena e cobre tudo em 5 a 8 f, trazendo a cor nova | Zei f845-851, f886-890; GesPat f17-22 |
| Íris fechando | Disco encolhe até um ponto sobre o fundo novo | Beaky f416-421; Zei f917-924 |
| Mergulho no preto | 1 a 4 f de preto entre ideias, com a cena seguinte nascendo de um borrão | Hakuna inteiro; Season inteiro |
| Fusão de cor | Fundo muda em 4 a 10 f, com elementos entrando juntos | Cendap f51-54; Zei f254-258 |
| Painel diagonal | Bloco sobe inclinado em degraus; pode empilhar um segundo | Open f183-194, f815-830; GesPat f885-930 |
| Linha de chão | Cenário achata numa linha e o próximo nasce dela | GesPat f174-229 |
| Apagador | Mancha ou risco grosso varre a cena | Cendap f383, f672; Zei f369-381 |
| Glitch de blocos | Faixas brancas e pretas em posições soltas, 3 a 4 f, antes de um flash total | Voltz f615-618, f732-735, f798-801 |
| Riscos verticais | Imagem se desfaz em listras, 2 a 4 f | GesPat f643, f667; Hakuna f174; Season f371 |
| Estrobo de saída | Cena pisca com preto em intervalos cada vez maiores | Season f683-700; Voltz f271-290 |

### Um objeto vira outro

O padrão mais comum nos 8 vídeos. O fim da cena é uma forma simples, que inspira a próxima.

- **Pílula → cartão → tela:** alarga e abre (Beaky f666-705; Cendap f413; Open f293-321; Hakuna f494-520).
- **Campo → quadrado → anel de carregamento:** Open f614-630; Zei f541-554.
- **Tela inteira → ícone ou marcador:** Open f372-391; Zei f72-90; Cendap f262-268.
- **Risco → ícone:** relógio, ticket, check (Cendap f472, f517, f855).
- **Bolinha → pontuação ou seta:** Cendap f268-284; Zei f56-71; Beaky f176-200.
- **Logo → risco ou letra achatada:** Open f116-125, f950-960; Season f122-130.
- **Forma distorcida → cartão:** estrela que incha (Zei f436-449); vidro que se contorce (Voltz f488-497).

### Cursor e mão

- A mão causa a próxima coisa; ela não decora. Clicou, muda (Cendap f442; Open f293-312; Zei f241-253).
- Mão grande, com contorno e sombra, puxa painéis (Open f183) ou atravessa a tela trazendo texto (Zei f405; Cendap f1229).
- Clique marcado pelo item piscando (Open f97-108).
- Em neon, a mão é uma silhueta de luz (Season f45-54).

### Interface viva

- Contadores, deslizadores e interruptores movem durante a fala (Zei f476-503; Open f293-312).
- Texto embaralhado que se resolve (GesPat f510-525; Open f570-580).
- Terminal falso: "Analisando dados" com linhas correndo (Open f630-650).
- Falso editor de vídeo: rótulo de pixels, grade, caixa de seleção (Cendap f776-816).

### Cor

- Vermelho conta o problema e a cor da marca, a solução, na mesma coreografia (Season inteiro; Beaky f20-44).
- Cor de fundo por assunto, com preto no resto (Voltz).
- Brilho nasce quente e esfria durante a cena (Hakuna f305-345).

### Repetição

- Três benefícios na mesma coreografia, trocando texto, ícone e cor do raio (Hakuna f673-766; Voltz f184-222).
- Logo reaproveitado no fim com um detalhe novo (Beaky f281 e f1029; Season f122 e f1022; Zei f110 e f953).

### Abertura

Comum: começar do preto ou do branco e já ter algo em movimento até o frame 3. Exemplos: palavra enorme encolhendo (Open f1-8), contorno se desenhando (Beaky f1-22), objeto desfocado que recua (GesPat f1-8; Cendap f1-8).

## Texto

- **Palavra quebrada:** "Res/posta", "Velo/cidade", "Auto/maticamente", com a primeira parte maior.
- **Duas vozes:** palavra leve junto de outra pesada ("Um **ERP**").
- **Sublinhado desenhado:** risco à mão sob a palavra-chave.
- **Palavra repetida ao fundo:** "DIFERENCIAL" empilhado e clarinho.
- **Ponto final:** a palavra acaba e sobra "..", que vira a próxima cena.

## Encerramento

Comum à maioria dos vídeos, nesta ordem, com cerca de 2 a 3 s em cada passo (Voltz e Hakuna não mostram site):
1. Logo com impacto ou letra por letra, às vezes com anéis.
2. Slogan pequeno entrando sob o logo.
3. Site ou chamada em texto pequeno.
4. Ícone sozinho, sumindo por fusão.

Os vídeos de agência têm cerca de 5 a 8 s finais quase parados e até silenciosos. Em anúncio de verdade, normalmente vale encurtar.
