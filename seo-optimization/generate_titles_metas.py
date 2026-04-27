#!/usr/bin/env python3
"""
Génère un CSV avec les 42 nouveaux Title et Meta description selon le gabarit.

Sortie: seo-optimization/exports/titles_metas.csv
Colonnes: URL, hub, mc_principal, current_title, current_meta, new_title, new_title_len,
         new_meta, new_meta_len, h1_suggested, statut, priorite
"""
import csv
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

F1 = [f for f in glob.glob("*.csv") if "GenAI" in f][0]
OUT = os.path.join(ROOT, "seo-optimization", "exports", "titles_metas.csv")


# ---------------------------------------------------------------------------
# Definition manuelle: par hub -> (new_title, new_meta, h1)
# Title cible 55-60 car. — Meta cible 150-160 car.
# Mots-clés issus du fichier 1
# ---------------------------------------------------------------------------
TITLES_METAS = {
    "Initiation Tir Shooting": {
        "title": "Stand de tir EVG : AK47, Glock, Sniper | Crazy-EVG",
        "meta": "Offrez un stand de tir EVG à votre pote : AK47, Glock, Magnum 357 à balles réelles. 9 destinations, devis 1 min. Sensations garanties pour son enterrement.",
        "h1": "Stand de tir EVG",
    },
    "Kidnapping": {
        "title": "Kidnapping EVG : fausse arrestation choc | Crazy-EVG",
        "meta": "Idée kidnapping EVG : faites vivre une fausse arrestation au futur marié pour son enterrement de vie de garçon. Stress et fou rire garantis. Devis en 1 min.",
        "h1": "Kidnapping EVG : fausse arrestation",
    },
    "Parcours du Combattant": {
        "title": "Stage commando EVG : parcours du combattant | Crazy-EVG",
        "meta": "Stage commando pour son EVG : parcours du combattant encadré par d'anciens militaires. Vos potes vont en baver. Devis en 1 min, 6 destinations.",
        "h1": "Parcours du combattant EVG",
    },
    "Corrida": {
        "title": "Corrida EVG : combat de taureau | Crazy-EVG",
        "meta": "Corrida EVG : devenez matador le temps d'une après-midi avec un vrai taureau. Une activité unique pour un enterrement de vie de garçon mémorable.",
        "h1": "Corrida EVG",
    },
    "Conduite Ferrari": {
        "title": "Conduite Ferrari EVG : pilotage sur circuit | Crazy-EVG",
        "meta": "Offrez une conduite Ferrari pour son EVG : pilotage sur circuit, encadré par un instructeur. Le kiff ultime pour son enterrement de vie de garçon.",
        "h1": "Conduite Ferrari EVG",
    },
    "Striptease Domicile": {
        "title": "Strip-tease à domicile EVG : show privé | Crazy-EVG",
        "meta": "Strip-tease à domicile pour son EVG : showgirl pro à votre appart ou hôtel, dans 25 destinations. Discret, simple, efficace. Devis en 1 minute.",
        "h1": "Strip-tease à domicile EVG",
    },
    "Car Smash": {
        "title": "Car Smash EVG : défoulez-vous sur une voiture | Crazy-EVG",
        "meta": "Car Smash pour son EVG : pulvérisez une vraie voiture à coups de batte et de masse. Le défouloir parfait pour un enterrement de vie de garçon.",
        "h1": "Car Smash EVG",
    },
    "Conduite Char D Assaut": {
        "title": "Conduite char d'assaut EVG : pilotez un tank | Crazy-EVG",
        "meta": "EVG tank : conduisez un vrai char d'assaut pour son enterrement de vie de garçon. 6 destinations dont Prague et Budapest. Devis en 1 minute.",
        "h1": "Conduite char d'assaut EVG",
    },
    "Sexy Reveil": {
        "title": "Réveil coquin EVG : sexy alarm pour le marié | Crazy-EVG",
        "meta": "Réveil coquin pour son EVG : une stripteaseuse réveille le futur marié au saut du lit. Surprise et fou rire garantis. 8 destinations, devis 1 min.",
        "h1": "Réveil coquin EVG",
    },
    "Crazy Night": {
        "title": "Crazy Night EVG : soirée folle clés en main | Crazy-EVG",
        "meta": "Crazy Night EVG : la soirée la plus folle de son enterrement de vie de garçon. Strip, boîte, bouteilles : tout est inclus. 9 destinations, devis 1 min.",
        "h1": "Crazy Night EVG",
    },
    "Airsoft Battle": {
        "title": "Airsoft battle EVG : combat tactique entre potes | Crazy-EVG",
        "meta": "Airsoft battle pour son EVG : combat tactique avec répliques d'armes en équipement complet. 10 destinations, devis 1 min. Adrénaline garantie.",
        "h1": "Airsoft battle EVG",
    },
    "Journee Ski": {
        "title": "EVG au ski : journée pistes & remontées | Crazy-EVG",
        "meta": "EVG au ski : journée sur les pistes, location matériel et forfaits inclus. Idéal en hiver entre potes. Devis 1 minute, séjour clés en main.",
        "h1": "EVG au ski",
    },
    "Degustation Bieres": {
        "title": "Dégustation de bières EVG : atelier brassicole | Crazy-EVG",
        "meta": "Dégustation de bières pour son EVG : atelier guidé, brasseries locales, 11 destinations dont Prague, Berlin, Bruxelles. Devis en 1 minute.",
        "h1": "Dégustation de bières EVG",
    },
    "Croisiere Bateau": {
        "title": "Croisière bateau EVG : privatisation sur l'eau | Crazy-EVG",
        "meta": "Croisière bateau pour son EVG : bateau privatisé entre potes, open bar et musique. 20 destinations en mer ou sur fleuve. Devis en 1 minute.",
        "h1": "Croisière en bateau EVG",
    },
    "Boite Bouteilles": {
        "title": "Boîte et bouteilles EVG : entrée VIP en club | Crazy-EVG",
        "meta": "Boîte et bouteille pour son EVG : entrée VIP, table privatisée, bouteilles offertes. 25 destinations testées. Devis 1 min, soirée garantie.",
        "h1": "Boîte et bouteilles EVG",
    },
    "Football": {
        "title": "Football EVG : match 5 contre 5 entre potes | Crazy-EVG",
        "meta": "Activité football EVG : match 5 vs 5 sur terrain privatisé, équipement fourni. 12 destinations. Idéal pour un enterrement de vie de garçon sportif.",
        "h1": "Football EVG",
    },
    "Diner Strip": {
        "title": "Dîner strip EVG : repas avec stripteaseuse | Crazy-EVG",
        "meta": "Dîner strip-tease EVG : repas dans un resto privatisé avec show de stripteaseuses. 13 destinations. La soirée parfaite pour son enterrement.",
        "h1": "Dîner strip-tease EVG",
    },
    "Poker Sexy": {
        "title": "Strip poker EVG : partie coquine entre potes | Crazy-EVG",
        "meta": "Poker sexy pour son EVG : partie de strip poker animée par une croupière professionnelle. Une soirée coquine et fun à tenter pour son enterrement.",
        "h1": "Poker sexy EVG",
    },
    "Combat Chien": {
        "title": "Combat Man vs Dog EVG : duel avec chien dressé | Crazy-EVG",
        "meta": "Combat chien EVG : affrontez un berger malinois équipé d'une protection. Une activité unique et adrénaline pour un enterrement de vie de garçon.",
        "h1": "Combat Man vs Dog EVG",
    },
    "Tournee Bars": {
        "title": "Tournée des bars EVG : pub crawl entre potes | Crazy-EVG",
        "meta": "Tournée des bars EVG : pub crawl encadré dans 18 destinations. Bars sélectionnés, shots offerts, ambiance garantie. Devis en 1 minute.",
        "h1": "Tournée des bars EVG",
    },
    "Party Bus Strip": {
        "title": "Bus strip EVG : party bus avec stripteaseuse | Crazy-EVG",
        "meta": "Party bus strip pour son EVG : bus privatisé, stripteaseuse à bord, musique et bouteilles. La fête commence dans le bus. 6 destinations.",
        "h1": "Bus strip EVG",
    },
    "Quad Buggy": {
        "title": "Randonnée quad & buggy EVG : raid tout-terrain | Crazy-EVG",
        "meta": "Randonnée quad ou buggy pour son EVG : raid tout-terrain encadré, pilotage en groupe. 14 destinations. Sensations fortes pour son enterrement.",
        "h1": "Randonnée quad & buggy EVG",
    },
    "Flyboard": {
        "title": "Flyboard EVG : envolez-vous au-dessus de l'eau | Crazy-EVG",
        "meta": "Flyboard pour son EVG : sensation de vol à 10m au-dessus de l'eau, encadrement pro. Une activité unique pour un enterrement de vie de garçon.",
        "h1": "Flyboard EVG",
    },
    "Karting": {
        "title": "Karting EVG : course sur circuit entre potes | Crazy-EVG",
        "meta": "Karting EVG : Grand Prix entre potes sur circuit privatisé, 20 destinations. Karts puissants, classement final. Devis en 1 minute.",
        "h1": "Karting EVG",
    },
    "Jet Ski": {
        "title": "Jet Ski EVG : pilotage en mer entre potes | Crazy-EVG",
        "meta": "Jet ski pour son EVG : session pilotage en mer, jets puissants, 7 destinations dont Barcelone et Marbella. Sensations garanties. Devis 1 min.",
        "h1": "Jet ski EVG",
    },
    "Footbulle": {
        "title": "Bubble foot EVG : foot dans une bulle gonflable | Crazy-EVG",
        "meta": "Bubble foot pour son EVG : match de foot dans des bulles gonflables géantes. Fou rire garanti, 17 destinations. Devis en 1 minute.",
        "h1": "Bubble foot EVG",
    },
    "Beer Bike": {
        "title": "Beer Bike EVG : vélo collectif & bière à bord | Crazy-EVG",
        "meta": "Beer bike EVG : vélo collectif de 12 places avec tireuse à bière à bord. Tour guidé en ville, ambiance assurée. 7 destinations, devis 1 min.",
        "h1": "Beer bike EVG",
    },
    "Hummer Lap Tour": {
        "title": "Limousine Hummer EVG : tour de ville VIP | Crazy-EVG",
        "meta": "Limousine Hummer pour son EVG : Hummer privatisé, bar à bord, tour de ville. La sortie la plus VIP de son enterrement de vie de garçon.",
        "h1": "Limousine Hummer EVG",
    },
    "Limousine": {
        "title": "Limousine EVG : transfert VIP entre potes | Crazy-EVG",
        "meta": "Limousine pour son EVG : transfert ou tour de ville VIP, bar à bord, capacité jusqu'à 12 personnes. 13 destinations. Devis en 1 minute.",
        "h1": "Limousine EVG",
    },
    "Stripclub": {
        "title": "Club strip-tease EVG : entrée VIP & bouteilles | Crazy-EVG",
        "meta": "Club striptease EVG : entrée VIP coupe-file, bouteilles offertes, table privatisée. Sélection des meilleurs strip clubs dans 20 destinations.",
        "h1": "Club strip-tease EVG",
    },
    "Parapente": {
        "title": "Parapente EVG : baptême de vol biplace | Crazy-EVG",
        "meta": "Parapente EVG : baptême de vol biplace encadré par un moniteur. Vue imprenable, montée d'adrénaline. Une activité d'exception pour un enterrement.",
        "h1": "Parapente EVG : baptême de vol",
    },
    "Saut Elastique": {
        "title": "Saut à l'élastique EVG : grand saut entre potes | Crazy-EVG",
        "meta": "EVG saut à l'élastique : grand saut depuis un pont ou une grue, encadrement pro. 4 destinations. Adrénaline maximum pour son enterrement.",
        "h1": "Saut à l'élastique EVG",
    },
    "Sexy Combat": {
        "title": "Combat sexy EVG : lutte avec stripteaseuses | Crazy-EVG",
        "meta": "Combat sexy EVG : combat fun face à des stripteaseuses dans un ring privatisé. Une animation unique pour un enterrement de vie de garçon.",
        "h1": "Combat sexy EVG",
    },
    "Chute Libre": {
        "title": "Chute libre EVG : simulateur en soufflerie | Crazy-EVG",
        "meta": "Chute libre EVG : simulateur indoor en soufflerie, sensation de saut en parachute en toute sécurité. 7 destinations. Idéal pour son enterrement.",
        "h1": "Chute libre indoor EVG",
    },
    "Paintball": {
        "title": "Paintball EVG : combat tactique entre potes | Crazy-EVG",
        "meta": "Paintball EVG : combat sur terrain privatisé, équipement complet, billes incluses. 22 destinations. Le grand classique de l'enterrement de garçon.",
        "h1": "Paintball EVG",
    },
    "Laser Game": {
        "title": "Laser game EVG : combat laser indoor | Crazy-EVG",
        "meta": "Laser game EVG : combat indoor en équipes, 13 destinations. Sans douleur, accessible à tous. Idéal pour démarrer un enterrement de vie de garçon.",
        "h1": "Laser game EVG",
    },
    "Faux Saut Elastique": {
        "title": "Faux saut à l'élastique EVG : le canular | Crazy-EVG",
        "meta": "Faux saut à l'élastique EVG : faites croire au futur marié qu'il va sauter dans le vide. Le canular ultime pour son enterrement de vie de garçon.",
        "h1": "Faux saut à l'élastique EVG",
    },
    "Canyoning": {
        "title": "Canyoning EVG : descente de canyon en groupe | Crazy-EVG",
        "meta": "EVG canyoning : descente de canyon, sauts, rappels et toboggans naturels. Encadré par des moniteurs diplômés. 5 destinations, devis 1 min.",
        "h1": "Canyoning EVG",
    },
    "Saut en Parachute": {
        "title": "Saut en parachute EVG : tandem à 4000m | Crazy-EVG",
        "meta": "Saut en parachute EVG : saut tandem à 4000m, chute libre 50 sec. L'expérience la plus extrême pour un enterrement de vie de garçon. Devis 1 min.",
        "h1": "Saut en parachute EVG",
    },
    "Escape Room": {
        "title": "Escape game EVG : énigmes en équipe entre potes | Crazy-EVG",
        "meta": "Escape game EVG : 60 min pour résoudre les énigmes en équipe. 22 destinations, scénarios variés. Activité idéale en début d'enterrement.",
        "h1": "Escape game EVG",
    },
    "Hydrospeed": {
        "title": "Hydrospeed EVG : descente de rivière en flotteur | Crazy-EVG",
        "meta": "Hydrospeed EVG : descente de rapides en flotteur individuel, encadré par un guide. Sensations aquatiques fortes pour un enterrement original.",
        "h1": "Hydrospeed EVG",
    },
    "Rafting Eaux Vives": {
        "title": "Rafting EVG : descente en eaux vives entre potes | Crazy-EVG",
        "meta": "Rafting EVG : descente en eaux vives en équipe, encadrée par un moniteur diplômé. 5 destinations. Idéal pour un EVG nature et adrénaline.",
        "h1": "Rafting EVG",
    },
}


def main():
    with open(F1, "r", encoding="utf-8") as fp:
        rows = list(csv.DictReader(fp))

    # Determine priority by current position + clicks
    def priority(r):
        try:
            pos = float(r["Position"].replace(",", "."))
        except (ValueError, AttributeError):
            pos = 99
        try:
            clicks = int(r["Clicks"])
        except (ValueError, AttributeError):
            clicks = 0
        if 4 <= pos <= 10 and clicks >= 30:
            return "P1 - Quick win"
        if 10 < pos <= 25 and clicks >= 5:
            return "P2 - Sleeping giant"
        if pos > 25 or clicks == 0:
            return "P3 - Cold page"
        return "P2 - Sleeping giant"

    output_rows = []
    missing = []
    for r in rows:
        hub = r["Nom activité"]
        tm = TITLES_METAS.get(hub)
        if not tm:
            missing.append(hub)
            continue
        output_rows.append({
            "URL": r["URL"],
            "hub": hub,
            "mc_principal": r["Mots-clés "].strip(),
            "current_title": r["Titre SEO"],
            "current_meta": r["Meta Description"],
            "new_title": tm["title"],
            "new_title_len": len(tm["title"]),
            "new_meta": tm["meta"],
            "new_meta_len": len(tm["meta"]),
            "h1_suggested": tm["h1"],
            "statut": r["Statut"],
            "priorite": priority(r),
        })

    with open(OUT, "w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Wrote {OUT}")
    print(f"Pages traitées: {len(output_rows)}/{len(rows)}")
    if missing:
        print(f"⚠ Hubs sans entrée: {missing}")
    too_long = [(r["hub"], r["new_title_len"]) for r in output_rows if r["new_title_len"] > 60]
    if too_long:
        print(f"⚠ Titles > 60 car.: {too_long}")
    meta_long = [(r["hub"], r["new_meta_len"]) for r in output_rows if r["new_meta_len"] > 160]
    if meta_long:
        print(f"⚠ Metas > 160 car.: {meta_long}")
    meta_short = [(r["hub"], r["new_meta_len"]) for r in output_rows if r["new_meta_len"] < 140]
    if meta_short:
        print(f"⚠ Metas < 140 car.: {meta_short}")


if __name__ == "__main__":
    main()
