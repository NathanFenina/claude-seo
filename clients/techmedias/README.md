# Skills client — TechMedias

Skills SEO/GEO **spécifiques au mandat TechMedias** (techmedias.fr + blog WordPress,
agence marketing & médias IT B2B, éditrice d'iTPro.fr).

Ils vivent ici pour être versionnés avec le reste de l'outillage SEO de l'agence, mais
leur emplacement d'exécution est le dépôt client : `tech-medias/.claude/skills/`, d'où
Claude Code les charge automatiquement. **Toute modification se fait des deux côtés.**

## Pourquoi des skills client plutôt que les génériques

Le dépôt fournit déjà `seo-redaction` et `seo-optimisation-onpage`, qui couvrent le
sujet pour n'importe quel site. Ils supposent toutefois un pipeline WordPress/Elementor
et un contenu manipulé en HTML. TechMedias n'a ni l'un ni l'autre :

| | Générique | TechMedias |
|---|---|---|
| Vitrine | HTML dans un CMS | Générateur statique maison : `routes.yml` + `content/*.{fr,en}.yml` + Jinja2 |
| Blog | HTML | Blocs Gutenberg générés par `deploy/wordpress/articles/_blocks.py` |
| Chiffres | Sourcés à la demande | **Liste fermée de six données validées**, tout le reste interdit |
| Langues | Une | FR + EN, **parité bloquante** en QA |
| Design | Libre | Tokens `system.css` imposés, zéro hexadécimal en dur |

Appliquer un skill générique ici produit des recommandations justes en apparence et
inapplicables en pratique — il désignerait des fichiers qui n'existent pas.

## Les deux skills

| Skill | Rôle |
|---|---|
| `techmedias-redaction-seo` | Écrire une page ou un article : passe anti-cannibalisation obligatoire avant d'écrire, chiffres autorisés, format réel de production, voix, maillage, boucle de vérification. |
| `techmedias-optimisation-seo` | Noter sur 100 puis corriger **dans les sources** : grille en 7 catégories (les 6 classiques + une catégorie TechMedias dont un rouge plafonne le score à 79), script de mesure déterministe. |

## Origine

La substance vient de deux sources, fusionnées puis resserrées :

- **`skills-seo` (zip Décupler)** — grille de scoring Yoast + couche GEO, malus de
  sur-optimisation, script `analyze_content.py`, test anti-« bateau » de
  `redaction-expert`.
- **Ce dépôt** — barème de `seo-optimisation-onpage`, exigences de `seo-redaction`.

## Deux correctifs apportés au script de mesure

`analyze_content.py` est repris du zip avec deux ajouts. Le second n'est pas propre à
TechMedias et vaut probablement pour d'autres clients.

1. **`--strip-chrome`** *(spécifique)* — n'analyse que le corps de page, entre
   `<main id="main">` et `<footer class="site-foot">`. Sans cette option, la nav et le
   footer mutualisés créditent chaque page de ~25 liens internes, 12 liens externes et
   15 H3 qu'elle ne porte pas : les mesures de maillage et de structure deviennent
   fausses, et identiques d'une page à l'autre.

2. **Frontières de bloc** *(générique)* — un point est inséré à la fermeture de chaque
   balise de bloc avant de découper en phrases. Sans cela, un titre de carte sans
   ponctuation finale (« Éditeurs de logiciels ») se colle au paragraphe suivant et
   fabrique une fausse phrase de 40 mots. Effet mesuré sur les 5 pages TechMedias :
   **45 à 52 % de « phrases longues » avant correctif, 12 à 15 % après** — un rouge
   intégral sur toute la catégorie lisibilité, qui ne correspondait à aucun défaut réel
   du texte. Tout gabarit à base de cartes est concerné.

## Utilisation

```bash
S=.claude/skills/techmedias-optimisation-seo/scripts

# Page de la vitrine
python3 $S/analyze_content.py --strip-chrome --keyword "agence seo b2b" \
  --file build/dist/pages/agence-seo-b2b/index.html

# Article du blog
cd deploy/wordpress/articles && python3 -c "
import importlib,sys; sys.path.insert(0,'.')
print(importlib.import_module('ligne-editoriale').CONTENT)" \
  | python3 ../../../$S/analyze_content.py --keyword "ligne éditoriale"
```
