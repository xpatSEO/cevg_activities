#!/usr/bin/env python3
"""
Agrège pour chaque hub d'activité (fichier 1) les données par destination
issues du fichier 2 (1857 lignes activité×destination).

Sortie: seo-optimization/exports/hubs_enriched.csv
"""
import csv
import glob
import os
import re
from collections import defaultdict
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

F1 = [f for f in glob.glob("*.csv") if "GenAI" in f][0]
F2 = [f for f in glob.glob("*.csv") if "crazy" in f][0]
OUT_DIR = os.path.join(ROOT, "seo-optimization", "exports")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Mapping hub -> patterns d'activités à matcher dans fichier 2
# ---------------------------------------------------------------------------
HUB_TO_PATTERNS = {
    # PATTERNS TRES SPECIFIQUES EN PREMIER (composés / variantes)
    "Faux Saut Elastique": [r"faux.*saut.*[ée]lastique", r"fake.*bungee"],
    "Hummer Lap Tour": [r"hummer"],
    "Footbulle": [r"foot.?bulle", r"bubble.?foot"],
    "Party Bus Strip": [r"party bus.*strip", r"bus.*strip", r"strip.*bus"],
    "Diner Strip": [r"d[îi]ner.*strip", r"diner.*strip", r"repas.*strip"],
    "Striptease Domicile": [r"striptease.*(domicile|appart|h[ôo]tel)", r"strip.*(domicile|appart)", r"^striptease$", r"striptease "],
    "Stripclub": [r"strip.?club", r"club.*strip"],
    "Sexy Combat": [r"sexy.*combat", r"combat.*sexy", r"lutte.*sexy", r"jelly.*wrestling"],
    "Sexy Reveil": [r"r[ée]veil.*(coquin|sexy|strip)", r"sexy.*r[ée]veil"],
    "Poker Sexy": [r"poker.*sexy", r"sexy.*poker", r"strip poker"],
    "Combat Chien": [r"combat.*chien", r"man.*vs.*dog"],
    "Conduite Char D Assaut": [r"char d.assaut", r"conduite.*char", r"\btank\b"],
    "Conduite Ferrari": [r"\bferrari\b"],
    "Parcours du Combattant": [r"parcours.*combattant", r"stage commando", r"journ[ée]e commando"],
    "Initiation Tir Shooting": [r"\bshooting\b", r"\btir\b.*\b(arme|balle|sniper|ak)"],
    "Kidnapping": [r"kidnapp", r"fausse arrestation", r"faux kidnap"],
    "Beer Bike": [r"beer.?bike", r"v[ée]lo.*bi[èe]re"],
    "Tournee Bars": [r"tourn[ée]e.*bars?", r"bar crawl", r"pub crawl"],
    "Boite Bouteilles": [r"bo[îi]te.*bouteille", r"boite.*bouteille", r"entr[ée]e.*bo[îi]te"],
    "Degustation Bieres": [r"d[ée]gustation.*bi[èe]re", r"bi[èe]re.*d[ée]gustation", r"atelier.*bi[èe]re"],
    "Crazy Night": [r"crazy night"],
    "Croisiere Bateau": [r"croisi[èe]re"],
    "Car Smash": [r"car smash", r"casser.*voiture"],
    "Corrida": [r"corrida", r"taureau"],
    "Airsoft Battle": [r"airsoft"],
    "Quad Buggy": [r"\bquad\b", r"\bbuggy\b"],
    "Flyboard": [r"flyboard", r"fly board"],
    "Jet Ski": [r"jet.?ski"],
    "Journee Ski": [r"journ[ée]e ski", r"crazy ski", r"cours de ski", r"location ski", r"ski indoor", r"forfait.*ski", r"ski pack"],
    "Karting": [r"karting", r"\bkart\b"],
    "Football": [r"foot 5", r"match.*foot", r"^football"],
    "Limousine": [r"limousine"],
    "Parapente": [r"parapente"],
    "Saut en Parachute": [r"saut.*parachute", r"parachutisme"],
    "Saut Elastique": [r"saut.*[ée]lastique", r"bungee"],
    "Chute Libre": [r"chute libre", r"simulateur.*chute"],
    "Paintball": [r"paintball"],
    "Laser Game": [r"laser.?game"],
    "Canyoning": [r"canyoning"],
    "Escape Room": [r"escape.?room", r"escape.?game"],
    "Hydrospeed": [r"hydrospeed", r"hydro.?speed"],
    "Rafting Eaux Vives": [r"rafting", r"eaux vives"],
}


# ---------------------------------------------------------------------------
def strip_html(html: str) -> str:
    """Supprime les balises HTML, garde le texte."""
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", " ", html)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_bullets(html: str) -> list:
    """Extrait les <li> du contenu (specs)."""
    if not html:
        return []
    items = re.findall(r"<li[^>]*>(.*?)</li>", html, flags=re.S | re.I)
    return [strip_html(i) for i in items if strip_html(i)]


def matches_hub(activity_name: str, patterns: list) -> bool:
    name_low = activity_name.lower()
    return any(re.search(p, name_low) for p in patterns)


# ---------------------------------------------------------------------------
def load_file2():
    rows = []
    with open(F2, "r", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        for r in reader:
            rows.append(r)
    return rows


def aggregate():
    file2_rows = load_file2()
    # index activity -> rows
    by_hub = defaultdict(list)
    for r in file2_rows:
        for hub, patterns in HUB_TO_PATTERNS.items():
            if matches_hub(r["activity_name"], patterns):
                by_hub[hub].append(r)
                break

    output = []
    for hub, patterns in HUB_TO_PATTERNS.items():
        matches = by_hub.get(hub, [])
        destinations = sorted({m["destination_name"] for m in matches if m["destination_name"]})

        # Aggregate bullets across all matched rows
        all_bullets = []
        for m in matches:
            bullets = extract_bullets(m["content"])
            all_bullets.extend(bullets)

        # Top recurring bullets (frequency)
        from collections import Counter
        bullet_counter = Counter(all_bullets)
        top_bullets = [b for b, c in bullet_counter.most_common(15)]

        # Sample descriptions (best 3, longest cleaned)
        descriptions = []
        for m in matches:
            txt = strip_html(m["presentation"]) or strip_html(m["description"])
            if txt and len(txt) > 80:
                descriptions.append((m["destination_name"], txt[:600]))
        descriptions.sort(key=lambda x: -len(x[1]))

        output.append({
            "hub": hub,
            "n_destinations_in_file2": len(destinations),
            "destinations": " | ".join(destinations),
            "n_bullets_aggregated": len(all_bullets),
            "top_specs": " || ".join(top_bullets[:10]),
            "sample_desc_1_dest": descriptions[0][0] if descriptions else "",
            "sample_desc_1_text": descriptions[0][1] if descriptions else "",
            "sample_desc_2_dest": descriptions[1][0] if len(descriptions) > 1 else "",
            "sample_desc_2_text": descriptions[1][1] if len(descriptions) > 1 else "",
            "sample_desc_3_dest": descriptions[2][0] if len(descriptions) > 2 else "",
            "sample_desc_3_text": descriptions[2][1] if len(descriptions) > 2 else "",
        })

    out_path = os.path.join(OUT_DIR, "hubs_enriched.csv")
    with open(out_path, "w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(output[0].keys()))
        writer.writeheader()
        writer.writerows(output)

    print(f"Wrote {out_path}")
    print(f"Hubs traités: {len(output)}")
    no_match = [o["hub"] for o in output if o["n_destinations_in_file2"] == 0]
    if no_match:
        print(f"⚠ Hubs sans match dans fichier 2: {no_match}")
    return output


if __name__ == "__main__":
    aggregate()
