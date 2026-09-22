---
name: techmedias-redaction-seo
description: >-
  Rédiger une page ou un article TechMedias (techmedias.fr + blog WordPress) au niveau
  attendu par une audience de praticiens IT : angle propre, profondeur, zéro remplissage,
  et 100 % du contenu traçable à une source existante. Couvre l'anti-cannibalisation
  (vérifier ce que le site dit déjà AVANT d'écrire), le format réel de production
  (YAML + Jinja pour la vitrine, blocs Gutenberg pour le blog), la parité FR/EN, la voix
  de marque et le maillage interne. Déclencher dès qu'on demande de créer, rédiger,
  écrire ou produire une page, un article, un brief ou un contenu pour TechMedias ou
  iTPro.fr — même sans le mot « rédaction ». Pour NOTER ou CORRIGER un contenu existant,
  utiliser techmedias-optimisation-seo (complémentaire : celui-ci écrit, l'autre score).
---

# Rédaction SEO/GEO — TechMedias

Tu écris pour des **praticiens** : DSI, RSSI, IT managers, dirigeants d'ESN. Ils
pratiquent le sujet tous les jours et repèrent une généralité en une phrase. Le seul
contenu qui fonctionne ici est celui qui leur apprend quelque chose.

Ce skill dit **comment écrire**. Pour noter ou corriger un contenu existant, c'est
`techmedias-optimisation-seo`. Les trois skills de charte
(`respect-charte-graphique-techmedias`, `respect-du-header-techmedias`,
`respect-footer-techmedias`) restent obligatoires dès qu'on touche à un template.

---

## 1. La contrainte qui prime sur tout : 100 % sourcé

Règle d'or n°5 du projet, et elle ne se négocie pas : **aucun chiffre, aucune
statistique, aucune promesse, aucun délai type qui ne soit déjà validé.**

**Chiffres autorisés** (tous déjà publiés sur le site, et eux seuls) :

| Donnée | Source dans le repo |
|---|---|
| 100 000+ décideurs IT B2B | `build/content/activation.fr.yml`, `home.fr.yml` |
| 25 ans d'autorité éditoriale | `build/content/about.fr.yml`, `home.fr.yml` |
| 8 rubriques d'expertise | `build/content/activation.fr.yml` |
| 190 leads · 1 M€+ d'opportunités · 8 semaines | `build/content/casestudy.fr.yml` |
| 4 typologies : éditeur, ESN, MSP, constructeur | `build/templates/_agencemedia_body.fr.html` |
| Taxonomie Notoriété / Business / Alignement | `build/content/home.fr.yml` (`method`) |

**Tout le reste est interdit** : pas de « 70 % des acheteurs B2B… », pas de « un cycle
dure 6 à 18 mois », pas de « consacrez 20 % à la création et 80 % à la diffusion », pas
de ratio budgétaire type. Ces formules *sonnent* juste et c'est exactement le problème :
elles sont invérifiables et engagent le client.

Quand une affirmation chiffrée manquerait vraiment :
1. Reformule en méthode plutôt qu'en chiffre (« la répartition dépend de trois
   facteurs : … » plutôt que « 60/40 »).
2. Si c'est impossible, **signale le trou** à l'utilisateur et laisse un TODO dans le
   fichier. Ne brode pas.

En tête de chaque fichier de contenu, liste les **sources de chaque affirmation** —
c'est la convention déjà en place, elle permet de relire un contenu six mois plus tard.

---

## 2. Avant d'écrire : la passe anti-cannibalisation (obligatoire)

Le site compte déjà 19 pages FR et 8 articles. Deux contenus TechMedias sur la même
intention se font concurrence et **aucun des deux ne se positionne**. Cette vérification
n'est pas optionnelle, elle a déjà produit deux incidents documentés (« plan média » vs
« média planning », l'article « content marketing B2B » vs sa page pilier).

```bash
# 1. Ce que les pages disent déjà sur le territoire visé
grep -ril "<mot-clé ou sa racine>" build/content/*.fr.yml

# 2. Les H2/H3 réellement publiés sur une page proche
grep -o '<h[23][^>]*>[^<]*' build/dist/pages/<slug>/index.html | sed 's/<[^>]*>//'

# 3. Ce que le blog couvre déjà
curl -s "$TECHMEDIAS_BLOG/wp-json/wp/v2/posts?per_page=50&_fields=slug,title" \
  | python3 -c "import json,sys;[print(p['slug'],'·',p['title']['rendered']) for p in json.load(sys.stdin)]"
```

Puis tranche explicitement :

- **Intention différente** → écris, et pose un lien croisé entre les deux contenus.
- **Même intention** → **ne crée pas un second contenu.** Recommande d'optimiser
  l'existant pour couvrir aussi la nouvelle requête, et dis-le à l'utilisateur. C'est
  presque toujours la bonne réponse, même quand la roadmap prévoit un contenu neuf.
- **Intention voisine** (page pilier vs satellite) → écris le satellite avec un angle
  propre, un titre qui ne vise pas la requête de tête du pilier, et un **lien montant**
  vers le pilier dès l'introduction.

Inscris l'arbitrage en commentaire en tête du fichier : la prochaine session doit
pouvoir comprendre pourquoi ce contenu existe à côté de l'autre.

---

## 3. Le test anti-remplissage

À appliquer à **chaque paragraphe** :

> « Est-ce qu'un DSI qui pratique le sujet apprend quelque chose ici, ou est-ce qu'il
> lit ce qu'il sait déjà ? »

Si c'est la seconde réponse : supprime ou creuse. Un paragraphe qui pourrait figurer
tel quel sur le site d'un concurrent ne défend pas TechMedias, il le banalise.

**Interdits** : « il est important de », « à l'ère du numérique », « dans un monde
où », « de nos jours », adjectifs sans preuve, conclusions qui résument sans trancher.

**Obligatoires** : une position assumée par section, le *comment* et pas seulement le
*quoi*, la contrepartie de chaque recommandation (ce qu'elle coûte, quand elle ne
s'applique pas), et au moins une chose que le lecteur ne fera plus après avoir lu.

Le marqueur le plus fiable d'un bon contenu TechMedias : **il dit aussi ce qu'il ne
faut pas faire, et quand s'abstenir.** Une section « quand ne pas se lancer » vaut
mieux que trois arguments de plus.

---

## 4. La voix

- **Vouvoiement**, registre professionnel, pas de familiarité ni d'humour.
- **Phrases denses et courtes.** Une idée par phrase.
- **Gras** sur les idées-clés uniquement, jamais sur des phrases entières.
- **Français parfait, accents obligatoires** (règle d'or n°8) — y compris dans les
  commentaires des fichiers et les messages de commit.
- Termes du métier employés avec leur sens exact : ESN, MSP, éditeur, constructeur,
  MQL, SQL, DSI, RSSI. Ne jamais les gloser comme si le lecteur ne les connaissait pas.
- On parle **depuis le média** : TechMedias édite iTPro.fr, ce n'est pas un partenaire
  ni un carnet d'adresses. C'est le seul argument que les concurrents ne peuvent pas
  reprendre — il doit apparaître, sans être répété à chaque section.

---

## 5. Le format réel de production

### Page de la vitrine

Trois fichiers, jamais plus :

```
build/routes.yml                       # + une entrée id / fr / en / built: [fr, en]
build/content/<id>.fr.yml              # les TEXTES (markup inline rendu en |safe)
build/content/<id>.en.yml              # miroir EXACT — la QA de parité est bloquante
build/templates/<id>.html.j2           # 11 lignes, rien de plus :
```

```jinja
{% extends "base.html.j2" %}
{% block head_extra %}{% include "_seopage_head.html" %}{% endblock %}
{% block content %}{% include "_seopage_body.html" %}{% endblock %}
```

Le gabarit partagé `_seopage_body.html` impose la structure : hero → définition →
cartes → enjeu → méthode → CTA → métriques → preuve → maillage → FAQ → bande CTA.
Les clés attendues sont documentées en tête de `_seopage_body.html`. **Aucun texte en
dur dans un template**, aucune couleur hexadécimale, aucune nouvelle `font-family`.

Slugs EN : toujours marqués `# slug EN À VALIDER par Renaud`.

### Article du blog

```
deploy/wordpress/articles/<slug>.py    # SLUG, TITLE, EXCERPT, CATEGORIES, TAGS, CONTENT
```

Le contenu se compose avec les helpers de `_blocks.py` — `p()`, `h2()`, `h3()`,
`ul()`, `ol()`, `table()`, `quote()`, `faq()` — jamais en écrivant des commentaires
`<!-- wp:… -->` à la main. `faq()` produit l'accordéon **et** le JSON-LD FAQPage.

Catégories et étiquettes : **utiliser celles qui existent**, `publish.py` refuse un
slug inconnu plutôt que d'en créer un. Vérifier avant d'écrire :

```bash
curl -s -u "$TECHMEDIAS_WP_USER:$TECHMEDIAS_WP_PWD" \
  "$TECHMEDIAS_BLOG/wp-json/wp/v2/tags?per_page=100&_fields=slug"
```

Longueur cible : **1 700 à 2 000 mots**, la fourchette des articles déjà publiés.
`python3 <slug>.py` affiche le compte.

Signature par défaut : **Renaud Rosset**. Aucun compte utilisateur n'est créé.

---

## 6. Le maillage interne

Chaque contenu neuf doit **recevoir** et **émettre** des liens. Le gabarit de page
offre 7 destinations : le 2e CTA du hero, le CTA de la section preuve, les 4 cartes de
la section « maillage », et le 2e CTA de la bande finale.

Carte du site à jour (`build/routes.yml` fait foi) :

| Territoire | Page |
|---|---|
| Hub de l'offre | `/pages/agence-marketing-it/` |
| Amont / cadrage | `/pages/conseil-marketing-digital/` |
| Média & amplification | `/pages/agence-media-it/` · `/pages/itprofr-activation-media/` |
| Régie | `/pages/regie-publicitaire/` |
| Dispositif éditorial | `/pages/agence-content-marketing/` |
| Exécution éditoriale | `/pages/agence-redaction-web/` |
| Pilier contenu (guide) | `/pages/content-marketing-b2b/` · `/pages/pilier-content/` |
| Référencement | `/pages/agence-seo-b2b/` |
| Moteurs IA | `/pages/referencement-ia/` · `/pages/geo-generative-engine-optimization/` |
| Leads | `/pages/generation-mql-sql/` |
| Preuve | `/pages/etude-cas-cybersecurite/` |

`/pages/agence-seo-tech/` est une **page de test désindexée** : ne jamais pointer
dessus.

Depuis un article, lier vers la vitrine en chemin absolu (`/pages/…/`) et vers les
autres articles en `/blog/<slug>/`. Vérifier que la cible existe **avant** de publier :
un lien vers un brouillon non publié renvoie 404.

---

## 7. La boucle de vérification (rien ne part sans)

### Page

```bash
cd build
ENV=prod python3 build.py
ENV=prod bash qa/check_coherence.sh        # exiger « == TOUT VERT == »
cd dist && python3 -m http.server 8899     # JAMAIS file:// (règle d'or n°1)
```

Puis, avant de considérer la page finie :
- `grep -nE '#[0-9a-fA-F]{3,6}|rgba?\(' build/templates/_seopage_head.html` → doit être vide.
- Noms d'icônes Material Symbols validés (une icône inexistante s'affiche en texte brut
  sur la page live).
- Aucun scroll horizontal en 1440 px **et** en 390 px.

### Article

```bash
cd deploy/wordpress/articles
python3 <slug>.py                     # compte de mots
python3 publish.py                    # dry-run, n'envoie rien
python3 publish.py --apply            # crée/met à jour en BROUILLON
```

Contrôler avant publication : HTML équilibré, blocs `wp:` appariés, JSON-LD FAQPage
valide et sans markup résiduel, liens internes résolus.

---

## 8. Déployer, c'est publier

L'indexation est ouverte depuis le go-live SEO. **Un contenu poussé sur `main` est
indexable dès la fin du run GitHub Actions** — il n'existe plus d'étape de preview.

Conséquence pratique : un texte qui doit encore être relu par le client ne se déploie
pas « pour voir ». Soit il est prêt, soit on pose une `meta robots noindex` dans le
`head_extra` de son template le temps de la relecture.

Après déploiement : vérifier les URL en 200, la non-régression sur `/`, `/en/`,
`/blog/`, puis consigner dans `deploy/DEPLOYMENT.md`.
