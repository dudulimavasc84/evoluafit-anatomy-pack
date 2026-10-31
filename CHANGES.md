# Alterações feitas nos modelos de origem

Cadeia de processamento (reproduzível, ver `pipeline/`):
1. **Conversão** dos OBJ do BodyParts3D 4.0 em GLB, agrupados por músculo (`pipeline/prep/*.py`); unidade mm → m.
2. **Z-Anatomy**: seleção das malhas grande dorsal, reto abdominal, oblíquo interno e eretores da espinha; rotação de eixos (Y-up → Z-up) e deslocamento medido para alinhar ao BodyParts3D (`pipeline/render/bulk.html`).
3. **Cabeça procedural** própria.
4. **Renderização** com three.js, câmera ortográfica, frente e costas, 800×1600 px, uma camada por músculo e por função (principal laranja `#ff7a1a`, secundário `#c9966a`), corpo-base cinza `#b9bcc4`. Músculos profundos são exibidos "através" dos superficiais (oclusores ocultados), conforme `GHOST_OCCLUDERS`.
5. **Composição** (`pipeline/compose.py`): corpo-base + camadas secundárias + camadas principais; recorte 560×1396; fundo `#141418`; redução para 392×977; WebP qualidade 55.
6. Camadas intermediárias (PNG RGBA) em `layers/`.

Limitações conhecidas: o vasto intermédio e músculos profundos (supraespinhal, subescapular, transverso do abdome, iliopsoas) não têm camada própria; a porção clavicular/esternocostal do peitoral não é destacada separadamente.
