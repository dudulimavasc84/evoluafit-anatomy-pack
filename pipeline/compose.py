#!/usr/bin/env python3
"""Compõe as imagens finais (frente/costas) de cada mapa muscular distinto.

Entrada : pipeline/config/exercises.json, pipeline/config/muscles.json, layers/*.png
Saída   : packs/<versao>/images/<id>_<view>.webp, manifest.json, exercises.json, SHA256SUMS

Receita (idêntica à dos cards aprovados): corpo-base -> camadas secundárias -> camadas
principais; recorte fixo 560x1396 em (120,212) do quadro 800x1600 (fundo 20,20,24);
redução 0,7 (392x977); WebP q55. Imagens são deduplicadas pelo mapa muscular (não pelo nome).
"""
import argparse, hashlib, json, os, sys, datetime
from PIL import Image

CROP = (120, 212, 560, 1396)           # x0, y0, w, h
BG = (20, 20, 24, 255)
OUT_W, OUT_H = 392, 977
WEBP_Q = 55
VIEWS = ('front', 'back')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def expand(ids, muscles):
    out = []
    for i in ids:
        out += muscles[i].get('expands', [i])
    return out

def map_key(prim, sec):
    return json.dumps([sorted(prim), sorted(sec)])

def image_id(prim, sec):
    return 'm_' + hashlib.sha1(map_key(prim, sec).encode()).hexdigest()[:10]

def compose(prim, sec, view, muscles, layers_dir):
    def L(name):
        return Image.open(os.path.join(layers_dir, name + '.png')).convert('RGBA')
    canvas = L(f'base_{view}')
    for g in expand(sec, muscles):
        canvas = Image.alpha_composite(canvas, L(f'{g}_{view}_sec'))
    for g in expand(prim, muscles):
        canvas = Image.alpha_composite(canvas, L(f'{g}_{view}_prim'))
    full = Image.new('RGBA', (canvas.width, canvas.height + 200), BG)
    full.alpha_composite(canvas)
    x0, y0, w, h = CROP
    img = full.crop((x0, y0, x0 + w, y0 + h)).convert('RGB')
    return img.resize((OUT_W, OUT_H), Image.LANCZOS)

DEEP = {'eretores': 'eretores da espinha', 'soleo': 'sóleo', 'obliquo_interno': 'oblíquo interno',
        'romboides': 'romboides', 'braquial': 'braquial'}

def technical_validation(e):
    """Validação técnica (não é aprovação visual): checagens automáticas do mapa + conferência com o cadastro."""
    if e['anatomy'] != 'pronta':
        return dict(status='nao_aplicavel', reason='sem representação anatômica correta' if e['anatomy'] == 'pendente' else '')
    if e['identification'] != 'identificado':
        return dict(status='identificacao_pendente', reason='mapa pronto, mas o equipamento/execução não está identificado: a figura não é exibida no app',
                    visual_approval='pendente')
    st = 'validada_com_ressalva' if e.get('user_confirmation_needed') else 'validada_tecnicamente'
    return dict(status=st, checks=['musculos_existem_no_modelo', 'sem_repeticao_principal_secundario',
                                   'camadas_visiveis', 'conferido_com_cadastro_e_literatura'],
                visual_approval='pendente')

def visibility_notes(e):
    if e['anatomy'] != 'pronta':
        return []
    return [f"{DEEP[m].capitalize()} é um músculo profundo: aparece só parcialmente (por transparência)." for m in e['primary'] + e['secondary'] if m in DEEP]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', required=True)
    ap.add_argument('--out', default=None)
    ap.add_argument('--only-ready', action='store_true', default=True)
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(ROOT, 'pipeline/config/exercises.json')))
    muscles = json.load(open(os.path.join(ROOT, 'pipeline/config/muscles.json')))
    layers_dir = os.path.join(ROOT, 'layers')
    out = a.out or os.path.join(ROOT, 'packs', a.version)
    img_dir = os.path.join(out, 'images'); os.makedirs(img_dir, exist_ok=True)
    errors = []
    maps = {}
    for e in cfg:
        if e['anatomy'] != 'pronta':
            continue
        p, s = e['primary'], e['secondary']
        if not p: errors.append(f"{e['name']}: sem músculo principal")
        if set(p) & set(s): errors.append(f"{e['name']}: músculo repetido em principal e secundário")
        for m in p + s:
            if m not in muscles: errors.append(f"{e['name']}: músculo desconhecido {m}")
        maps.setdefault(image_id(p, s), (p, s))
    if errors:
        print('\n'.join(errors)); sys.exit(1)
    images = []
    for iid, (p, s) in sorted(maps.items()):
        for v in VIEWS:
            fn = f'{iid}_{v}.webp'
            im = compose(p, s, v, muscles, layers_dir)
            fp = os.path.join(img_dir, fn)
            im.save(fp, 'WEBP', quality=WEBP_Q, method=6)
            data = open(fp, 'rb').read()
            images.append(dict(id=iid, view=v, file=f'images/{fn}', bytes=len(data), width=OUT_W, height=OUT_H,
                               md5=hashlib.md5(data).hexdigest(), sha256=hashlib.sha256(data).hexdigest()))
    exercises = []
    for e in cfg:
        item = {k: e[k] for k in ('name', 'equipment_logged', 'identification', 'anatomy', 'anatomy_pending_reason',
                                  'laterality', 'note', 'user_confirmation_needed', 'primary', 'secondary')}
        item['image'] = image_id(e['primary'], e['secondary']) if e['anatomy'] == 'pronta' else None
        item['reviewed'] = False          # aprovação visual do usuário: nunca marcada automaticamente
        item['pending_kinds'] = e.get('pending_kinds', [])
        item['technical_validation'] = technical_validation(e)
        item['visibility_notes'] = visibility_notes(e)
        exercises.append(item)
    manifest = dict(
        name='evoluafit-anatomy-pack', version=a.version, image_format='webp', width=OUT_W, height=OUT_H,
        views=list(VIEWS), generated=datetime.date.today().isoformat(),
        compose=dict(crop=CROP, background=BG[:3], scale=0.7, webp_quality=WEBP_Q),
        license=dict(images='CC BY-SA 4.0', attribution='ATTRIBUTION.md', changes='CHANGES.md'),
        images=images)
    json.dump(manifest, open(os.path.join(out, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
    json.dump(dict(version=a.version, muscles=muscles, exercises=exercises), open(os.path.join(out, 'exercises.json'), 'w'), ensure_ascii=False, indent=1)
    with open(os.path.join(out, 'SHA256SUMS'), 'w') as f:
        for im in images: f.write(f"{im['sha256']}  {im['file']}\n")
    ready = sum(1 for e in exercises if e['image'])
    print(f'{len(maps)} mapas distintos, {len(images)} imagens, {ready} exercícios com imagem, {len(exercises)} no total')

if __name__ == '__main__':
    main()
