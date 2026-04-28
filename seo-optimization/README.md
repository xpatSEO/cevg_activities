# SEO Optimization — Hubs activités Crazy-EVG

Plan d'optimisation SEO complet pour les 42 pages `/activity-category/<slug>` du site `crazy-evg.com`.

## Arborescence

```
seo-optimization/
├── README.md                          (ce fichier)
├── aggregate.py                       Croise fichiers 1 et 2 → CSV enrichi
├── generate_titles_metas.py           Produit le CSV des 42 Title/Meta
├── briefs/
│   └── GABARIT-EDITORIAL.md           Gabarit réutilisable (9 blocs, patterns, checklist)
├── pilots/
│   ├── 01-shooting-evg.md             Page pilote 1 — Stand de tir (P1 quick win)
│   ├── 02-kidnapping-evg.md           Page pilote 2 — Kidnapping (P1 quick win)
│   ├── 03-corrida-evg.md              Page pilote 3 — Corrida (P1 quick win)
│   ├── 04-sexy-reveil-evg.md          Page pilote 4 — Réveil coquin (P1 quick win)
│   ├── 05-striptease-domicile-evg.md  Page pilote 5 — Strip-tease à domicile (P1, 25 dest.)
│   ├── 06-car-smash-evg.md            Page pilote 6 — Car Smash (P1 quick win)
│   └── 07-conduite-char-d-assaut-evg.md  Page pilote 7 — EVG tank (P1 quick win)
├── schema/
│   ├── schema-template.json           Template JSON-LD (Service + FAQPage + BreadcrumbList)
│   └── schema-shooting-EXAMPLE.json   Exemple rempli pour la page Shooting
└── exports/
    ├── hubs_enriched.csv              42 hubs × données agrégées du fichier 2
    └── titles_metas.csv               42 nouveaux Title + Meta + priorité
```

## Reproduire les exports

```bash
python3 seo-optimization/aggregate.py
python3 seo-optimization/generate_titles_metas.py
```

## Roadmap proposée

| Phase | Durée | Livrable |
|---|---|---|
| 1. Métas | 1 sem. | Déployer les 42 Title/Meta du CSV `titles_metas.csv` |
| 2. Quick wins | 3-4 sem. | Rédiger les 10 pages P1 selon gabarit (7 pilotes prêts : Shooting, Kidnapping, Corrida, Réveil coquin, Strip-tease domicile, Car Smash, Char d'Assaut) |
| 3. Sleeping giants | 2-3 sem. | Rédiger les 8 pages P2 |
| 4. Cold pages | 2 sem. | Rédiger / fusionner / désindexer les pages P3 |
| 5. Schema | 1 sem. | Déployer JSON-LD sur les 42 pages via le template |
| 6. Audit | 6-8 sem. | Mesurer GSC : CTR, position, clics |

## Cas particuliers identifiés

- **Limousine + Hummer Lap Tour** → fusion + redirection 301
- **Footbulle vs Football** → vérifier la cannibalisation
- **9 pages "Optimisée"** dans le statut mais body vide à l'extraction → re-crawler pour vérifier
