# evoluafit-anatomy-pack

Biblioteca de imagens anatômicas 3D (frente e costas) do app EvoluaFit AI. Contém **apenas** imagens, mapas musculares por exercício, camadas intermediárias, scripts de geração e licenças. Sem dados pessoais, histórico de treino ou credenciais.

## Versões
Cada pacote fica em `packs/<versão>/` e **nunca é modificado depois de publicado**. Use URLs com **commit** fixo (SHA completo de 40 caracteres; não use `main`):

```
https://raw.githubusercontent.com/dudulimavasc84/evoluafit-anatomy-pack/<commit-sha>/packs/v1.0.0/manifest.json
```

Um pacote contém `manifest.json` (md5/sha256, tamanho e dimensões de cada imagem), `exercises.json` (mapa muscular por exercício, status de identificação e de anatomia), `SHA256SUMS` e `images/*.webp` (392×977).

## Reproduzir
```
pip install pillow
python3 pipeline/compose.py --version v1.0.0     # recompõe imagens a partir de layers/
```
Para regerar as camadas 3D (`pipeline/render/`), veja `pipeline/SOURCES.md`.

## Licença
CC BY-SA 4.0 — veja `ATTRIBUTION.md`, `CHANGES.md` e `LICENSE-CC-BY-SA-4.0.txt`. BodyParts3D: CC BY 4.0. Z-Anatomy: CC BY-SA 4.0.
