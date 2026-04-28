#!/usr/bin/env python3
"""
Génère 42 fichiers JSON-LD (un par hub) à coller dans le <head> de chaque page.
Source: hubs_enriched.csv (destinations + specs) + titles_metas.csv (meta) + dict de prix interne.

Sortie: seo-optimization/schema/generated/{slug}.json (42 fichiers)
"""
import csv
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT_DIR = os.path.join(ROOT, "seo-optimization", "schema", "generated")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Fourchettes de prix par hub (en EUR). Tarifs estimés sur la base des données
# du fichier 2 + connaissance industrielle. À ajuster avec le client.
# Format: (low, high, unit) - unit = "person" (par personne) ou "group" (forfait groupe)
# ---------------------------------------------------------------------------
PRICES = {
    "Initiation Tir Shooting": (39, 129, "person"),
    "Kidnapping": (180, 450, "group"),
    "Parcours du Combattant": (89, 159, "person"),
    "Corrida": (120, 180, "person"),
    "Conduite Ferrari": (149, 349, "person"),
    "Striptease Domicile": (150, 350, "group"),
    "Car Smash": (59, 119, "person"),
    "Conduite Char D Assaut": (149, 290, "person"),
    "Sexy Reveil": (150, 280, "group"),
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
    "Parapente": (89, 159, "person"),
    "Saut Elastique": (89, 149, "person"),
    "Sexy Combat": (180, 320, "group"),
    "Chute Libre": (59, 99, "person"),
    "Paintball": (29, 59, "person"),
    "Laser Game": (19, 39, "person"),
    "Faux Saut Elastique": (180, 350, "group"),
    "Canyoning": (59, 99, "person"),
    "Saut en Parachute": (199, 299, "person"),
    "Escape Room": (19, 39, "person"),
    "Hydrospeed": (49, 99, "person"),
    "Rafting Eaux Vives": (49, 99, "person"),
}


# ---------------------------------------------------------------------------
# FAQ types (réponses génériques, à ajuster manuellement pour les pages
# pilotes déjà rédigées si on veut être plus précis).
# Le rédacteur peut surcharger ces réponses dans le HTML final.
# ---------------------------------------------------------------------------
def build_faq(hub: str, mc: str, n_dest: int, dest_list: str, low: int, high: int, unit: str) -> list:
    activite = hub.lower()
    if unit == "person":
        prix_str = f"entre {low} € et {high} € par personne"
    else:
        prix_str = f"entre {low} € et {high} € en forfait pour le groupe"

    return [
        {
            "@type": "Question",
            "name": f"Combien coûte un {activite} pour un EVG ?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"Le tarif d'un {activite} EVG est compris {prix_str}. Le prix varie selon la destination, la taille du groupe et les options choisies. Demandez un devis en 1 minute pour un tarif personnalisé."
            }
        },
        {
            "@type": "Question",
            "name": f"Combien de temps dure un {activite} EVG ?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"La durée varie selon la formule, généralement entre 1h et 4h transferts inclus. Consultez la fiche détaillée de chaque destination pour le programme précis."
            }
        },
        {
            "@type": "Question",
            "name": f"Faut-il un niveau particulier pour faire un {activite} EVG ?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"Aucun niveau requis. Toutes nos sessions sont encadrées par un instructeur professionnel qui assure le briefing et l'accompagnement. L'activité est accessible aux débutants."
            }
        },
        {
            "@type": "Question",
            "name": f"À partir de combien de personnes peut-on réserver un {activite} EVG ?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"La majorité de nos partenaires acceptent les groupes à partir de 4 à 6 personnes. Les conditions exactes varient selon la destination. Au-delà de 12-15 participants, plusieurs créneaux sont organisés."
            }
        },
        {
            "@type": "Question",
            "name": f"Que faut-il prévoir pour un {activite} EVG ?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"Une pièce d'identité valide est généralement demandée. Le matériel et l'encadrement sont fournis par notre partenaire local. Prévoyez une tenue adaptée et des chaussures fermées. Détails complets fournis à la réservation."
            }
        },
        {
            "@type": "Question",
            "name": f"Dans quelles villes peut-on faire un {activite} EVG ?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f"L'activité {activite} est disponible dans {n_dest} destinations Crazy-EVG : {dest_list}."
            }
        },
        {
            "@type": "Question",
            "name": f"Comment réserver un {activite} EVG ?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Demandez un devis en 1 minute sur Crazy-EVG. Notre équipe revient vers vous sous 24h avec un programme sur mesure et un tarif détaillé pour votre groupe."
            }
        },
    ]


def slug_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def build_jsonld(hub_data: dict, meta_data: dict) -> dict:
    hub = meta_data["hub"]
    url = meta_data["URL"]
    slug = slug_from_url(url)
    title_clean = meta_data["new_title"].split(" | ")[0]
    h1 = meta_data["h1_suggested"]
    meta_desc = meta_data["new_meta"]
    mc = meta_data["mc_principal"]

    destinations = [d.strip() for d in hub_data["destinations"].split("|") if d.strip()]
    n_dest = len(destinations)
    dest_list_text = ", ".join(destinations) if destinations else "destinations à venir"

    low, high, unit = PRICES[hub]

    area_served = [{"@type": "City", "name": d} for d in destinations]

    faq = build_faq(hub, h1, n_dest, dest_list_text, low, high, unit)

    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": f"{url}#service",
                "name": h1,
                "alternateName": mc,
                "description": meta_desc,
                "serviceType": "Activité EVG",
                "category": "Enterrement de vie de garçon",
                "url": url,
                "provider": {
                    "@type": "Organization",
                    "@id": "https://www.crazy-evg.com/#organization",
                    "name": "Crazy-EVG",
                    "url": "https://www.crazy-evg.com",
                    "telephone": "+33176215730",
                    "email": "contact@crazy-evg.com",
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": "8 rue du Faubourg Poissonnière",
                        "postalCode": "75010",
                        "addressLocality": "Paris",
                        "addressCountry": "FR"
                    }
                },
                "areaServed": area_served,
                "audience": {
                    "@type": "Audience",
                    "audienceType": "Groupe d'amis - Enterrement de vie de garçon",
                    "suggestedMinAge": 18
                },
                "offers": {
                    "@type": "AggregateOffer",
                    "priceCurrency": "EUR",
                    "lowPrice": str(low),
                    "highPrice": str(high),
                    "offerCount": str(n_dest) if n_dest else "1",
                    "availability": "https://schema.org/InStock"
                }
            },
            {
                "@type": "FAQPage",
                "@id": f"{url}#faq",
                "mainEntity": faq
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Accueil",
                     "item": "https://www.crazy-evg.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Activités EVG",
                     "item": "https://www.crazy-evg.com/activites-evg"},
                    {"@type": "ListItem", "position": 3, "name": title_clean,
                     "item": url}
                ]
            }
        ]
    }


def main():
    enriched = {}
    with open("seo-optimization/exports/hubs_enriched.csv", "r", encoding="utf-8") as fp:
        for r in csv.DictReader(fp):
            enriched[r["hub"]] = r

    with open("seo-optimization/exports/titles_metas.csv", "r", encoding="utf-8") as fp:
        metas = list(csv.DictReader(fp))

    written = 0
    for m in metas:
        hub = m["hub"]
        if hub not in enriched:
            print(f"⚠ {hub}: pas de data enrichie")
            continue
        if hub not in PRICES:
            print(f"⚠ {hub}: pas de fourchette de prix")
            continue

        jsonld = build_jsonld(enriched[hub], m)
        slug = slug_from_url(m["URL"])
        out_path = os.path.join(OUT_DIR, f"{slug}.json")
        with open(out_path, "w", encoding="utf-8") as fp:
            json.dump(jsonld, fp, ensure_ascii=False, indent=2)
        written += 1

    print(f"✓ {written}/42 JSON-LD générés dans {OUT_DIR}")


if __name__ == "__main__":
    main()
