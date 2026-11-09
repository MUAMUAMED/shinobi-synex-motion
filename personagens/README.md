# Personagens do Shinobi Synex

Imagens dos 125 NPCs do jogo, convertidas para JPG (os rostos ficam em WebP) para caber no repositório.

| Pasta | O que tem |
|---|---|
| `cartoes/` | Cartão 16:9 de cada NPC, com o personagem no cenário (1672x941) |
| `fichas-visuais/` | Folha de personagem: corpo de frente, de lado e de costas, 6 expressões, close dos olhos e itens. Boa para recortar expressões e olhos |
| `retratos/` | Retratos avulsos que ficam na raiz `assets/npcs/` do jogo |
| `rostos/` | `face_<chave>.webp` e `<chave>.webp` (512x512): rosto e busto |
| `kunoichis/` | As NPCs mulheres, pelo nome (1024x1536) |
| `indice.json` | Para cada chave: nome, grupo (vila), idade, aniversário, papel, de qual obra o rosto foi recriado e os caminhos das imagens |

O nome do arquivo é a chave interna do NPC, que nem sempre bate com o nome dele. Por exemplo, `mito_no_ch_wa` é a Karinna Uzumaki. Use `indice.json` para traduzir.

Regras usadas no vídeo:
- Personagens só aparecem quando o assunto são os NPCs.
- As imagens das kunoichis são sensuais: nos closes use o rosto, as expressões e os olhos da folha, nunca o corpo.
