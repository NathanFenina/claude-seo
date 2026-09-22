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

## 6. Les illustrations — obligatoires, et jamais décoratives

Retour client du 22/09 : *« contenu assez faible et pas assez world class, ça manque
cruellement d'image »*. Le diagnostic était juste — les pages n'avaient qu'un visuel de
hero abstrait, réutilisé d'une autre section, et aucun schéma dans le corps.

**Un contenu B2B sans figure se fait survoler.** Un comité d'achat ne lit pas 1 500 mots :
il cherche le schéma qui résume l'arbitrage, et le transmet en interne. Une page ou un
article sans illustration porteuse d'information n'est pas terminé.

### La règle

> **Toute page et tout article porte au moins un schéma, et ce schéma dit quelque chose
> que le texte ne dit pas mieux.** Si la figure ne fait que répéter un paragraphe, elle
> ne doit pas exister : un visuel qui n'apporte rien alourdit la page.

Aucun modèle de génération d'images n'est disponible dans cet environnement — et c'est
sans importance, parce qu'une illustration décorative ne servirait à rien ici. Les
schémas sont **rendus par code à partir du contenu réel**.

### Comment produire un schéma

```bash
# 1. Décrire la figure — les DONNÉES, pas le dessin
$EDITOR build/illustrations/figures.yml

# 2. Rendre (HTML -> Chromium -> WebP + JPEG, 2400 px de large)
cd build/illustrations && python3 render.py --only <id>
#    -> deploy/htdocs/illustrations/schemas/<id>.{webp,jpg}
```

Les tokens de charte sont **lus dans `system.css` au moment du rendu** et les polices de
marque embarquées depuis les woff2 du thème : aucune couleur ni police n'est recopiée,
donc aucune dérive possible. Il n'y a rien à vérifier côté charte.

### Les quatre gabarits disponibles

| Gabarit | Sert à | Exemple en production |
|---|---|---|
| `steps` | Un processus ordonné, 3 ou 4 étapes | `methode-conseil`, `chaine-redaction` |
| `columns` | Opposer 2 à 4 options sur les mêmes critères | `b2b-vs-b2c`, `owned-earned-paid` |
| `cluster` | Un élément central et ses satellites | `cluster-semantique`, `carte-leviers` |
| `funnel` | Des étapes de tunnel avec leur indicateur | `tunnel-kpi` |

Un gabarit neuf s'ajoute dans `render.py` (fonction `layout_<nom>`), pas en écrivant du
CSS dans le YAML.

### Brancher la figure

**Page de la vitrine** — le gabarit partagé porte un emplacement, entre la section
« enjeu » et la méthode. Déclarer dans le YAML, FR **et** EN :

```yaml
figure:
  id: comite-achat-b2b
  height: 1620            # hauteur réelle du rendu — évite le décalage de mise en page
  aria: "Le comité d'achat IT"
  alt: "…"                # reprendre l'alt de figures.yml
  caption: "…"            # ce que la figure démontre, pas ce qu'elle montre
```

**Article du blog** — déclarer `FIGURES` dans le module, et poser le marqueur à
l'endroit voulu :

```python
FIGURES = [{"id": "b2b-vs-b2c", "alt": "…", "caption": "…"}]
...
    p("{{FIG:b2b-vs-b2c}}"),      # publish.py remplace le BLOC paragraphe entier
```

`publish.py` téléverse le fichier (idempotent) et substitue le bloc. ⚠️ Il remplace le
bloc `wp:paragraph` complet, pas son texte : une `<figure>` dans un `<p>` est du HTML
invalide, le navigateur ferme le paragraphe avant elle.

### Ce qui fait une bonne légende

La légende ne décrit pas l'image — le lecteur la voit. Elle dit **ce que la figure
démontre** et ce qu'on en fait. « Tableau comparant le B2B et le B2C » est inutile ;
« ignorer une seule de ces six contraintes suffit à rendre un dispositif inopérant »
apporte quelque chose.

L'attribut `alt`, lui, décrit bien le contenu : il sert au lecteur d'écran et au moteur.

---

## 7. Ne pas produire cinq fois la même page

Retour client du 22/09, après les schémas : *« ça manque clairement de contenu, c'est un
peu vide, et aussi les images, et faire tourner les chiffres, et casser la symétrie »*.

Le diagnostic portait sur le gabarit, pas sur le volume. Les cinq pages d'offre sont
rendues par `_seopage_body.html`, un template partagé — ce qui est un acquis : une
correction de charte se fait une fois. Mais tant que chaque page ne remplissait que les
mêmes emplacements dans le même ordre, avec les **mêmes trois chiffres**, le lecteur qui
en ouvrait deux voyait un formulaire rempli deux fois. À 1 400 mots chacune, ce n'est pas
un manque de texte : c'est un manque de **singularité**, et ça se lit comme du vide.

> **Deux pages du même gabarit ne doivent jamais donner la même impression de lecture.**
> Le gabarit est partagé ; ce qu'on y met ne l'est pas.

### Règle 1 — un bloc propre à la page, d'un type que ses voisines n'ont pas

Chaque page porte une section `spotlight`, placée avant les métriques. Ce n'est pas un
bloc de plus à remplir : c'est **l'endroit où la page prouve qu'elle connaît son sujet**,
sous une forme que les autres pages n'emploient pas.

Les cinq types en production — en ajouter un nouveau plutôt que réemployer un existant :

| Page | Type de bloc | Ce qu'il fait |
|---|---|---|
| Agence SEO B2B | Grille de diagnostic | Symptôme → ce qu'il révèle → ce qu'on change |
| Conseil marketing digital | Tableau de livrables | Ce qui sort de chaque phase, et sous quelle forme |
| Rédaction web | Référentiel de formats | Format → à quelle étape il sert → longueur réelle |
| Content marketing | Aide à la décision | Internaliser ou déléguer, critère par critère |
| Marketing IT | Routeur de points d'entrée | Votre situation → par où commencer |

Structure dans le YAML (`columns` + `rows`, la première cellule de chaque ligne devient
un `<th scope="row">`) :

```yaml
spotlight:
  aria: "Le diagnostic d'entrée"
  eyebrow: "— Le diagnostic"
  title: 'Ce qu''on regarde <span class="accent">en premier</span>'
  aside: "Une phrase qui situe le tableau."
  lead: "Deux à quatre phrases qui posent le raisonnement AVANT le tableau."
  columns: ["Le symptôme", "Ce qu'il révèle", "Ce qu'on change"]
  rows:
    - ["Du trafic, aucune demande", "…", "…"]
  foot: "Optionnel — la nuance qui empêche de lire le tableau comme une recette."
```

⚠️ Le HTML dans une valeur YAML (`class="accent"`) casse le parseur s'il n'est pas
échappé. Écris ces valeurs en guillemets simples avec doublement de l'apostrophe, comme
ci-dessus, ou passe par un bloc littéral.

### Règle 2 — faire tourner les chiffres

Les métriques sont **différenciées d'une page à l'autre**. Le fonds de chiffres validés
est petit et fermé (§1) : on n'en invente pas pour varier, on **choisit ceux qui servent
l'angle de la page**. Une page rédaction met en avant les rubriques d'expertise ; une
page conseil met en avant l'ancienneté. Aucun triplet ne doit apparaître deux fois.

Vérification, à lancer avant de considérer un lot de pages terminé :

```bash
cd build && python3 -c "
import yaml, io, glob, collections
# Les pages hors sitemap (page de test en noindex) ne sont pas dans le jeu lu par
# les prospects : elles ne comptent pas comme doublon.
routes = yaml.safe_load(io.open('routes.yml', encoding='utf-8'))
exclus = {p['id'] for p in routes['pages'] if p.get('sitemap_exclude')}
vus = collections.defaultdict(list)
for f in sorted(glob.glob('content/*.fr.yml')):
    ident = f.split('/')[-1].split('.')[0]
    if ident in exclus:
        continue
    d = yaml.safe_load(io.open(f, encoding='utf-8')) or {}
    m = (d.get('metrics') or {}).get('entries')
    if m:
        # Comparaison sur l'ENSEMBLE des chiffres : réordonner trois chiffres
        # identiques ne rend pas deux pages différentes.
        vus[tuple(sorted(e['num'] for e in m))].append(ident)
for chiffres, pages in sorted(vus.items()):
    if len(pages) > 1:
        print('DOUBLON', list(chiffres), '->', pages)
print('pages indexables avec métriques :', sum(len(v) for v in vus.values()))
"
```

Une ligne `DOUBLON` = deux pages qui se ressemblent. À corriger avant déploiement.

Ce contrôle n'est pas théorique : écrit le 22/09, il a immédiatement sorti
`agence-marketing-it` et `referencement-ia`, qui affichaient les mêmes trois chiffres
**avec les mêmes libellés**. La page chapeau porte désormais l'audience, les 4 typologies
servies et les 3 objectifs adressés — un angle d'accueil, pas une redite.

### Règle 3 — deux figures, à deux moments de la lecture

Une seule figure suffisait à respecter §6, pas à tenir une page de 1 700 mots. Chaque
page d'offre en porte **deux**, séparées par plusieurs sections :

- `figure` — après la section « enjeu », elle **cadre le problème** ;
- `figure2` — avant le maillage interne, elle **récapitule la réponse** et reprend la
  matière du `spotlight` sous forme visuelle.

La seconde figure n'est pas un doublon de la première : si tu ne peux pas dire en une
phrase ce qu'elle ajoute, la page n'a pas besoin d'elle.

### Ce que ça a donné

| | Avant | Après |
|---|---|---|
| Volume par page | 1 374 – 1 498 mots | 1 654 – 1 739 mots |
| Sections H2 | 9 | 10 |
| Images | 2 | 3 |
| Triplets de chiffres distincts | 1 pour 5 pages | 5 pour 5 pages |

Le gain de volume est une conséquence, pas l'objectif. L'objectif est qu'un lecteur qui
ouvre deux pages y trouve deux raisonnements différents.

---

## 8. Le maillage interne

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

## 9. La boucle de vérification (rien ne part sans)

### Page

```bash
cd build
ENV=prod python3 build.py
ENV=prod bash qa/check_coherence.sh        # exiger « == TOUT VERT == »
cd dist && python3 -m http.server 8899     # JAMAIS file:// (règle d'or n°1)
```

Puis, avant de considérer la page finie :
- **Le contrôle de doublons de chiffres de §7 doit sortir `doublons : 0`.**
- La page porte bien **deux figures** et **un `spotlight` d'un type que ses voisines
  n'emploient pas** — sinon elle ressemblera à la page d'à côté, quel que soit son texte.
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

## 10. Déployer, c'est publier

L'indexation est ouverte depuis le go-live SEO. **Un contenu poussé sur `main` est
indexable dès la fin du run GitHub Actions** — il n'existe plus d'étape de preview.

Conséquence pratique : un texte qui doit encore être relu par le client ne se déploie
pas « pour voir ». Soit il est prêt, soit on pose une `meta robots noindex` dans le
`head_extra` de son template le temps de la relecture.

Après déploiement : vérifier les URL en 200, la non-régression sur `/`, `/en/`,
`/blog/`, puis consigner dans `deploy/DEPLOYMENT.md`.
