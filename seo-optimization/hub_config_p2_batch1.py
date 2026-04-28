"""
Configurations par hub pour la génération HTML P2.
Une entrée par hub avec :
- intro_p1: 1er paragraphe d'intro (hook accrocheur, ~80 mots)
- intro_p2: 2e paragraphe d'intro (context, MC + variantes, ~80 mots)
- why_args: 4 arguments pour le bloc "Pourquoi choisir"
- exp_intro: 1 phrase de transition avant le bloc "L'expérience en détail"
- price_note: note de bas de tableau prix (optionnel)
- faq_overrides: dict question->reponse (optionnel, sinon FAQ générique)
"""

HUB_CONFIG_BATCH_1 = {
    # =====================================================================
    "Parcours du Combattant": {
        "intro_p1": "Le <strong>parcours du combattant EVG</strong> (aussi connu sous le nom de <em>stage commando EVG</em>) est l'épreuve ultime pour transformer le futur marié en machine de guerre… ou en serpillière. Encadré par d'anciens militaires, votre groupe enchaîne franchissements, rampers sous filets, courses d'obstacles, montées de cordes et autres gentillesses pensées pour vous mettre à genoux dans la boue.",
        "intro_p2": "Idéal pour un <a href=\"https://www.crazy-evg.com/enterrement-de-vie-de-garcon\">EVG</a> qui veut sortir des sentiers battus, le stage commando combine défoulement physique, esprit d'équipe et fous rires. Le futur marié a évidemment droit aux <strong>punitions</strong> du groupe : pompes supplémentaires, tractions, port de charge. Une activité qui marque les corps autant que les mémoires.",
        "why_args": [
            "<strong>Encadrement par d'anciens militaires :</strong> sécurité, discipline et challenge calibrés.",
            "<strong>Le futur marié pris pour cible :</strong> punitions personnalisées, briefing personnel, surnom de bidasse.",
            "<strong>Esprit d'équipe garanti :</strong> rien ne soude un groupe comme la boue partagée.",
            "<strong>Adapté à tous niveaux :</strong> les épreuves sont modulables, l'objectif est de transpirer ensemble.",
        ],
        "exp_intro": "Programme type d'une demi-journée :",
        "price_note": "<strong>À noter :</strong> prévoyez des vêtements que vous pouvez salir et de quoi vous changer — la boue est garantie.",
    },

    # =====================================================================
    "Crazy Night": {
        "intro_p1": "La <strong>Crazy Night EVG</strong>, c'est la soirée folle clés en main : on prend les meilleurs ingrédients de l'enterrement de vie de garçon (<a href=\"https://www.crazy-evg.com/activity-category/striptease-domicile-evg\">strip-tease</a>, boîte VIP, bouteilles, transport privatif, parfois show coquin), on les emballe dans un programme calibré pour la soirée, et on vous laisse vous occuper d'une seule chose : kiffer.",
        "intro_p2": "Disponible dans 9 destinations Crazy-EVG, la Crazy Night est le format préféré des groupes qui veulent <strong>une nuit légendaire sans se prendre la tête</strong> avec la logistique. Tout est inclus, votre guide locale gère le timing, et vous concentrez votre énergie là où elle compte : le futur marié.",
        "why_args": [
            "<strong>Soirée 100 % clés en main :</strong> aucune logistique à gérer, votre guide locale s'occupe de tout.",
            "<strong>Le combo parfait :</strong> dîner ou apéro, strip-tease, boîte VIP, bouteilles offertes.",
            "<strong>Tarif optimisé :</strong> le forfait groupe est ~30 % moins cher que les activités achetées séparément.",
            "<strong>Disponible dans les capitales de la fête :</strong> Prague, Budapest, Cracovie, Barcelone, Amsterdam, etc.",
        ],
        "exp_intro": "Soirée type Crazy Night :",
    },

    # =====================================================================
    "Airsoft Battle": {
        "intro_p1": "L'<strong>airsoft battle EVG</strong> est la version la plus tactique des activités combat : répliques d'armes ultra-réalistes, terrain dédié (forêt, arènes urbaines, hangars), <strong>billes biodégradables</strong>, équipement complet — gilet, masque, protections — et scénarios variés (capture du drapeau, élimination, défense de zone).",
        "intro_p2": "Plus engagé que le paintball, l'airsoft offre une expérience proche de la simulation militaire. Le futur marié ? Cible désignée du groupe, naturellement. Activité disponible dans 10 destinations européennes, idéale pour un <a href=\"https://www.crazy-evg.com/enterrement-de-vie-de-garcon\">EVG</a> à thème commando.",
        "why_args": [
            "<strong>Plus tactique que le paintball :</strong> répliques réalistes, vraies stratégies d'équipe.",
            "<strong>Sans douleur excessive :</strong> billes biodégradables, équipement de protection complet.",
            "<strong>Scénarios multiples :</strong> capture du drapeau, élimination, défense, escorte du marié.",
            "<strong>Parfait combo commando :</strong> à enchaîner avec stand de tir, parcours du combattant ou tank.",
        ],
        "exp_intro": "Déroulé type d'une session airsoft :",
    },

    # =====================================================================
    "Journee Ski": {
        "intro_p1": "L'<strong>EVG au ski</strong>, c'est l'option hivernale (et pour certains, la meilleure de toutes) : journée sur les pistes, après-ski musclé, location matériel et forfaits inclus. Le format idéal pour un enterrement de vie de garçon entre amateurs de glisse — ou pour ceux qui veulent enfin apprendre à skier en se ridiculisant ensemble.",
        "intro_p2": "Disponible dans nos destinations montagne (Annecy, Andorre), l'<a href=\"https://www.crazy-evg.com/enterrement-de-vie-de-garcon\">EVG ski</a> combine la <strong>journée sport</strong> et la <strong>soirée festive</strong> en chalet ou bar d'altitude. Toutes les options possibles : ski alpin, snowboard, cours pour débutants, raquettes, motoneige selon les domaines.",
        "why_args": [
            "<strong>Une expérience montagne complète :</strong> ski/snow le jour, après-ski et chalet le soir.",
            "<strong>Tout inclus :</strong> forfait remontées, location matériel, hébergement chalet ou résidence.",
            "<strong>Adapté à tous niveaux :</strong> du débutant au skieur confirmé, plusieurs domaines reliés.",
            "<strong>L'occasion d'enchaîner :</strong> ski le matin, sauna l'après-midi, raclette le soir, soirée bar.",
        ],
        "exp_intro": "Programme type d'un week-end ski EVG :",
    },

    # =====================================================================
    "Degustation Bieres": {
        "intro_p1": "La <strong>dégustation de bières EVG</strong> est l'animation parfaite pour démarrer un enterrement de vie de garçon en douceur — ou en force, selon le rythme imposé. Atelier guidé par un <em>maître brasseur</em>, visite de brasserie locale, dégustation de 5 à 10 bières artisanales avec planches de charcuterie/fromage : le combo culture-débauche-conviabilité.",
        "intro_p2": "Disponible dans 11 destinations EVG dont les capitales brassicoles européennes (Bruxelles, Berlin, Prague, Amsterdam), la dégustation de bières s'adresse aussi bien aux <strong>connaisseurs</strong> qu'aux groupes qui veulent juste <strong>boire en bonne compagnie</strong>. Comptez 1h30 à 2h d'activité.",
        "why_args": [
            "<strong>Animation pédagogique :</strong> initiation à la dégustation, accords mets-bières, vocabulaire pro.",
            "<strong>Lieux d'exception :</strong> brasseries artisanales, caves voûtées, micro-brasseries de centre-ville.",
            "<strong>Parfaite ouverture d'EVG :</strong> on commence léger, on prépare le terrain pour la soirée.",
            "<strong>Capitales brassicoles couvertes :</strong> Bruxelles, Berlin, Prague, Amsterdam, etc.",
        ],
        "exp_intro": "Programme type d'une dégustation :",
    },
}
