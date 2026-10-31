import collections,re,numpy as np,trimesh,os,json
el=collections.defaultdict(list); nm={}; rev=collections.defaultdict(list)
for l in open('isa_element_parts.txt'):
    p=l.rstrip('\n').split('\t')
    if p[0].startswith('FMA'): el[p[0]].append(p[2]); nm[p[0]]=p[1]; rev[p[2]].append(p[0])
muscle=set(el['FMA5022']); bone=set(el.get('FMA5018',[]))
print('muscle',len(muscle),'bone',len(bone))
RULES=[ # (grupo, regex sobre nome do conceito)
 ('peitoral', r'pectoralis major'),
 ('deltoide_anterior', r'clavicular part of (left |right )?deltoid'),
 ('deltoide_lateral', r'acromial part of (left |right )?deltoid'),
 ('deltoide_posterior', r'spinal part of (left |right )?deltoid'),
 ('triceps', r'triceps brachii'),
 ('biceps', r'biceps brachii'),
 ('braquial', r'^(left |right )?brachialis$'),
 ('braquiorradial', r'brachioradialis'),
 ('antebraco', r'extensor carpi|flexor carpi|extensor digitorum$|flexor digitorum (superficialis|profundus)|pronator|palmaris'),
 ('trapezio_superior', r'descending part of'),
 ('trapezio_medio', r'transverse part of'),
 ('trapezio_inferior', r'ascending part of'),
 ('romboides', r'rhomboid'),
 ('infraespinhal', r'infraspinatus'),
 ('redondo_maior', r'teres major'),
 ('redondo_menor', r'teres minor'),
 ('serratil', r'serratus anterior'),
 ('obliquos', r'external oblique'),
 ('gluteo_maximo', r'gluteus maximus'),
 ('gluteo_medio', r'gluteus medius|gluteus minimus'),
 ('reto_femoral', r'rectus femoris'),
 ('vasto_lateral', r'vastus lateralis'),
 ('vasto_medial', r'vastus medialis'),
 ('adutores', r'adductor|gracilis|pectineus'),
 ('isquiotibiais', r'semitendinosus|semimembranosus|biceps femoris'),
 ('panturrilha', r'gastrocnemius|soleus'),
 ('tibial', r'tibialis anterior'),
]
def group(fj):
    names=[nm[c] for c in rev[fj]]
    for g,rx in RULES:
        if any(re.search(rx,n) for n in names): return g
    return 'musculo_outro' if fj in muscle else ('osso' if fj in bone else None)

G=collections.defaultdict(list)
for fj in set(list(muscle)+list(bone)+list(rev.keys())): 
    g=group(fj)
    if g: G[g].append(fj)
for g,v in G.items(): print(g,len(v))
os.makedirs('glb',exist_ok=True)
ONLY={'braquiorradial','antebraco','infraespinhal','redondo_maior','redondo_menor'}
for g,fjs in G.items():
    if g not in ONLY: continue
    meshes=[]
    for fj in fjs:
        try:
            m=trimesh.load(f'obj/isa_BP3D_4.0_obj_99/{fj}.obj',force='mesh',process=False)
            meshes.append(m)
        except Exception as e: print('skip',fj,e)
    if not meshes: continue
    m=trimesh.util.concatenate(meshes)
    m.apply_scale(0.001)  # mm -> m
    m.export(f'glb/{g}.glb')
    print('ok',g,len(m.faces))
