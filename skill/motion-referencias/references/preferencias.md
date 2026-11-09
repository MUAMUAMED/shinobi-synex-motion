# Preferências dadas pela pessoa

Valem para vídeos futuros, salvo pedido diferente. Inclua correções novas aqui.

## Fidelidade
- Quando pedir "igual" ou "no estilo de X", reaproveite a coreografia real de X. Uma leitura livre dele foi recusada ("não curti"); a versão com os keyframes da Voltz foi a base aceita para os ajustes seguintes.
- Prefere estudar as referências frame a frame, com ênfase nas transições.

- Pedido de 05/11/2026: parar de usar a base da Voltz em tudo. Para um filme novo, combine técnicas de todas as referências, com música e efeitos, e muita conexão entre as cenas.

## Chibi (narradora)
- Use imagem fixa, sem alternar boca aberta e fechada. Pode trocar de expressão entre cenas, uma imagem por cena.

## Imagens
- Não use imagens internas do sistema em todas as cenas. Personagens do Shinobi Synex aparecem só onde o assunto são eles, como nos "+120 NPCs".
- No resto, crie os elementos ou use uma biblioteca de ícones temática.
- Não use emoji (nem os 3D do Fluent): a pessoa acha que dá cara de edição por IA. O que entrou no lugar: game-icons.net (CC BY 3.0, crédito obrigatório), com ícones de ninja, shuriken, pergaminho e katana, em silhueta na cor do tema. Script: `assets/filme-exemplo/icones.py` e `L.icones()`.
- Parede de NPCs do Shinobi Synex: só os NPCs recriados de outras obras e animes, listados em `assets/data/npc-face-references.json` e `npc-user-references.json` do projeto. A leitura foi que "só elas" se referia a esses; confirme se o pedido mudar.
- Ao falar de rotinas, personalidades, histórias e vidas, não mostre só o personagem: mostre o conceito com dados reais do NPC (rotina por horário, fala, trecho da história, idade e profissão).
- Histórias cômicas, como a dos Rinnegans e das facadas, ficam melhores com bonecos de palito arrastados pelo cursor, no estilo "Animator vs Animation".
- Pedido de 05/11/2026: em rotinas, personalidades, histórias e vidas, mostre só NPCs mulheres. Ela citou Karinna Uzumaki (a "mítica", tier MYTHIC), Kaede Isana e Yūgao Sarutobi, e deixou a quarta à escolha (foi a Sari Kazekage). As imagens delas são sensuais: use o rosto (`npcs/avatars/face_*.webp`, cortado no topo) e as expressões e olhos da folha `npcs/sheets/<chave>.png`, nunca o corpo.

## Ritmo e movimento
- Pedido de 05/11/2026: motion mais movimentado e chamativo, com movimento e algo que chame atenção em todo quadro.
- Referência aprovada por ela: vídeo de tipografia (pasta `analise/snapinsta`). Uma palavra grande por quadro, o fundo alterna preto, claro e cor a cada palavra, e o ritmo acelera de 0,7 s para 0,25 s por palavra. A palavra chega cerca de 14% maior e desfocada e assenta em 3 a 4 quadros, e há poeira de película por cima. Na biblioteca isso é `L.batida`, `L.pop` e `L.ecos`, mais a camada `grao.html`.
- Nada fica parado: use deriva lenta (`L.vivo`), faixas de palavras gigantes em contorno correndo no fundo e raios girando atrás de logo e chibi.

## Som
- Pedido de 05/11/2026: ela não gostou da música e dos efeitos tirados do Jamendo e do Freesound. A biblioteca nova é a Mixkit (mixkit.co): é grátis, permite uso comercial e não exige crédito. Use `assets/filme-exemplo/mixkit.py` (catálogo com pausas, porque o site responde 429 a pedidos seguidos).
- A música é escolhida sem ouvir. Meça a energia por meio segundo e a grade de batidas, e prefira faixas com energia constante. Abafe a música com passa-baixa no problema e na virada final, e abra tudo no logo.

## Voz
- Locução rápida, no ritmo do Voltz. A narração pausada e a voz inicial não agradaram.
- Na ElevenLabs, o que deu mais velocidade até agora: `eleven_multilingual_v2` com `speed` 1.2 (3,1 palavras por segundo). `eleven_v3` e `eleven_v4` com o mesmo ajuste ficaram em 2,5 a 2,6.
- As tags de emoção são recurso do v3/v4 e não servem no v2.
- Voz aprovada pela pessoa em amostra: `aw1` (`xeY9slKb5XBrj6sLUV4S`), modelo `eleven_v4`, estabilidade 0,52, similaridade 0,75, com `[fast-paced]` no início do texto. Rende 2,7 palavras por segundo. A aprovação foi da amostra, de um trecho de 28 palavras, não da narração inteira.
- A pessoa testa vozes por conta própria no site. Pergunte se a voz continua a mesma antes de refazer o vídeo.
- Prefere "RPs" a "Roleplays" no texto falado.
- Nunca peça para colar chave no chat; use um arquivo `.env`.

## Cor
- Vermelho só no problema, e a cor da marca entra quando a marca aparece. Usado na versão 4 do Shinobi Synex a partir do estudo das referências; ainda sem retorno da pessoa.

## Formato
- O vídeo do Shinobi Synex é 16:9, 1920x1080. As referências são verticais, então adapte a composição em vez de só cortar.

## Comunicação
- Responda em português do Brasil.
- Diga o que foi só medido e o que foi visto. O áudio nunca é ouvido, apenas medido.
