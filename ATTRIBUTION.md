# Atribuições e licenças

As imagens deste repositório são **obras derivadas** de modelos 3D anatômicos de terceiros e são distribuídas sob **Creative Commons Atribuição-CompartilhaIgual 4.0 Internacional (CC BY-SA 4.0)** — https://creativecommons.org/licenses/by-sa/4.0/ (texto integral em `LICENSE-CC-BY-SA-4.0.txt`).

## Fontes

### BodyParts3D
- © The Database Center for Life Science (DBCLS), licenciado sob CC Atribuição 4.0 Internacional (CC BY 4.0) — https://creativecommons.org/licenses/by/4.0/ (texto em `LICENSE-CC-BY-4.0-BodyParts3D.txt`).
- Página do projeto: https://lifesciencedb.jp/bp3d/
- Citação: Mitsuhashi N. et al., "BodyParts3D: 3D structure database for anatomical concepts", Nucleic Acids Research 37 (2009) D782–D785.
- Uso: maioria dos músculos e esqueleto de apoio (modelo `isa_BP3D_4.0`).

### Z-Anatomy
- Licenciado sob CC Atribuição-CompartilhaIgual 4.0 Internacional (CC BY-SA 4.0) — https://www.z-anatomy.com/ e https://github.com/Z-Anatomy
- Obtido via repositório `mhaney93/body-atlas` (`public/models/muscular.glb`), que redistribui o modelo muscular do Z-Anatomy.
- Uso: grande dorsal, reto abdominal, oblíquo interno e eretores da espinha (iliocostal, longuíssimo e espinal).
- Partes do Z-Anatomy sob licença não comercial (orelha, ossículos, nervos do ouvido interno) **não são usadas**.

### Cabeça
Geometria procedural original deste projeto (superelipsoide), sem uso de modelo de terceiros.

## O que foi alterado
Veja `CHANGES.md`. Resumo: conversão para glTF, alinhamento entre os dois modelos, renderização ortográfica em frente e costas, colorização por função muscular (principal/secundário), composição de camadas, recorte, redução de escala e compressão WebP.

## Condições de redistribuição das imagens
1. **Atribuição**: mantenha este arquivo (ou os mesmos créditos) junto às imagens.
2. **Indicação de alterações**: mantenha ou cite `CHANGES.md`.
3. **Licença**: link para CC BY-SA 4.0; as imagens e qualquer adaptação delas devem ser distribuídas sob CC BY-SA 4.0 (ou licença compatível).
4. Não há garantia; não há uso médico ou diagnóstico.

Os scripts em `pipeline/` (código próprio) seguem a mesma licença para simplificar a redistribuição, sem restringir os termos acima.
