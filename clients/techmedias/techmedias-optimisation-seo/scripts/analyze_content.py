#!/usr/bin/env python3
"""
analyze_content.py — mesures objectives pour l'audit techmedias-optimisation-seo.

Adapté du script `seo-geo-score` de Décupler. Ajout propre à TechMedias : l'option
--strip-chrome isole le CORPS de la page (entre <main id="main"> et le <footer
class="site-foot">) avant de mesurer. Sans elle, la nav et le footer — partagés par
les 38 pages — ajoutent à chaque page ~25 liens internes, 12 liens externes, 2 images
et une quinzaine de H3, ce qui rend les mesures de maillage et de structure fausses
et identiques d'une page à l'autre. Toujours l'utiliser sur un HTML de build/dist/.

But : donner au skill des CHIFFRES RÉELS (densité, longueur des phrases, liens,
images/alt, présence FAQ/schema) au lieu d'estimations « à l'œil ». C'est ce qui
rend le score réaliste et reproductible : deux audits du même contenu donnent les
mêmes mesures.

Usage :
    python3 analyze_content.py --keyword "content marketing" --file article.html
    cat article.html | python3 analyze_content.py --keyword "content marketing"

Sortie : un bloc JSON avec les mesures. Le skill lit ces chiffres, applique la
grille (references/criteres-scoring.md) et le malus sur-optimisation, puis rédige
le rapport. Le jugement qualitatif (pertinence, ton, intention) reste au modèle ;
le script ne fait que le quantitatif fiable.
"""
import argparse
import json
import re
import sys

# Mots de transition FR (liste indicative, pour estimer la fluidité façon Yoast).
TRANSITIONS = {
    "d'abord", "ensuite", "enfin", "puis", "donc", "ainsi", "car", "parce que",
    "cependant", "toutefois", "néanmoins", "pourtant", "en effet", "par ailleurs",
    "de plus", "en outre", "par exemple", "notamment", "surtout", "en revanche",
    "au contraire", "tandis que", "alors que", "par conséquent", "c'est pourquoi",
    "grâce à", "afin de", "pour", "malgré", "puisque", "désormais", "aujourd'hui",
    "plutôt que", "en résumé", "pour conclure", "d'une part", "d'autre part",
}


def strip_chrome(html: str) -> str:
    """Isole le corps de la page TechMedias : <main id="main"> … <footer class="site-foot".

    Le chrome (nav + footer) est mutualisé par base.html.j2 : le mesurer reviendrait à
    créditer chaque page de liens et de titres qu'elle ne porte pas. Si les repères ne
    sont pas trouvés (autre gabarit, contenu collé), on renvoie le HTML tel quel.
    """
    start = re.search(r'<main[^>]*id="main"[^>]*>', html, re.I)
    if not start:
        return html
    body = html[start.end():]
    end = re.search(r'<footer[^>]*class="[^"]*site-foot', body, re.I)
    return body[:end.start()] if end else body


# Balises de bloc : leur fermeture termine une unité de lecture, même sans ponctuation.
BLOCK_TAGS = (
    "p|div|section|article|aside|main|header|footer|h[1-6]|li|ul|ol|dt|dd|"
    "td|th|tr|table|figure|figcaption|blockquote|summary|details|br|hr|nav|span"
)


def strip_noise(html: str):
    """Retire commentaires, <script>, <style> ; renvoie (texte_visible, html_brut).

    ⚠️ Correctif TechMedias — sans lui, la mesure de lisibilité est fausse sur ce site.
    Le gabarit de page empile des titres de cartes et des libellés SANS ponctuation
    finale (« Éditeurs de logiciels », « 100 000+ décideurs IT B2B »…). En remplaçant
    naïvement chaque balise par une espace, ces libellés se collent au paragraphe
    suivant et forment une fausse phrase de 40 mots. Résultat mesuré avant correctif :
    45 à 52 % de « phrases longues » sur les 5 pages — un rouge intégral qui ne
    correspondait à aucun défaut réel du texte.
    On insère donc un point à la fermeture de chaque balise de bloc : une unité de
    lecture s'y termine, même sans ponctuation typographique.
    """
    raw = html
    no_comment = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    no_script = re.sub(r"<script.*?</script>", " ", no_comment, flags=re.S | re.I)
    no_style = re.sub(r"<style.*?</style>", " ", no_script, flags=re.S | re.I)
    bounded = re.sub(rf"</(?:{BLOCK_TAGS})\s*>|<(?:br|hr)\s*/?>", " . ", no_style, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", bounded)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(?:\s*\.){2,}", " . ", text)          # points de frontière consécutifs
    text = re.sub(r"([.!?:;,])\s+\.", r"\1", text)          # ponctuation réelle déjà présente
    return text.strip(), raw


def word_tokens(text: str):
    return re.findall(r"[0-9a-zàâäéèêëïîôöùûüçœ]+", text.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strip-chrome", action="store_true",
                    help="TechMedias : ne mesurer que le corps de page "
                         "(<main id=\"main\"> … <footer class=\"site-foot\">), "
                         "sans la nav ni le footer mutualisés.")
    ap.add_argument("--keyword", required=True, help="Mot-clé principal ciblé")
    ap.add_argument("--file", help="Fichier contenu (HTML ou texte). Sinon: stdin")
    args = ap.parse_args()

    html = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    if args.strip_chrome:
        html = strip_chrome(html)
    text, raw = strip_noise(html)
    low = text.lower()
    kw = args.keyword.lower().strip()
    kw_wordlen = len(kw.split())

    words = word_tokens(text)
    n = len(words) or 1

    # Densité du mot-clé exact (correspondance contiguë stricte).
    occ = len(re.findall(re.escape(kw), low))
    density = occ * kw_wordlen / n * 100

    # Correspondance "distribuée", façon Yoast : le mot-clé compte même si de petits
    # mots s'intercalent ("rénovation À Fontainebleau"). On retire les mots vides du
    # mot-clé, puis on compte les fenêtres qui contiennent TOUS les mots utiles.
    STOP = {"de", "du", "des", "la", "le", "les", "l", "à", "a", "au", "aux", "en",
            "et", "pour", "un", "une", "d"}
    content_words = [w for w in word_tokens(kw) if w not in STOP]
    distributed = 0
    if content_words:
        win = len(content_words) + 4  # petite fenêtre glissante tolérante
        i = 0
        while i <= max(0, n - 1):
            window = set(words[i:i + win])
            if all(cw in window for cw in content_words):
                distributed += 1
                i += win  # fenêtres non chevauchantes pour ne pas sur-compter
            else:
                i += 1
    # Densité effective : la plus favorable des deux (exacte vs distribuée),
    # pour ne pas pénaliser un mot-clé local bien placé mais non contigu.
    density_distrib = distributed * len(content_words) / n * 100 if content_words else 0
    density_eff = max(density, density_distrib)

    # Phrases + longueur.
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    long_sents = [s for s in sentences if len(word_tokens(s)) > 20]
    pct_long = (len(long_sents) / len(sentences) * 100) if sentences else 0

    # Mots de transition (part des phrases qui en contiennent au moins un).
    with_trans = sum(1 for s in sentences if any(t in s.lower() for t in TRANSITIONS))
    pct_trans = (with_trans / len(sentences) * 100) if sentences else 0

    # Liens (sur le HTML brut).
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', raw, flags=re.I)
    external = [h for h in hrefs if re.match(r"https?://", h, flags=re.I)]
    internal = [h for h in hrefs if h.startswith("/") or h.startswith("#")]

    # Images + alt.
    imgs = re.findall(r"<img\b[^>]*>", raw, flags=re.I)
    imgs_with_alt = [t for t in imgs if re.search(r'alt=["\'][^"\']+["\']', t, flags=re.I)]

    # Titres.
    headings = {f"h{i}": len(re.findall(rf"<h{i}\b", raw, flags=re.I)) for i in range(1, 5)}

    # Signaux GEO.
    has_faq_schema = bool(re.search(r'"@type"\s*:\s*"FAQPage"', raw, flags=re.I))
    has_any_schema = bool(re.search(r"application/ld\+json", raw, flags=re.I))
    kw_in_first_100 = kw in " ".join(words[:100])

    out = {
        "mot_cle": args.keyword,
        "mots": n,
        "occurrences_exactes": occ,
        "occurrences_distribuees": distributed,
        "densite_exacte_pct": round(density, 2),
        "densite_effective_pct": round(density_eff, 2),
        "densite_verdict": (
            "ABSENT" if density_eff == 0 else
            "OK" if density_eff <= 2.5 else
            "un peu haute" if density_eff <= 3.5 else
            "SUR-OPTIMISATION"
        ),
        "malus_suroptimisation": (
            0 if density_eff <= 3.5 else
            5 if density_eff <= 5 else
            8 if density_eff <= 6.5 else 12
        ),
        "mot_cle_dans_100_premiers_mots": (
            kw_in_first_100 or all(cw in " ".join(words[:100]) for cw in content_words)
        ),
        "phrases": len(sentences),
        "phrases_longues_pct": round(pct_long, 1),
        "mots_transition_pct": round(pct_trans, 1),
        "liens_internes": len(internal),
        "liens_externes": len(external),
        "images": len(imgs),
        "images_avec_alt": len(imgs_with_alt),
        "titres": headings,
        "faq_schema": has_faq_schema,
        "schema_present": has_any_schema,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
