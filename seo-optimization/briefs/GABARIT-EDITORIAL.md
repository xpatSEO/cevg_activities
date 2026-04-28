# Gabarit éditorial — Hubs activité Crazy-EVG

**Cible** : pages `/activity-category/<slug>` (42 pages)
**Volume cible** : 800-1100 mots
**Lecteur cible** : témoin / organisateur d'EVG, 25-40 ans, recherche Google
**Ton** : direct, complice, second degré assumé (cohérent avec le ton de marque)
**Structure** : à insérer entre l'intro existante et la grille "Destinations pour cette activité"

---

## 0 · Variables à remplir avant rédaction

| Variable | Source | Exemple |
|---|---|---|
| `{ACTIVITE}` | Fichier 1 → `Nom activité` | Shooting |
| `{ACTIVITE_LOW}` | minuscules | shooting |
| `{MC_PRINCIPAL}` | Fichier 1 → `Mots-clés` | stand de tir evg |
| `{MC_VARIANTES}` | brainstorm | tir balles réelles evg, AK47 evg, stand tir entre potes |
| `{N_DESTINATIONS}` | Fichier 1 (grille) | 9 |
| `{LISTE_DESTINATIONS}` | Fichier 1 (grille) | Varsovie, Bucarest, Berlin, Prague... |
| `{SPECS_RECURRENTES}` | Fichier 2 (`hubs_enriched.csv` → `top_specs`) | Liste matériel/durée |
| `{DESC_DEST_1..3}` | Fichier 2 (`sample_desc_*`) | Présentation par destination |

---

## 1 · Title (60 caractères max)

**Pattern principal** :
```
{Activité} EVG : {bénéfice/promesse} | Crazy-EVG
```

**Patterns alternatifs** (si le principal dépasse 60 car.) :
- `{Activité} pour EVG | {N_DEST} destinations | Crazy-EVG`
- `EVG {Activité} : {bénéfice} - Crazy-EVG`

**Règles** :
- Mot-clé principal en premier tiers
- Toujours "EVG" présent (intent)
- Brand "Crazy-EVG" en fin
- Pas de "À Paris", "À Berlin" dans le title (la marque couvre toutes les destinations)

---

## 2 · Meta description (150-160 caractères)

**Pattern** :
```
{Verbe d'action} {activité} pour son EVG : {élément concret/preuve}.
{N_DESTINATIONS} destinations, devis 1 min. {Bénéfice émotionnel}.
```

**Règles** :
- Mot-clé exact dans les 100 premiers caractères
- Au moins un chiffre (preuve sociale ou concrète)
- CTA implicite ("devis 1 min", "réservez")
- Évite "découvrez" / "Bienvenue" / formulations creuses

---

## 3 · H1

**Pattern** :
```
{Activité} EVG
```
ou
```
{Activité} pour un enterrement de vie de garçon
```

→ Conserver "EVG" obligatoirement (vs H1 actuels qui omettent souvent).

---

## 4 · Structure du corps de page

### Bloc A — Introduction (existant, à enrichir)

> **Conserver** les 2 paragraphes actuels s'ils sont bons, sinon les réécrire.
> **Cible** : 120-180 mots.
> **Doit contenir** : mot-clé principal + 1-2 variantes + accroche émotionnelle.

---

### Bloc B — H2 : Pourquoi choisir {activité} pour son EVG ?

**Format** : 3-4 arguments en bullet list ou H3 courts.
**Longueur** : 150-200 mots.
**Objectif SEO** : capture intent informationnel, sémantique latente.

Ex. d'arguments :
- Une expérience qui marque les esprits
- Adapté à tous les niveaux (ou : réservé aux plus aguerris)
- Idéal en groupe de X à Y personnes
- Encadré par des pros (sécurité)

---

### Bloc C — H2 : L'expérience {activité} en détail

**Format** : 2-3 paragraphes descriptifs.
**Longueur** : 200-280 mots.
**Source** : agréger les `presentation` du fichier 2 (`sample_desc_*` du CSV enrichi).
**Objectif SEO** : densité sémantique + longue traîne ("comment se déroule un...", "à quoi s'attendre").

---

### Bloc D — H2 : Ce qui est inclus

**Format** : bullet list (UL).
**Source** : top 6-10 specs récurrentes du fichier 2 (`top_specs`).
**Longueur** : 8-12 items.
**Objectif SEO** : mots-clés "inclus", "matériel", "équipement", "durée".

Items types :
- Durée : entre Xh et Yh
- Encadrement par instructeur
- Équipement complet fourni
- Min X / max Y participants
- Briefing sécurité

---

### Bloc E — H2 : Combien ça coûte ? Tarif et durée

**Format** : tableau (3 colonnes : critère / valeur / précision) ou paragraphe + UL.
**Longueur** : 100-150 mots.
**Objectif SEO** : intent transactionnel, snippet "people also ask" ("prix", "tarif", "combien").

Critères types :
- Tarif moyen / personne
- Tarif moyen / groupe
- Durée moyenne
- Nombre de joueurs (min / max)
- Inclus / non inclus

---

### Bloc F — H2 : Où faire {activité} pour un EVG ?

**Format** : grille existante (H3 par destination — déjà en place).
**Action** : aucune modification de gabarit, mais **ajouter une phrase d'intro** sous le H2 mentionnant les destinations principales pour le maillage.

> Exemple : "Le {activité} est disponible dans {N_DEST} de nos destinations EVG : {LISTE_DESTINATIONS}. Chaque ville propose une déclinaison avec ses propres spécificités."

---

### Bloc G — H3 (sous Bloc F) : Comparatif rapide des destinations

**Format** : tableau ou liste de 3-5 destinations phares avec phrase courte.
**Source** : `sample_desc_*` du CSV enrichi.
**Longueur** : 80-150 mots.
**Objectif SEO** : maillage interne, différenciation, contenu unique.

Exemple :
- **EVG Berlin** : phrase courte tirée de `presentation` + lien vers la page activité×Berlin
- **EVG Prague** : idem
- ...

---

### Bloc H — H2 : Ces activités EVG vont aussi vous plaire

**Format** : 4-6 cartes ou liens contextuels.
**Choix** : activités thématiquement proches (à valider manuellement).

| Hub source | Suggestions de maillage |
|---|---|
| Shooting | Char d'assaut, Airsoft, Parcours du Combattant, Paintball |
| Kidnapping | Parcours du Combattant, Combat Chien, Crazy Night, Sexy Combat |
| Croisière | Jet Ski, Flyboard, Hydrospeed |
| Striptease Domicile | Sexy Réveil, Diner Strip, Stripclub, Party Bus Strip |
| Karting | Quad Buggy, Conduite Ferrari, Conduite Char d'Assaut |
| (à compléter) | |

**Ancres** : varier (`stand de tir EVG`, `tir entre potes`, `initiation au tir EVG`).

---

### Bloc I — H2 : FAQ — {Activité} EVG

**Format** : 5-7 questions, chaque question en H3 + réponse courte (40-80 mots).
**Objectif SEO** : Schema FAQPage, "People Also Ask".

**Questions standards à adapter** :
1. Combien coûte un {activité} pour un EVG ?
2. Quelle est la durée d'une session de {activité} ?
3. Est-ce dangereux / faut-il un niveau particulier ?
4. À partir de combien de personnes ?
5. Que faut-il prévoir / apporter ?
6. Dans quelles villes peut-on faire un {activité} EVG ?
7. Comment réserver un {activité} pour son EVG ?

---

## 5 · Données structurées (JSON-LD)

À injecter dans le `<head>` ou en bas de page : voir `seo-optimization/schema/schema-template.json`.

Trois blocs à inclure :
1. `Service` (nom, description, areaServed, offers.priceRange)
2. `FAQPage` (réponses du Bloc I)
3. `BreadcrumbList`

---

## 6 · Liens internes obligatoires

| Type | Destination | Ancre suggérée |
|---|---|---|
| Vers page mère | `/enterrement-de-vie-de-garcon` | `enterrement de vie de garçon` |
| Vers 4-6 hubs frères | `/activity-category/<slug>` | varier (voir Bloc H) |
| Vers chaque page activité×destination | `/enterrement-de-vie-de-garcon-<dest>/<slug>` | `{activité} à {destination}` |
| Vers vidéo | conserver le lien existant | `voir le {activité} en vidéo` |

---

## 7 · Checklist de validation (avant publication)

- [ ] Title ≤ 60 caractères + contient mot-clé principal + "Crazy-EVG"
- [ ] Meta description 150-160 car. + mot-clé + chiffre + CTA
- [ ] H1 unique avec mot-clé principal
- [ ] Au moins 5 H2 dans la zone éditoriale (hors footer)
- [ ] 800-1100 mots de contenu utile (hors footer/menu)
- [ ] Mot-clé principal présent : H1, premier paragraphe, au moins 1 H2
- [ ] 4-6 liens internes contextuels (hors footer)
- [ ] FAQ avec 5+ questions
- [ ] JSON-LD `Service` + `FAQPage` + `BreadcrumbList` injecté
- [ ] Image principale avec `alt` contenant le mot-clé
- [ ] CTA "Devis 1 minute" conservé
- [ ] Pas de duplication de contenu avec un autre hub
