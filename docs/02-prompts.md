# Prompts

## Roteiro (copy) usado em todas as versões
> Sério... Tá todo mundo cansado daqueles RPs genéricos de Naruto, são sempre as mesmas coisas e nenhuma inovação! Mas foi fugindo dessa moda que surgiu o Shinobi Synex! Inspirado nas mecânicas de Red Dead Redemption e Kingdom Come Deliverance, o Shinobi Synex conta com mais de cento e vinte NPCs com rotinas, personalidades, histórias e vidas completamente diferentes! Você pode fazer amizade com eles, aprender Jutsus, receber poderes e até mesmo se casar com eles! É sério, você pode em um dia aleatório estar andando no meio da floresta e um homem misterioso aparecer e te dar dois Rinnegans! Ou duas facadas, depende muito da sua sorte! Além disso, Synex possui um combate dinâmico, treinos que realmente te desafiam, missões que funcionam exatamente como um RPG de mesa e vários outros sistemas inovadores! Mas a próxima inovação será você que vai fazer nessa história, seja bem-vindo ao Shinobi Synex!

São 149 palavras e 55,7 s de fala. O tempo de cada palavra está em [`voz/aw1.json`](../voz/aw1.json).

## Pedido à ElevenLabs (voz aprovada)
```json
POST https://api.elevenlabs.io/v1/text-to-speech/xeY9slKb5XBrj6sLUV4S/with-timestamps?output_format=mp3_44100_128
{
  "text": "[fast-paced] Sério... Tá todo mundo cansado daqueles RPs genéricos de Naruto, ... seja bem-vindo ao Shinobi Synex!",
  "model_id": "eleven_v4",
  "voice_settings": { "stability": 0.52, "similarity_boost": 0.75 }
}
```
Observações:
- Escreva "cento e vinte" por extenso e use "RPs" em vez de "Roleplays".
- As tags de emoção (`[fast-paced]`, `[excited]` etc.) só funcionam no v3 e no v4.
- Para mais velocidade, `eleven_multilingual_v2` com `speed: 1.2` chegou a 3,1 palavras por segundo, mas a voz aprovada é a do v4.

## Pedidos da pessoa, em ordem
Estes são os pedidos que moldaram o estilo, palavra por palavra. Eles valem como prompt para os próximos vídeos.

1. "Quero fazer vídeos iguais esses da referência, quero demais usar todo esse estilo, e o ponto principal é porque tem que analisar todos os frames de 1 segundo pra entender as transições."
2. "Tenta recriar os 30 segundos do que é do Discord (Voltz) pra eu ver, faça de forma que fique o mais igual."
3. Roteiro do Shinobi Synex:
   - tela dividida com gameplay de Red Dead e Kingdom Come;
   - cartões dos NPCs atrás da apresentadora;
   - animação de recorte arrastada pelo mouse;
   - chibi como apresentadora;
   - estilo da Voltz, mas 16:9 (1920x1080).
4. "Eu não curti... tenta refazer o vídeo do Voltz mas com o nosso estilo e tudo que temos."
5. "As imagens [dos personagens] só aparecem quando estamos falando dos +120. O restante você deve criar ou usar PNGs da internet. O áudio do Voltz é falado rápido."
6. "Destrinche todas as referências frame por frame, crie padrões, ferramentas, skills... uma skill que vai receber essa referência e vai saber que eu quero uma edição mais ou menos nesse estilo."
7. "Pare de usar esse vídeo base. Crie um completo com tudo que você tem de referência, usando efeitos sonoros, música... pode usar a chibi mas não faça ela movendo a boca, apenas uma imagem dela. Faça o melhor motion design com muita conexão entre frame por frame e nas transições."
8. Ajustes seguintes:
   - "você está usando elementos de emojis, e eu não curto... explora uma biblioteca Shinobi de elementos" (vira cara de edição por IA);
   - em histórias e personalidades, ilustre o conceito e não mostre só o personagem;
   - dos 120 NPCs, use só os recriados de outras obras e animes;
   - na história das facadas e dos Rinnegans, use bonecos de palito.
9. Último pedido:
   - nos conceitos, só NPCs mulheres: Karinna Uzumaki (a mítica), Kaede Isana, Yūgao Sarutobi e mais uma à escolha;
   - "motion design mais movimentado e mais chamativo, em todo frame tendo um movimento";
   - a referência de tipografia com textos grandes trocando e o fundo mudando de cor;
   - uma biblioteca gratuita nova de música e efeitos.

## Prompt sugerido para a próxima IA
> Leia o README deste repositório, depois `docs/01-como-fazer-um-video.md`, `docs/03-estilo.md` e `skill/motion-referencias/references/preferencias.md`. Faça um vídeo promocional de [PRODUTO] em 16:9, 1920x1080, com o roteiro [COPY], no mesmo estilo do `video/shinobi-synex-filme-v3.mp4`:
> - gere a voz primeiro e use o tempo de cada palavra como relógio;
> - uma palavra grande por quadro nos trechos de impacto, com o fundo alternando;
> - cenas ligadas por íris, tinta, corte ou ponto que atravessa;
> - movimento em todo quadro;
> - ícones do game-icons.net no lugar de emoji;
> - música e efeitos da Mixkit, cada efeito no pico da ação;
> - revise com folhas de quadros antes de entregar.
>
> Reaproveite `filme/assets/lib.js`, `compositions/grao.html` e `tools/montar.py`.
