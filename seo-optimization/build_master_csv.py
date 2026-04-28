#!/usr/bin/env python3
"""
Construit le master CSV consolidé avec, pour chaque page :
- URL, slug, hub, mot-clé, statut, priorité
- Title actuel et nouveau, Meta actuelle et nouvelle, H1
- Stats actuelles (clicks, impressions, position)
- HTML complet (extrait des pilots/*.md pour P1, depuis html/*.html pour P2/P3)
- JSON-LD complet (depuis schema/generated/{slug}.json)

Sortie: seo-optimization/exports/master.csv
"""
import csv
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT = os.path.join(ROOT, "seo-optimization", "exports", "master.csv")


def slug_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def extract_html_from_pilot(md_path: str) -> str:
    """Extrait le bloc ```html ... ``` d'un fichier pilot."""
    with open(md_path, "r", encoding="utf-8") as fp:
        content = fp.read()
    # Match ```html ... ```
    match = re.search(r"```html\n(.*?)\n```", content, flags=re.S)
    if match:
        return match.group(1).strip()
    return ""


def find_pilot_path(slug: str) -> str:
    """Cherche le pilot file correspondant au slug."""
    for f in glob.glob("seo-optimization/pilots/*.md"):
        # Le nom du fichier contient le slug (ex: 01-shooting-evg.md -> shooting-evg)
        base = os.path.basename(f).replace(".md", "")
        # Remove leading "NN-"
        clean = re.sub(r"^\d+-", "", base)
        if clean == slug or slug.replace("initiation-tir-", "") in clean or clean.replace("char-d-assaut", "char-d-assaut") in slug:
            return f
    return ""


# Mapping explicite slug -> pilot file (plus fiable que le matching auto)
PILOT_FILES = {
    "initiation-tir-shooting-evg": "seo-optimization/pilots/01-shooting-evg.md",
    "kidnapping-evg": "seo-optimization/pilots/02-kidnapping-evg.md",
    "corrida-evg": "seo-optimization/pilots/03-corrida-evg.md",
    "sexy-reveil-evg": "seo-optimization/pilots/04-sexy-reveil-evg.md",
    "striptease-domicile-evg": "seo-optimization/pilots/05-striptease-domicile-evg.md",
    "car-smash-evg": "seo-optimization/pilots/06-car-smash-evg.md",
    "conduite-char-d-assaut-evg": "seo-optimization/pilots/07-conduite-char-d-assaut-evg.md",
}


def main():
    # Charge titles_metas (déjà priorisés)
    with open("seo-optimization/exports/titles_metas.csv", "r", encoding="utf-8") as fp:
        metas = list(csv.DictReader(fp))

    # Charge stats du fichier 1
    f1 = [f for f in glob.glob("*.csv") if "GenAI" in f][0]
    with open(f1, "r", encoding="utf-8") as fp:
        base_by_hub = {r["Nom activité"]: r for r in csv.DictReader(fp)}

    rows_out = []
    missing_html = []
    missing_json = []

    for m in metas:
        hub = m["hub"]
        url = m["URL"]
        slug = slug_from_url(url)
        b = base_by_hub.get(hub, {})

        # Récupérer le HTML
        html = ""
        if slug in PILOT_FILES:
            html = extract_html_from_pilot(PILOT_FILES[slug])
        else:
            html_path = f"seo-optimization/html/{slug}.html"
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as fp:
                    html = fp.read()
        if not html:
            missing_html.append(slug)

        # Récupérer le JSON-LD
        json_str = ""
        json_path = f"seo-optimization/schema/generated/{slug}.json"
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as fp:
                json_str = fp.read().strip()
        else:
            missing_json.append(slug)

        rows_out.append({
            "URL": url,
            "slug": slug,
            "hub": hub,
            "priorite": m["priorite"],
            "statut_initial": b.get("Statut", ""),
            "mc_principal": m["mc_principal"],
            "current_title": m["current_title"],
            "current_meta": m["current_meta"],
            "new_title": m["new_title"],
            "new_title_len": m["new_title_len"],
            "new_meta": m["new_meta"],
            "new_meta_len": m["new_meta_len"],
            "h1_suggested": m["h1_suggested"],
            "clicks": b.get("Clicks", ""),
            "impressions": b.get("Impressions", ""),
            "ctr": b.get("CTR", ""),
            "position": b.get("Position", ""),
            "html": html,
            "html_word_count": len(html.split()),
            "jsonld": json_str,
            "jsonld_size_bytes": len(json_str.encode("utf-8")),
        })

    fieldnames = list(rows_out[0].keys())
    with open(OUT, "w", encoding="utf-8", newline="") as fp:
        # quoting ALL pour gérer correctement les retours ligne dans HTML/JSON
        writer = csv.DictWriter(fp, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"✓ Master CSV généré: {OUT}")
    print(f"  Pages: {len(rows_out)}/42")
    by_prio = {}
    for r in rows_out:
        by_prio.setdefault(r["priorite"], 0)
        by_prio[r["priorite"]] += 1
    for p, n in sorted(by_prio.items()):
        print(f"  {p}: {n}")
    if missing_html:
        print(f"⚠ HTML manquant pour: {missing_html}")
    if missing_json:
        print(f"⚠ JSON-LD manquant pour: {missing_json}")

    # Stats
    avg_words = sum(r["html_word_count"] for r in rows_out) / len(rows_out)
    print(f"\n  Mots moyens / page : {avg_words:.0f}")
    total_html_bytes = sum(len(r["html"].encode("utf-8")) for r in rows_out)
    total_json_bytes = sum(r["jsonld_size_bytes"] for r in rows_out)
    print(f"  Total HTML : {total_html_bytes/1024:.0f} KB")
    print(f"  Total JSON-LD : {total_json_bytes/1024:.0f} KB")


if __name__ == "__main__":
    main()
