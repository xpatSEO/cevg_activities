#!/usr/bin/env python3
"""
Génère les pages HTML P2 (et P3) à partir de:
- titles_metas.csv (Title, Meta, H1)
- hubs_enriched.csv (destinations, top_specs, sample_desc_*)
- hub_config_p2_batch{1..5}.py (config par hub: intro, args, exp_intro)
- SISTER_HUBS + SLUG_TO_LABEL (maillage interne)
- PRICES (fourchettes tarifaires)

Sortie: seo-optimization/html/{slug}.html
"""
import csv
import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT_DIR = os.path.join(ROOT, "seo-optimization", "html")
os.makedirs(OUT_DIR, exist_ok=True)


def slug_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def clean_text(t: str) -> str:
    if not t:
        return ""
    t = re.sub(r"\s+", " ", t).strip()
    return t


# Importe les configs partagées depuis generate_p2_sheets.py
_p2sheets_path = os.path.join(ROOT, "seo-optimization", "generate_p2_sheets.py")
spec = importlib.util.spec_from_file_location("p2sheets", _p2sheets_path)
p2sheets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p2sheets)
SISTER_HUBS = p2sheets.SISTER_HUBS
SLUG_TO_LABEL = p2sheets.SLUG_TO_LABEL
PRICES = dict(p2sheets.PRICES)


# Importe les 5 batches de config par hub
def _load_batch(name: str, var: str) -> dict:
    p = os.path.join(ROOT, "seo-optimization", f"{name}.py")
    s = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return getattr(m, var)


HUB_CONFIG = {}
HUB_CONFIG.update(_load_batch("hub_config_p2_batch1", "HUB_CONFIG_BATCH_1"))
HUB_CONFIG.update(_load_batch("hub_config_p2_batch2", "HUB_CONFIG_BATCH_2"))
HUB_CONFIG.update(_load_batch("hub_config_p2_batch3", "HUB_CONFIG_BATCH_3"))
HUB_CONFIG.update(_load_batch("hub_config_p2_batch4", "HUB_CONFIG_BATCH_4"))
HUB_CONFIG.update(_load_batch("hub_config_p2_batch5", "HUB_CONFIG_BATCH_5"))
HUB_CONFIG.update(_load_batch("hub_config_p3", "HUB_CONFIG_P3"))


# Compléter les SISTER_HUBS et PRICES pour les hubs P3
SISTER_HUBS = dict(SISTER_HUBS)
SISTER_HUBS.update({
    "Conduite Ferrari": ["karting-evg", "quad-buggy-evg",
                         "conduite-char-d-assaut-evg", "jet-ski-evg",
                         "flyboard-evg"],
    "Parapente": ["chute-libre-evg", "saut-elastique-evg",
                  "saut-en-parachute-evg", "canyoning-evg",
                  "rafting-eaux-vives-evg"],
    "Laser Game": ["paintball-evg", "airsoft-battle-evg",
                   "escape-room-evg", "footbulle-evg",
                   "football-evg"],
    "Canyoning": ["rafting-eaux-vives-evg", "hydrospeed-evg",
                  "parapente-evg", "saut-elastique-evg",
                  "quad-buggy-evg"],
    "Saut en Parachute": ["saut-elastique-evg", "chute-libre-evg",
                          "parapente-evg", "faux-saut-elastique-evg",
                          "flyboard-evg"],
    "Escape Room": ["laser-game-evg", "paintball-evg",
                    "kidnapping-evg", "footbulle-evg",
                    "airsoft-battle-evg"],
    "Hydrospeed": ["rafting-eaux-vives-evg", "canyoning-evg",
                   "jet-ski-evg", "flyboard-evg",
                   "croisiere-bateau-evg"],
    "Rafting Eaux Vives": ["canyoning-evg", "hydrospeed-evg",
                           "parapente-evg", "saut-elastique-evg",
                           "quad-buggy-evg"],
})
PRICES.update({
    "Conduite Ferrari": (149, 349, "person"),
    "Parapente": (89, 159, "person"),
    "Laser Game": (19, 39, "person"),
    "Canyoning": (59, 99, "person"),
    "Saut en Parachute": (199, 299, "person"),
    "Escape Room": (19, 39, "person"),
    "Hydrospeed": (49, 99, "person"),
    "Rafting Eaux Vives": (49, 99, "person"),
})


def build_pricing_table(low: int, high: int, unit: str, n_dest: int, hub: str, price_note: str = "") -> str:
    if unit == "person":
        tarif_label = f"<strong>{low} € à {high} € par personne</strong>"
        groupe_label = "Selon la formule, généralement 4 à 15+ pers."
    else:
        tarif_label = f"<strong>{low} € à {high} € en forfait pour le groupe</strong>"
        groupe_label = "Idéal entre 6 et 15 pers."

    html = (
        '<table>\n'
        '  <thead><tr><th>Critère</th><th>Fourchette</th><th>Précisions</th></tr></thead>\n'
        '  <tbody>\n'
        f'    <tr><td>Tarif</td><td>{tarif_label}</td><td>Selon la destination et la formule</td></tr>\n'
        '    <tr><td>Durée</td><td>1h à 4h</td><td>Transferts inclus selon les destinations</td></tr>\n'
        f'    <tr><td>Taille du groupe</td><td>{groupe_label}</td><td>Au-delà : créneaux multiples</td></tr>\n'
        f'    <tr><td>Nombre de destinations</td><td>{n_dest}</td><td>Voir la grille ci-dessous</td></tr>\n'
        '    <tr><td>Délai de réservation</td><td>5 à 14 jours</td><td>Selon la destination et la saison</td></tr>\n'
        '  </tbody>\n'
        '</table>'
    )
    if price_note:
        html += f"\n\n<p>{price_note}</p>"
    return html


def build_specs_list(top_specs: list) -> str:
    items = []
    for s in top_specs:
        s = clean_text(s)
        if s and len(s) < 250:
            items.append(f"  <li>{s}</li>")
    if not items:
        return "  <li>Encadrement par un professionnel local</li>\n  <li>Matériel et sécurité fournis</li>"
    return "\n".join(items)


def build_destinations_compare(hub: str, samples: list, slug: str) -> str:
    """samples = liste de tuples (dest, text)"""
    items = []
    for dest, text in samples:
        if not (dest and text):
            continue
        text_short = clean_text(text)[:280]
        if len(text_short) < 80:
            continue
        # Lien vers la page activité×destination (pattern crazy-evg)
        dest_slug = re.sub(r"[^a-z0-9]+", "-", dest.lower()).strip("-")
        link = f"https://www.crazy-evg.com/enterrement-de-vie-de-garcon-{dest_slug}/{slug.replace('-evg', '')}-activites"
        label = f"{hub} EVG à {dest}"
        items.append(f'  <li><strong><a href="{link}">{label}</a></strong> — {text_short}</li>')
    if not items:
        return "  <li>Comparatif à enrichir manuellement à partir des descriptions par destination.</li>"
    return "\n".join(items)


def build_sister_links(hub: str) -> str:
    slugs = SISTER_HUBS.get(hub, [])
    items = []
    for s in slugs:
        label = SLUG_TO_LABEL.get(s, s)
        items.append(f'  <li><a href="https://www.crazy-evg.com/activity-category/{s}">{label}</a></li>')
    return "\n".join(items)


def build_faq(hub: str, mc: str, h1: str, n_dest: int, dest_list: str, low: int, high: int, unit: str) -> str:
    activite = hub.lower()
    if unit == "person":
        prix_str = f"<strong>entre {low} € et {high} € par personne</strong>"
    else:
        prix_str = f"<strong>entre {low} € et {high} € en forfait pour le groupe entier</strong>"

    qa = [
        (
            f"Combien coûte un {activite} pour un EVG ?",
            f"Le tarif d'un {activite} EVG est compris {prix_str}. Le prix varie selon la destination, la taille du groupe et les options choisies. Demandez un <a href=\"https://www.crazy-evg.com/devis\">devis en 1 minute</a> pour un tarif personnalisé."
        ),
        (
            f"Combien de temps dure un {activite} EVG ?",
            f"La durée varie selon la formule, généralement <strong>entre 1h et 4h transferts inclus</strong>. Consultez la fiche détaillée de chaque destination pour le programme précis."
        ),
        (
            f"Faut-il un niveau particulier pour faire un {activite} EVG ?",
            f"Aucun niveau requis. Toutes nos sessions sont <strong>encadrées par un instructeur professionnel</strong> qui assure le briefing et l'accompagnement. L'activité est accessible aux débutants."
        ),
        (
            f"À partir de combien de personnes peut-on réserver un {activite} EVG ?",
            f"La majorité de nos partenaires acceptent les groupes <strong>à partir de 4 à 6 personnes</strong>. Au-delà de 12-15 participants, plusieurs créneaux sont organisés. Les conditions exactes varient selon la destination."
        ),
        (
            f"Que faut-il prévoir pour un {activite} EVG ?",
            f"Une <strong>pièce d'identité valide</strong> est généralement demandée. Le matériel et l'encadrement sont fournis par notre partenaire local. Prévoyez une tenue adaptée et des chaussures fermées. Détails complets fournis à la réservation."
        ),
        (
            f"Dans quelles villes peut-on faire un {activite} EVG ?",
            f"L'activité est disponible dans <strong>{n_dest} destinations</strong> Crazy-EVG : {dest_list}."
        ),
        (
            f"Comment réserver un {activite} EVG ?",
            f"Demandez un <a href=\"https://www.crazy-evg.com/devis\">devis en 1 minute</a> sur Crazy-EVG. Notre équipe revient vers vous sous 24h avec un programme sur mesure et un tarif détaillé pour votre groupe."
        ),
    ]
    parts = []
    for q, a in qa:
        parts.append(f"<h3>{q}</h3>\n<p>{a}</p>")
    return "\n\n".join(parts)


def build_experience_section(exp_intro: str, samples: list) -> str:
    """Construit le bloc C 'L'expérience en détail' à partir des sample descriptions."""
    paragraphs = [f"<p>{exp_intro}</p>"]
    for i, (dest, text) in enumerate(samples[:2]):
        text_clean = clean_text(text)
        if text_clean and len(text_clean) > 100:
            # Tronque à ~280 caractères, fin sur un point
            cut = text_clean[:300]
            last_dot = cut.rfind(".")
            if last_dot > 150:
                cut = cut[:last_dot + 1]
            paragraphs.append(f"<p><strong>À {dest} :</strong> {cut}</p>")
    return "\n".join(paragraphs)


def render_html(meta: dict, enriched: dict) -> str:
    hub = meta["hub"]
    url = meta["URL"]
    slug = slug_from_url(url)
    h1 = meta["h1_suggested"]
    title = meta["new_title"]
    meta_desc = meta["new_meta"]
    mc = meta["mc_principal"]

    config = HUB_CONFIG.get(hub, {})
    intro_p1 = config.get("intro_p1", f"<p>Le <strong>{hub} EVG</strong> est l'une des activités phares du catalogue Crazy-EVG.</p>")
    intro_p2 = config.get("intro_p2", "")
    why_args = config.get("why_args", [])
    exp_intro = config.get("exp_intro", "Programme type :")
    price_note = config.get("price_note", "")

    destinations = [d.strip() for d in enriched["destinations"].split("|") if d.strip()]
    n_dest = len(destinations)
    dest_list_text = ", ".join(destinations) if destinations else "destinations à venir"
    top_specs = [s.strip() for s in enriched["top_specs"].split("||") if s.strip()][:10]

    samples = []
    for k_dest, k_text in [
        ("sample_desc_1_dest", "sample_desc_1_text"),
        ("sample_desc_2_dest", "sample_desc_2_text"),
        ("sample_desc_3_dest", "sample_desc_3_text"),
    ]:
        d = enriched.get(k_dest, "").strip()
        t = enriched.get(k_text, "").strip()
        if d or t:
            samples.append((d, t))

    low, high, unit = PRICES.get(hub, (50, 150, "person"))

    why_html = "\n".join(f"  <li>{a}</li>" for a in why_args) if why_args else (
        "  <li><strong>Activité unique :</strong> peu de groupes la proposent.</li>\n"
        "  <li><strong>Encadrement pro :</strong> sécurité et confort garantis.</li>\n"
        "  <li><strong>Adapté aux groupes EVG :</strong> tarif et logistique optimisés.</li>"
    )

    exp_html = build_experience_section(exp_intro, samples)
    specs_html = build_specs_list(top_specs)
    pricing_html = build_pricing_table(low, high, unit, n_dest, hub, price_note)
    destinations_intro = (
        f"<p>L'activité <strong>{h1}</strong> est disponible dans "
        f"<strong>{n_dest} destinations</strong> Crazy-EVG : {dest_list_text}."
        f"</p>"
    )
    compare_html = build_destinations_compare(hub, samples, slug)
    sister_html = build_sister_links(hub)
    faq_html = build_faq(hub, mc, h1, n_dest, dest_list_text, low, high, unit)

    return f"""<!-- Page: {url} -->
<!-- Title: {title} -->
<!-- Meta: {meta_desc} -->

<h1>{h1}</h1>

<!-- BLOC A — Introduction -->
<p>{intro_p1}</p>
{f'<p>{intro_p2}</p>' if intro_p2 else ''}

<!-- BLOC B — Pourquoi choisir -->
<h2>Pourquoi choisir le {hub.lower()} pour son EVG ?</h2>
<ul>
{why_html}
</ul>

<!-- BLOC C — L'expérience en détail -->
<h2>L'expérience {hub.lower()} en détail</h2>
{exp_html}

<!-- BLOC D — Ce qui est inclus -->
<h2>Ce qui est inclus dans un {hub.lower()} EVG</h2>
<ul>
{specs_html}
</ul>

<!-- BLOC E — Tarif -->
<h2>Combien coûte un {hub.lower()} EVG ?</h2>
{pricing_html}

<!-- BLOC F — Destinations -->
<h2>Où faire un {hub.lower()} pour un EVG ?</h2>
{destinations_intro}

<!-- BLOC G — Comparatif destinations -->
<h3>Comparatif rapide des destinations</h3>
<ul>
{compare_html}
</ul>

<!-- BLOC H — Activités liées -->
<h2>Ces activités EVG vont aussi vous plaire</h2>
<ul>
{sister_html}
</ul>

<!-- BLOC I — FAQ -->
<h2>FAQ — {h1}</h2>

{faq_html}
"""


def main():
    with open("seo-optimization/exports/titles_metas.csv", "r", encoding="utf-8") as fp:
        metas = list(csv.DictReader(fp))

    with open("seo-optimization/exports/hubs_enriched.csv", "r", encoding="utf-8") as fp:
        enriched_by_hub = {r["hub"]: r for r in csv.DictReader(fp)}

    target = sys.argv[1] if len(sys.argv) > 1 else "P2"

    written = 0
    skipped = []
    for m in metas:
        # On ne traite que les P2 par défaut, ou tout si arg "all"
        if target == "P2" and m["priorite"] != "P2 - Sleeping giant":
            continue
        if target == "P3" and m["priorite"] != "P3 - Cold page":
            continue

        hub = m["hub"]
        if hub not in enriched_by_hub:
            skipped.append(hub)
            continue

        html = render_html(m, enriched_by_hub[hub])
        slug = slug_from_url(m["URL"])
        out_path = os.path.join(OUT_DIR, f"{slug}.html")
        with open(out_path, "w", encoding="utf-8") as fp:
            fp.write(html)
        written += 1

    print(f"✓ {written} pages HTML générées dans {OUT_DIR} (target={target})")
    if skipped:
        print(f"⚠ Skipped: {skipped}")


if __name__ == "__main__":
    main()
