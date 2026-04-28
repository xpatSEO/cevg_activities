# SEO Optimization — Hubs activités Crazy-EVG

Plan d'optimisation SEO complet pour les 42 pages `/activity-category/<slug>` du site `crazy-evg.com`.

## Arborescence

```
seo-optimization/
├── README.md                          (ce fichier)
├── aggregate.py                       Croise fichiers 1 et 2 → CSV enrichi
├── generate_titles_metas.py           Produit le CSV des 42 Title/Meta
├── generate_jsonld.py                 Génère 42 fichiers JSON-LD (Service+FAQ+Breadcrumb)
├── generate_p2_sheets.py              Génère 27 fiches de production P2
├── generate_html.py                   Génère HTML pour P2 (27) + P3 (8) — 35 pages
├── build_master_csv.py                Consolide les 42 pages dans master.csv
├── hub_config_p2_batch{1..5}.py       Seeds éditoriaux P2 (intro, args, exp_intro)
├── hub_config_p3.py                   Seeds éditoriaux P3
├── briefs/
│   ├── GABARIT-EDITORIAL.md           Gabarit réutilisable (9 blocs, patterns, checklist)
│   └── P3-DECISIONS.md                Décisions par page froide (optimiser/fusionner/désindexer)
├── pilots/                            7 pages P1 rédigées en plein (HTML prêt à coller)
│   ├── 01-shooting-evg.md
│   ├── 02-kidnapping-evg.md
│   ├── 03-corrida-evg.md
│   ├── 04-sexy-reveil-evg.md
│   ├── 05-striptease-domicile-evg.md
│   ├── 06-car-smash-evg.md
│   └── 07-conduite-char-d-assaut-evg.md
├── p2-sheets/                         27 fiches de production P2 (Title/Meta/data/maillage)
│   └── *.md                           Une fiche par hub, pour le rédacteur
├── schema/
│   ├── schema-template.json           Template JSON-LD (placeholders)
│   ├── schema-shooting-EXAMPLE.json   Exemple rempli (référence)
│   └── generated/                     42 fichiers JSON-LD prêts à injecter
│       └── *.json
├── html/                              35 pages HTML générées (P2 + P3)
│   └── *.html
└── exports/
    ├── hubs_enriched.csv              42 hubs × données agrégées du fichier 2
    ├── titles_metas.csv               42 nouveaux Title + Meta + priorité
    └── master.csv                     ⭐ Master consolidé : 42 pages × HTML × JSON-LD
```

## Reproduire les exports

```bash
python3 seo-optimization/aggregate.py
python3 seo-optimization/generate_titles_metas.py
python3 seo-optimization/generate_jsonld.py
python3 seo-optimization/generate_p2_sheets.py
python3 seo-optimization/generate_html.py P2     # 27 HTML P2
python3 seo-optimization/generate_html.py P3     # 8 HTML P3
python3 seo-optimization/build_master_csv.py     # ⭐ Master CSV consolidé
```

## Roadmap proposée

| Phase | Durée | Livrable |
|---|---|---|
| 1. Métas | 1 sem. | Déployer les 42 Title/Meta du CSV `titles_metas.csv` |
| 2. Quick wins (P1) | 3-4 sem. | 7 pilotes prêts à intégrer (Shooting, Kidnapping, Corrida, Réveil coquin, Strip-tease domicile, Car Smash, Char d'Assaut) |
| 3. Sleeping giants (P2) | 4-5 sem. | Rédiger 27 pages depuis `p2-sheets/` selon le gabarit |
| 4. Cold pages (P3) | 2 sem. | Appliquer les décisions de `briefs/P3-DECISIONS.md` (6 à optimiser, 1 fusion, 1 repositionnement) |
| 5. Schema | 1 sem. | Injecter les 42 JSON-LD de `schema/generated/` dans le `<head>` |
| 6. Audit | 6-8 sem. | Mesurer GSC : CTR, position, clics |

## Cas particuliers identifiés

- **Limousine + Hummer Lap Tour** → fusion + redirection 301 (cf. `briefs/P3-DECISIONS.md`)
- **Hydrospeed → Rafting** : fusion + redirection 301 (cf. `briefs/P3-DECISIONS.md`)
- **Footbulle vs Football** → vérifier la cannibalisation
- **9 pages "Optimisée"** dans le statut mais body vide à l'extraction → re-crawler pour vérifier
- **Fourchettes de prix** dans `generate_jsonld.py` et `generate_p2_sheets.py` : à valider avec le client avant déploiement Schema
