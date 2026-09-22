---
name: techmedias-optimisation-seo
description: >-
  Auditer, scorer sur 100 et CORRIGER une page ou un article TechMedias face à un
  mot-clé cible — l'équivalent de Yoast/Rank Math, mais il applique lui-même les
  correctifs, et dans les VRAIES sources du projet (YAML de contenu, gabarit Jinja,
  fichier d'article Python), jamais dans build/dist/ ni en prod à la main. Ajoute au
  barème classique une couche GEO/AEO (citabilité par ChatGPT, Perplexity, AI Overviews)
  et un contrôle de cannibalisation interne. Déclencher sur : « optimise cette page »,
  « score SEO », « note sur 100 », « audit on-page », « passe au vert », « est-ce bien
  optimisé », « améliore le référencement de », ou une URL techmedias.fr + un mot-clé.
  Pour ÉCRIRE un contenu neuf, utiliser techmedias-redaction-seo.
---

# Optimisation SEO/GEO — TechMedias

Deux modes, toujours dans cet ordre :

- **Audit** (par défaut) — score /100, un feu 🔴/🟡/🟢 par critère, et pour chaque
  critère non vert **ce qu'il faut changer concrètement**.
- **Correction** — tu appliques les correctifs **dans les fichiers sources**, tu
  rebuilds, tu repasses la QA, et tu affiches le score avant / après.

On ne corrige bien que ce qu'on a diagnostiqué : commence toujours par l'audit, même
quand on te demande directement d'optimiser.

---

## Où corriger (et où ne jamais toucher)

| Ce qu'on corrige | Fichier |
|---|---|
| Title, meta description | `build/content/<id>.{fr,en}.yml` → `meta:` |
| H1, sous-titres, corps, FAQ | `build/content/<id>.{fr,en}.yml` |
| Structure de page, CSS | `build/templates/_seopage_{head,body}.html` (gabarit **partagé**) |
| Slug / URL | `build/routes.yml` |
| Article de blog | `deploy/wordpress/articles/<slug>.py` |

⛔ **Jamais** `build/dist/` (artefact régénérable, règle d'or n°4), **jamais** le HTML
en prod à la main, **jamais** `deploy/htdocs/assets/system.css` pour un travail de page.
Une correction qui ne passe pas par la source est perdue au prochain build.

⚠️ Le corps des pages SEO est **mutualisé** : modifier `_seopage_body.html` change
**toutes** les pages qui l'incluent. Une correction propre à une page passe par son YAML.

⚠️ **Parité FR/EN bloquante** : toute correction dans un `.fr.yml` a son équivalent
dans le `.en.yml`, sinon `check_coherence.sh` échoue.

---

## Méthode d'audit (déterministe)

### 1. Mesurer avant de juger

```bash
S=.claude/skills/techmedias-optimisation-seo/scripts

# Page de la vitrine (sur le HTML réellement produit)
python3 $S/analyze_content.py --keyword "agence seo b2b" \
  --file build/dist/pages/agence-seo-b2b/index.html

# Article du blog (sur le contenu Gutenberg généré)
cd deploy/wordpress/articles && python3 -c "
import importlib,sys; sys.path.insert(0,'.')
m=importlib.import_module('ligne-editoriale'); print(m.CONTENT)" \
  | python3 ../../../$S/analyze_content.py --keyword "ligne éditoriale"
```

Le script rend en JSON : nombre de mots, occurrences et **densité** du mot-clé, malus
de sur-optimisation, % de phrases longues, % de mots de transition, liens internes et
externes, images et `alt`, arbre des Hn, présence FAQ/schema. **Ces chiffres sont la
base factuelle de la note — ne les estime jamais à l'œil.**

### 2. Noter contre la grille

Le barème complet, avec les seuils de chaque feu, est dans
**`references/criteres-scoring.md`** — lis-le avant de noter, c'est la source de vérité.

| Catégorie | Points |
|---|---|
| 1 · Mot-clé & sémantique | 18 |
| 2 · Balises & méta | 16 |
| 3 · Structure & Hn | 14 |
| 4 · Lisibilité | 14 |
| 5 · Maillage & E-E-A-T | 14 |
| 6 · GEO / AEO | 14 |
| 7 · Spécificités TechMedias | 10 |

La catégorie 7 est propre à ce projet et **non négociable** : sourçage des chiffres,
non-cannibalisation, parité FR/EN, conformité de charte. Un contenu excellent en SEO
mais qui invente un chiffre ne peut pas passer au vert.

En cas d'hésitation entre deux feux, prends **le plus sévère**. Un audit complaisant ne
rend service à personne.

### 3. Calculer

Points par critère → total par catégorie → score brut /100 → **malus de
sur-optimisation** → score final. Affiche le malus en clair : « 83, −8
sur-optimisation → **75** ». Les critères non applicables sont ⚪ N/A et redistribués
au prorata dans leur catégorie.

| Score | Feu | Lecture |
|---|---|---|
| 80–100 | 🟢 | Prêt à publier, ajustements mineurs |
| 55–79 | 🟡 | Correct, optimisations importantes restantes |
| 0–54 | 🔴 | À retravailler avant de viser un positionnement |

---

## Format du rapport

```markdown
## Audit — <titre> · mot-clé : « <mot-clé> »
**Score : 74/100** 🟡  (brut 79, −5 sur-optimisation)

### Mesures
1 842 mots · densité 3,8 % · 6 liens internes · 0 lien externe · 4 H2 · FAQ présente

### Par catégorie
| Catégorie | Score | Feu |
|---|---|---|
| Mot-clé & sémantique | 13/18 | 🟡 |
| …

### Ce qui bloque (par ordre d'impact)
1. 🔴 **Densité à 3,8 %** — « agence seo b2b » revient 31 fois en 1 842 mots.
   → Remplacer 12 occurrences par des variantes (« référencement B2B », « votre
   dispositif SEO »). Fichier : `build/content/agenceseob2b.fr.yml`, sections
   `definition` et `faq`.
2. 🟡 **Aucune réponse autoportante en tête** — …
```

Chaque recommandation nomme **le fichier et la section**. « C'est moyen » n'est pas une
recommandation.

---

## Mode correction

1. Applique les correctifs dans les sources, FR **et** EN.
2. Rebuild + QA :
   ```bash
   cd build && ENV=prod python3 build.py && ENV=prod bash qa/check_coherence.sh
   ```
   Exiger `== TOUT VERT ==`. Pour un article : `python3 publish.py --apply` (brouillon).
3. Re-mesure avec le script et **réaffiche le score avant / après**.
4. Ne déploie que si la QA est verte. Rappel : **déployer = publier**, l'indexation est
   ouverte.

---

## Les pièges propres à ce site

- **Sur-optimisation par le gabarit.** Le mot-clé apparaît déjà dans le hero, les
  titres de section, la FAQ et la bande CTA — la densité monte vite sans qu'on ait
  « bourré ». Corrige par des variantes, pas en supprimant des sections.
- **Les partiels HTML échappent aux greps sur les YAML.** Trois pages ont leur corps
  dans `templates/_agencemedia_body.*.html`, `_cmb_body.*.html`, `_geo_body.*.html`.
  Un audit qui ne lit que les YAML les rate. Audite toujours le HTML de `dist/`.
- **Cannibalisation interne.** Avant de recommander un contenu neuf, vérifier ce que
  le site couvre déjà (`grep -ril` sur `build/content/`, et la liste des articles du
  blog). Deux contenus TechMedias sur la même intention : aucun ne se positionne. Cas
  déjà arbitrés et documentés en tête des fichiers concernés :
  `/blog/plan-media/` vs `/blog/media-planning/`, et l'article
  `content-marketing-b2b-specificites` vs la page pilier `/pages/content-marketing-b2b/`.
- **Chiffres.** Un chiffre qui n'est pas dans la liste des six données validées (voir
  `techmedias-redaction-seo`) est un **rouge automatique** en catégorie 7, quel que
  soit le reste du score.
- **Charte.** Toute correction touchant un template repasse par les skills
  `respect-charte-graphique-techmedias`, `respect-du-header-techmedias` et
  `respect-footer-techmedias`.
