# Grille de scoring — techmedias-optimisation-seo

Score global sur **100 points**, 7 catégories. Chaque critère reçoit un feu :

- 🟢 **Vert** → 100 % des points du critère.
- 🟡 **Orange** → 50 % des points (arrondi au supérieur).
- 🔴 **Rouge** → 0 point.
- ⚪ **N/A** → critère retiré du total, points redistribués au prorata dans sa catégorie.

Hésitation entre deux feux → prendre **le plus sévère**.

Origine : grille `seo-geo-score` de Décupler (Yoast/Rank Math + couche GEO), resserrée
pour TechMedias et augmentée d'une catégorie 7 propre au projet.

| Catégorie | Pts |
|---|---|
| 1 · Mot-clé & sémantique | 18 |
| 2 · Balises & méta | 16 |
| 3 · Structure & Hn | 14 |
| 4 · Lisibilité | 14 |
| 5 · Maillage & E-E-A-T | 14 |
| 6 · GEO / AEO | 14 |
| 7 · Spécificités TechMedias | 10 |
| **Total** | **100** |

## Bandes de score

| Score | Feu | Lecture |
|---|---|---|
| 80–100 | 🟢 | Prêt à publier, ajustements mineurs |
| 55–79 | 🟡 | Correct, optimisations importantes restantes |
| 0–54 | 🔴 | À retravailler avant de viser un positionnement |

## Malus de sur-optimisation (sur le score global)

La densité est déjà un critère, mais un mot-clé répété 30 fois dégrade **tout** le
contenu, pas seulement trois points. Après calcul du score brut :

| Densité du mot-clé exact | Malus |
|---|---|
| ≤ 3,5 % | 0 |
| 3,5 – 5 % | **−5** |
| 5 – 6,5 % | **−8** |
| > 6,5 % | **−12** |

Toujours l'afficher : « 83, −8 sur-optimisation → **75** ».

⚠️ **Spécificité TechMedias** : le gabarit `_seopage_body.html` place déjà le mot-clé
dans le hero, plusieurs titres de section, la FAQ et la bande CTA. La densité monte
donc sans bourrage volontaire. La correction passe par des **variantes**, jamais par
la suppression de sections du gabarit.

---

## Catégorie 1 — Mot-clé & sémantique (18 pts)

| Critère | Pts | 🟢 | 🟡 | 🔴 |
|---|---|---|---|---|
| Mot-clé dans le **title** | 3 | Présent, en début | Présent en fin | Absent |
| Mot-clé dans le **H1** | 3 | Exact ou très proche | Variante seulement | Absent |
| Mot-clé dans l'**intro** (100 premiers mots) | 3 | Présent naturellement | Au-delà de 100 mots | Absent du début |
| Mot-clé dans la **meta description** | 2 | Présent | Variante | Absent |
| Mot-clé dans **≥ 1 H2/H3** | 2 | Oui, naturel | Variante lointaine | Aucun |
| Mot-clé dans le **slug** | 2 | Présent, slug propre | Partiel | Absent |
| **Densité** | 3 | 0,5 – 2,5 % | 2,5 – 3,5 % ou 0,3 – 0,5 % | > 3,5 % ou ~0 % |

**Pourquoi** — *title* : signal de pertinence le plus fort et texte cliqué en SERP ·
*H1* : annonce le sujet · *intro* : les 100 premiers mots pèsent lourd pour Google
comme pour les LLM · *meta* : pas un facteur de ranking mais surlignée, elle fait le
clic · *Hn* : confirme que le sujet est traité · *slug* : signal visible et durable,
repris comme ancre · *densité* : trop bas = sujet flou, trop haut = spam.

Sur ce site, le slug est dans `build/routes.yml` — le changer après mise en ligne
impose une redirection. Ne le recommander que si le gain est net.

---

## Catégorie 2 — Balises & méta (16 pts)

| Critère | Pts | 🟢 | 🟡 | 🔴 |
|---|---|---|---|---|
| Longueur du **title** | 4 | 50–60 caractères | 45–70 | < 40, > 75, ou dupliqué sur le site |
| Longueur de la **meta description** | 4 | 140–165 caractères | 120–180 | < 100, > 190, ou absente |
| **Promesse** de la meta | 3 | Dit ce qu'on apprend, verbe d'action | Descriptive et plate | Liste de mots-clés |
| **Canonical + hreflang** | 3 | Auto-canonical, paire FR/EN + x-default | Incomplet | Absent ou croisé |
| **JSON-LD** | 2 | WebPage + FAQPage si FAQ, sans markup résiduel | Présent mais partiel | Absent ou invalide |

Sur la vitrine, canonical et hreflang sont posés par `build.py` : ces critères sont
verts par construction, sauf régression de la QA. Le JSON-LD FAQPage est ajouté
automatiquement dès que le YAML déclare `faq.entries`.

Titles du site : fourchette observée 46–69 caractères. Meta descriptions : 117–236,
cible 140–165.

---

## Catégorie 3 — Structure & Hn (14 pts)

| Critère | Pts | 🟢 | 🟡 | 🔴 |
|---|---|---|---|---|
| **H1 unique** | 3 | Un seul H1 | — | Zéro ou plusieurs |
| **Hiérarchie** Hn | 3 | Séquentielle, aucun saut | Un saut de niveau | Anarchique |
| **Plan autoportant** | 4 | Les H2 lus seuls résument le contenu | Titres corrects mais vagues | Titres génériques (« Introduction », « Conclusion ») |
| **Longueur** | 2 | Page ≥ 1 200 mots · article 1 700–2 000 | Un peu court ou long | Contenu mince |
| **Équilibre des sections** | 2 | Aucune section 3× plus longue qu'une autre | Déséquilibre visible | Un bloc monolithique |

**Pourquoi** — un plan qui ne tient pas debout sans le texte signale un contenu qui
n'a pas de thèse. C'est aussi ce que les moteurs génératifs lisent en premier pour
décider si une section est citable.

Le gabarit impose le H1 unique et la hiérarchie : ces deux critères sont verts par
construction sur une page de la vitrine.

---

## Catégorie 4 — Lisibilité (14 pts)

| Critère | Pts | 🟢 | 🟡 | 🔴 |
|---|---|---|---|---|
| **Phrases longues** (> 25 mots) | 4 | < 20 % | 20–30 % | > 30 % |
| **Paragraphes** | 3 | ≤ 4 phrases | 5–6 phrases | Blocs compacts |
| **Mots de transition** | 3 | ≥ 25 % des phrases | 15–25 % | < 15 % |
| **Voix active** | 2 | Dominante | Passif fréquent | Passif dominant |
| **Jargon expliqué** | 2 | Termes techniques employés à bon escient | Quelques sigles non posés | Sigles empilés sans contexte |

⚠️ **Calibrage TechMedias** : le lecteur est un praticien. Ne pas pénaliser un
vocabulaire technique exact (ESN, MSP, MQL, RSSI) — le sur-expliquer est une faute de
registre, pas une qualité. Le critère « jargon » vise les sigles empilés sans propos,
pas la précision métier.

---

## Catégorie 5 — Maillage & E-E-A-T (14 pts)

| Critère | Pts | 🟢 | 🟡 | 🔴 |
|---|---|---|---|---|
| **Liens internes sortants** | 4 | ≥ 4, ancres descriptives, cibles pertinentes | 2–3, ou ancres pauvres | < 2, ou « cliquez ici » |
| **Cibles valides** | 3 | Toutes en 200 | Une cible douteuse | Un lien 404 ou vers `/pages/agence-seo-tech/` |
| **Preuve** | 4 | REX chiffré ou cas nommé | Allusion à un résultat | Aucune preuve |
| **Expérience démontrée** | 3 | « ce qu'on observe », méthode, contrepartie assumée | Ton d'expert sans démonstration | Exposé neutre interchangeable |

**Pourquoi** — en B2B, l'acheteur recoupe systématiquement le discours. Un contenu
sans preuve est lu comme de l'argumentaire.

`/pages/agence-seo-tech/` est une page de test désindexée : tout lien vers elle est un
🔴. Le gabarit de page offre 7 emplacements de lien (2e CTA du hero, CTA de la preuve,
4 cartes de maillage, 2e CTA de la bande finale) — en utiliser au moins 5.

---

## Catégorie 6 — GEO / AEO (14 pts)

Ce qu'un moteur génératif regarde pour décider de citer une source.

| Critère | Pts | 🟢 | 🟡 | 🔴 |
|---|---|---|---|---|
| **Réponse directe en tête** | 4 | 40–60 mots autoportants près du H1 | Réponse diluée sur 3 paragraphes | Aucune réponse avant le 3e écran |
| **Sections extractibles** | 3 | Chaque section se comprend hors contexte | Certaines dépendent de la précédente | Texte continu non découpable |
| **Définition explicite** | 2 | Le sujet défini en une phrase nette | Définition implicite | Jamais défini |
| **FAQ** | 3 | ≥ 4 questions, réponses de 40–80 mots, balisées FAQPage | 2–3 questions ou balisage absent | Aucune FAQ |
| **Entités nommées** | 2 | Technologies, rôles et acteurs nommés explicitement | Allusions | Vocabulaire abstrait |

**Pourquoi** — un LLM cite un passage qu'il peut extraire sans le reste de la page.
Une réponse autoportante en tête de section est la condition d'entrée ; le balisage
FAQPage lève l'ambiguïté sur ce que contient la page.

---

## Catégorie 7 — Spécificités TechMedias (10 pts)

Propre au projet. **Un rouge ici plafonne le score global à 79** quel que soit le
reste : un contenu qui invente un chiffre ne peut pas être « prêt à publier ».

| Critère | Pts | 🟢 | 🔴 |
|---|---|---|---|
| **Sourçage des chiffres** | 4 | Tout chiffre appartient aux six données validées | Un seul chiffre, délai ou ratio non sourcé |
| **Non-cannibalisation** | 3 | Intention distincte de tout contenu existant, arbitrage documenté en tête de fichier | Doublon d'intention avec une page ou un article du site |
| **Parité FR/EN** | 2 | `.fr.yml` et `.en.yml` de structure identique, QA verte | Clé manquante d'un côté |
| **Charte** | 1 | Zéro hex, zéro `font-family` hors tokens, rayons en `var(--r-*)` | Une valeur en dur |

Les six données validées : 100 000+ décideurs IT · 25 ans d'autorité · 8 rubriques ·
190 leads · 1 M€+ d'opportunités · 8 semaines. Plus les 4 typologies (éditeur, ESN,
MSP, constructeur) et la taxonomie Notoriété / Business / Alignement.

Contrôles :

```bash
# Chiffres non sourcés (tout nombre à 2+ chiffres ou %)
grep -oE '\b[0-9]{2,}( ?%| ?€| ?ans| ?mois| ?semaines)?\b' build/content/<id>.fr.yml | sort -u

# Charte
grep -nE '#[0-9a-fA-F]{3,6}|rgba?\(|font-family:(?! *var)' build/templates/_seopage_head.html

# Parité
cd build && ENV=prod bash qa/check_coherence.sh
```

---

## N/A et contenu partiel

Si on ne te donne que le corps (sans title ni meta), note ce que tu as et marque le
reste ⚪ N/A — ne pénalise pas une information non fournie. Annonce alors le score
« sous réserve (base partielle) ».

Critères N/A fréquents : « slug » sur un texte collé, « canonical/hreflang » sur un
article de blog (géré par WordPress), « équilibre des sections » sur un contenu court.
