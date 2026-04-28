#!/usr/bin/env python3
"""
Génère 27 fiches de production Markdown — une par page P2 "sleeping giant".

Chaque fiche regroupe les éléments spécifiques à la page (Title/Meta/H1, destinations,
specs, comparatif rapide, sister hubs, FAQ skeleton) pour que le rédacteur puisse
produire le HTML final en suivant le gabarit éditorial GABARIT-EDITORIAL.md.

Sortie: seo-optimization/p2-sheets/{slug}.md
"""
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT_DIR = os.path.join(ROOT, "seo-optimization", "p2-sheets")
os.makedirs(OUT_DIR, exist_ok=True)

# Mapping hub -> liste de slugs frères pour le bloc H (maillage interne)
SISTER_HUBS = {
    "Parcours du Combattant": ["initiation-tir-shooting-evg", "airsoft-battle-evg",
                                "kidnapping-evg", "conduite-char-d-assaut-evg", "paintball-evg"],
    "Crazy Night": ["boite-bouteilles-evg", "stripclub-evg", "tournee-bars-evg",
                    "party-bus-strip-evg", "diner-strip-evg"],
    "Airsoft Battle": ["initiation-tir-shooting-evg", "paintball-evg",
                       "parcours-du-combattant-evg", "laser-game-evg",
                       "conduite-char-d-assaut-evg"],
    "Journee Ski": ["canyoning-evg", "rafting-eaux-vives-evg", "parapente-evg",
                    "saut-en-parachute-evg", "quad-buggy-evg"],
    "Degustation Bieres": ["beer-bike-evg", "tournee-bars-evg", "boite-bouteilles-evg",
                           "crazy-night-evg", "diner-strip-evg"],
    "Croisiere Bateau": ["jet-ski-evg", "flyboard-evg", "hydrospeed-evg",
                         "rafting-eaux-vives-evg", "party-bus-strip-evg"],
    "Boite Bouteilles": ["stripclub-evg", "crazy-night-evg", "tournee-bars-evg",
                         "party-bus-strip-evg", "diner-strip-evg"],
    "Football": ["footbulle-evg", "karting-evg", "paintball-evg",
                 "laser-game-evg", "airsoft-battle-evg"],
    "Diner Strip": ["striptease-domicile-evg", "stripclub-evg", "sexy-reveil-evg",
                    "party-bus-strip-evg", "crazy-night-evg"],
    "Poker Sexy": ["striptease-domicile-evg", "stripclub-evg", "sexy-combat-evg",
                   "diner-strip-evg", "crazy-night-evg"],
    "Combat Chien": ["kidnapping-evg", "parcours-du-combattant-evg",
                     "initiation-tir-shooting-evg", "airsoft-battle-evg",
                     "sexy-combat-evg"],
    "Tournee Bars": ["beer-bike-evg", "boite-bouteilles-evg", "crazy-night-evg",
                     "degustation-bieres-evg", "party-bus-strip-evg"],
    "Party Bus Strip": ["striptease-domicile-evg", "stripclub-evg", "diner-strip-evg",
                        "limousine-evg", "tournee-bars-evg"],
    "Quad Buggy": ["karting-evg", "conduite-char-d-assaut-evg",
                   "rafting-eaux-vives-evg", "canyoning-evg", "jet-ski-evg"],
    "Flyboard": ["jet-ski-evg", "croisiere-bateau-evg", "hydrospeed-evg",
                 "parapente-evg", "rafting-eaux-vives-evg"],
    "Karting": ["quad-buggy-evg", "conduite-ferrari-evg", "conduite-char-d-assaut-evg",
                "paintball-evg", "footbulle-evg"],
    "Jet Ski": ["flyboard-evg", "croisiere-bateau-evg", "hydrospeed-evg",
                "rafting-eaux-vives-evg", "quad-buggy-evg"],
    "Footbulle": ["football-evg", "paintball-evg", "laser-game-evg",
                  "karting-evg", "airsoft-battle-evg"],
    "Beer Bike": ["tournee-bars-evg", "boite-bouteilles-evg", "degustation-bieres-evg",
                  "limousine-evg", "crazy-night-evg"],
    "Hummer Lap Tour": ["limousine-evg", "party-bus-strip-evg", "stripclub-evg",
                        "boite-bouteilles-evg", "tournee-bars-evg"],
    "Limousine": ["hummer-lap-tour-evg", "party-bus-strip-evg", "stripclub-evg",
                  "boite-bouteilles-evg", "tournee-bars-evg"],
    "Stripclub": ["striptease-domicile-evg", "diner-strip-evg", "sexy-reveil-evg",
                  "party-bus-strip-evg", "crazy-night-evg"],
    "Saut Elastique": ["faux-saut-elastique-evg", "saut-en-parachute-evg",
                       "chute-libre-evg", "canyoning-evg", "parapente-evg"],
    "Sexy Combat": ["combat-chien-evg", "kidnapping-evg", "sexy-reveil-evg",
                    "striptease-domicile-evg", "poker-sexy-evg"],
    "Chute Libre": ["saut-en-parachute-evg", "saut-elastique-evg", "parapente-evg",
                    "flyboard-evg", "canyoning-evg"],
    "Paintball": ["airsoft-battle-evg", "laser-game-evg", "parcours-du-combattant-evg",
                  "initiation-tir-shooting-evg", "football-evg"],
    "Faux Saut Elastique": ["saut-elastique-evg", "kidnapping-evg",
                            "parcours-du-combattant-evg", "sexy-reveil-evg",
                            "faux-saut-elastique-evg"],
}

PRICES = {
    "Parcours du Combattant": (89, 159, "person"),
    "Crazy Night": (89, 199, "person"),
    "Airsoft Battle": (35, 79, "person"),
    "Journee Ski": (79, 149, "person"),
    "Degustation Bieres": (29, 59, "person"),
    "Croisiere Bateau": (39, 119, "person"),
    "Boite Bouteilles": (29, 99, "person"),
    "Football": (19, 49, "person"),
    "Diner Strip": (49, 99, "person"),
    "Poker Sexy": (180, 320, "group"),
    "Combat Chien": (49, 89, "person"),
    "Tournee Bars": (29, 79, "person"),
    "Party Bus Strip": (49, 99, "person"),
    "Quad Buggy": (79, 159, "person"),
    "Flyboard": (79, 159, "person"),
    "Karting": (29, 59, "person"),
    "Jet Ski": (49, 119, "person"),
    "Footbulle": (19, 39, "person"),
    "Beer Bike": (29, 49, "person"),
    "Hummer Lap Tour": (49, 119, "person"),
    "Limousine": (39, 89, "person"),
    "Stripclub": (39, 99, "person"),
    "Saut Elastique": (89, 149, "person"),
    "Sexy Combat": (180, 320, "group"),
    "Chute Libre": (59, 99, "person"),
    "Paintball": (29, 59, "person"),
    "Faux Saut Elastique": (180, 350, "group"),
}


# Slug -> label propre pour affichage des liens internes
SLUG_TO_LABEL = {
    "initiation-tir-shooting-evg": "Stand de tir EVG",
    "kidnapping-evg": "Kidnapping EVG",
    "parcours-du-combattant-evg": "Parcours du combattant EVG",
    "corrida-evg": "Corrida EVG",
    "conduite-ferrari-evg": "Conduite Ferrari EVG",
    "striptease-domicile-evg": "Strip-tease à domicile EVG",
    "car-smash-evg": "Car Smash EVG",
    "conduite-char-d-assaut-evg": "Conduite char d'assaut EVG",
    "sexy-reveil-evg": "Réveil coquin EVG",
    "crazy-night-evg": "Crazy Night EVG",
    "airsoft-battle-evg": "Airsoft battle EVG",
    "journee-ski-evg": "EVG au ski",
    "degustation-bieres-evg": "Dégustation de bières EVG",
    "croisiere-bateau-evg": "Croisière en bateau EVG",
    "boite-bouteilles-evg": "Boîte et bouteilles EVG",
    "football-evg": "Football EVG",
    "diner-strip-evg": "Dîner strip EVG",
    "poker-sexy-evg": "Strip poker EVG",
    "combat-chien-evg": "Combat Man vs Dog EVG",
    "tournee-bars-evg": "Tournée des bars EVG",
    "party-bus-strip-evg": "Bus strip EVG",
    "quad-buggy-evg": "Quad & buggy EVG",
    "flyboard-evg": "Flyboard EVG",
    "karting-evg": "Karting EVG",
    "jet-ski-evg": "Jet ski EVG",
    "footbulle-evg": "Bubble foot EVG",
    "beer-bike-evg": "Beer bike EVG",
    "hummer-lap-tour-evg": "Limousine Hummer EVG",
    "limousine-evg": "Limousine EVG",
    "stripclub-evg": "Club strip-tease EVG",
    "parapente-evg": "Parapente EVG",
    "saut-elastique-evg": "Saut à l'élastique EVG",
    "sexy-combat-evg": "Combat sexy EVG",
    "chute-libre-evg": "Chute libre EVG",
    "paintball-evg": "Paintball EVG",
    "laser-game-evg": "Laser game EVG",
    "faux-saut-elastique-evg": "Faux saut à l'élastique EVG",
    "canyoning-evg": "Canyoning EVG",
    "saut-en-parachute-evg": "Saut en parachute EVG",
    "escape-room-evg": "Escape game EVG",
    "hydrospeed-evg": "Hydrospeed EVG",
    "rafting-eaux-vives-evg": "Rafting EVG",
}


def slug_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def render_sheet(meta: dict, enriched: dict, base_row: dict) -> str:
    hub = meta["hub"]
    url = meta["URL"]
    h1 = meta["h1_suggested"]
    title = meta["new_title"]
    meta_desc = meta["new_meta"]
    mc = meta["mc_principal"]
    statut = meta["statut"]
    pos = base_row["Position"]
    clicks = base_row["Clicks"]
    impr = base_row["Impressions"]

    destinations = [d.strip() for d in enriched["destinations"].split("|") if d.strip()]
    n_dest = len(destinations)
    top_specs = [s.strip() for s in enriched["top_specs"].split("||") if s.strip()][:8]

    s1_dest = enriched.get("sample_desc_1_dest", "").strip()
    s1_text = enriched.get("sample_desc_1_text", "").strip()
    s2_dest = enriched.get("sample_desc_2_dest", "").strip()
    s2_text = enriched.get("sample_desc_2_text", "").strip()
    s3_dest = enriched.get("sample_desc_3_dest", "").strip()
    s3_text = enriched.get("sample_desc_3_text", "").strip()

    low, high, unit = PRICES.get(hub, (0, 0, "person"))
    price_unit_label = "par personne" if unit == "person" else "en forfait pour le groupe"

    sister_slugs = SISTER_HUBS.get(hub, [])
    sister_links = "\n".join(
        f"- [{SLUG_TO_LABEL.get(slug, slug)}](https://www.crazy-evg.com/activity-category/{slug})"
        for slug in sister_slugs
    )

    specs_md = "\n".join(f"- {s}" for s in top_specs)

    dest_compare = ""
    if s1_dest and s1_text:
        dest_compare += f"- **{hub} EVG à {s1_dest}** — {s1_text[:300]}\n"
    if s2_dest and s2_text:
        dest_compare += f"- **{hub} EVG à {s2_dest}** — {s2_text[:300]}\n"
    if s3_dest and s3_text:
        dest_compare += f"- **{hub} EVG à {s3_dest}** — {s3_text[:300]}\n"

    return f"""# Fiche de production P2 — `{slug_from_url(url)}`

> **Hub** : {hub}
> **Mot-clé principal** : `{mc}`
> **Position actuelle** : {pos} · **Clicks** : {clicks} · **Impressions** : {impr}
> **Statut actuel** : {statut or "(vide)"}
> **Priorité** : P2 - Sleeping giant
> **Destinations couvertes (fichier 2)** : {n_dest}

---

## 1. Balises meta (à appliquer)

| Champ | Contenu | Long. |
|---|---|---|
| **Title** | `{title}` | {len(title)} |
| **Meta description** | `{meta_desc}` | {len(meta_desc)} |
| **H1** | `{h1}` | — |
| **URL canonique** | `{url}` | — |

---

## 2. Données disponibles (sources fichier 2)

### Destinations couvertes ({n_dest})
{', '.join(destinations) if destinations else '(aucune dans le fichier 2)'}

### Top specs récurrentes (à intégrer dans le Bloc D "Ce qui est inclus")
{specs_md if specs_md else '(à enrichir manuellement)'}

### Comparatif rapide des destinations (à utiliser dans le Bloc G)
{dest_compare if dest_compare else '(données limitées — étoffer manuellement)'}

---

## 3. Bloc E — Tarif type (à valider avec le client)

| Critère | Fourchette |
|---|---|
| Tarif | **{low} € à {high} € {price_unit_label}** |
| Devise | EUR |
| Délai de réservation | 7 à 14 jours selon destination |

---

## 4. Bloc H — Maillage interne suggéré (sister hubs)

{sister_links}

---

## 5. Bloc I — FAQ skeleton (7 questions à rédiger)

1. Combien coûte un {hub.lower()} pour un EVG ?
2. Combien de temps dure un {hub.lower()} EVG ?
3. Faut-il un niveau particulier pour faire un {hub.lower()} EVG ?
4. À partir de combien de personnes peut-on réserver un {hub.lower()} EVG ?
5. Que faut-il prévoir pour un {hub.lower()} EVG ?
6. Dans quelles villes peut-on faire un {hub.lower()} EVG ?
7. Comment réserver un {hub.lower()} EVG ?

→ Voir les 7 pages pilotes (`pilots/01` à `pilots/07`) pour des exemples de formulation et la profondeur de réponse attendue (40-80 mots/réponse).

---

## 6. Checklist de production

- [ ] Title et Meta appliqués (col. `new_title` et `new_meta` de `titles_metas.csv`)
- [ ] H1 réécrit avec le mot-clé principal
- [ ] Intro (2 paragraphes, 120-180 mots) avec mot-clé principal et 1-2 variantes
- [ ] Bloc B "Pourquoi choisir" (4 arguments, 150-200 mots)
- [ ] Bloc C "Comment ça se déroule" (200-280 mots, basé sur les sample descriptions)
- [ ] Bloc D "Ce qui est inclus" (8-12 bullets, à partir des top specs)
- [ ] Bloc E tableau tarif + durée + groupe
- [ ] Bloc F intro destinations (mention des {n_dest} villes)
- [ ] Bloc G comparatif des 4-5 destinations stars
- [ ] Bloc H 5 sister hubs (liste ci-dessus)
- [ ] Bloc I FAQ 7 questions (40-80 mots/réponse)
- [ ] JSON-LD injecté (cf. `schema/generated/{slug_from_url(url)}.json`)
- [ ] Image principale avec alt = mot-clé principal
- [ ] 800-1100 mots utiles au total
"""


def main():
    with open("seo-optimization/exports/titles_metas.csv", "r", encoding="utf-8") as fp:
        metas = list(csv.DictReader(fp))

    with open("seo-optimization/exports/hubs_enriched.csv", "r", encoding="utf-8") as fp:
        enriched_by_hub = {r["hub"]: r for r in csv.DictReader(fp)}

    import glob
    f1 = [f for f in glob.glob("*.csv") if "GenAI" in f][0]
    with open(f1, "r", encoding="utf-8") as fp:
        base_by_hub = {r["Nom activité"]: r for r in csv.DictReader(fp)}

    written = 0
    for m in metas:
        if m["priorite"] != "P2 - Sleeping giant":
            continue
        hub = m["hub"]
        if hub not in enriched_by_hub:
            print(f"⚠ {hub}: pas de data enrichie")
            continue
        sheet = render_sheet(m, enriched_by_hub[hub], base_by_hub[hub])
        slug = slug_from_url(m["URL"])
        out_path = os.path.join(OUT_DIR, f"{slug}.md")
        with open(out_path, "w", encoding="utf-8") as fp:
            fp.write(sheet)
        written += 1

    print(f"✓ {written}/27 fiches P2 générées dans {OUT_DIR}")


if __name__ == "__main__":
    main()
