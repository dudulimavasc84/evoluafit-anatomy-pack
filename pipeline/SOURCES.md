# Fontes dos modelos (não incluídos neste repositório pelo tamanho)

- BodyParts3D 4.0 (OBJ + `isa_element_parts.txt`): https://lifesciencedb.jp/bp3d/ (arquivo `isa_BP3D_4.0_obj_99.zip`).
- Z-Anatomy muscular: https://github.com/mhaney93/body-atlas (`public/models/muscular.glb`), origem https://www.z-anatomy.com/
- three.js 0.160 (`npm i three@0.160`), Chromium/Playwright com SwiftShader para renderização sem GPU.

Ordem: `pipeline/prep/prep_bodyparts3d_v1.py` → `_v2.py` → `_v3.py` (gera `glb/`), depois `node pipeline/render/bulk.mjs "$(cat pipeline/render/jobs_v1.json)"` e `jobs_v2.json` (+ `jobs_v2_fix.json`). Os PNG resultantes são os de `layers/`.
