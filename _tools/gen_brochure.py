#!/usr/bin/env python3
"""Génère brochure/index.html (FR) et en/brochure/index.html (EN).

Une seule source pour les deux langues : la mise en page reste identique,
seuls les textes changent. Relancer après toute modification :
    python3 _tools/gen_brochure.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Lien de contact direct affiché sur chaque page (WhatsApp, Calendly…).
# Vide = les boutons de contact sont masqués.
CONTACT_URL = "https://wa.me/33668680407"
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3.2.8.9-3.1-.2-.3c-.8-1.3-1.3-2.8-1.3-4.4C3.6 7.4 7.4 3.6 12 3.6s8.4 3.8 8.4 8.4-3.8 8.2-8.4 8.2z"/><path d="M17.5 14.4c-.3-.2-1.7-.9-2-1-.3-.1-.4-.2-.6.1-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5 0-.2 0-.4-.1-.5l-.9-2.1c-.2-.5-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.3.3-1 .9-1 2.3s1 2.7 1.2 2.9c.1.2 2 3.1 5 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3z"/></svg>'

LOTS = [
    # n, type FR, type EN, m², étage, expo FR, expo EN, chambres FR, chambres EN, extra FR, extra EN, prix
    (5, "3 pièces", "2-bedroom", "76", 1, "Sud-ouest", "South-west", "2 chambres + 2 coins montagne", "2 bedrooms + 2 mountain nooks", "", "", "525 000", "525,000"),
    (6, "4 pièces", "3-bedroom", "70", 2, "Nord-ouest-est", "North-west-east", "3 chambres + 1 coin montagne", "3 bedrooms + 1 mountain nook", "Terrasse", "Terrace", "620 000", "620,000"),
    (7, "3 pièces", "2-bedroom", "62", 2, "Sud-est", "South-east", "2 chambres + 1 coin montagne", "2 bedrooms + 1 mountain nook", "", "", "600 000", "600,000"),
    (8, "4 pièces", "3-bedroom", "75", 2, "Sud-ouest", "South-west", "3 chambres + 1 coin montagne", "3 bedrooms + 1 mountain nook", "Terrasse sud de 12 m²", "12 m² south terrace", "670 000", "670,000"),
    (9, "4 pièces", "3-bedroom", "69", 3, "Nord-ouest-est", "North-west-east", "3 chambres + 1 coin montagne", "3 bedrooms + 1 mountain nook", "Terrasse", "Terrace", "620 000", "620,000"),
    (10, "3 pièces bis", "2-bedroom plus", "59", 3, "Sud-est", "South-east", "2 suites + 1 coin montagne", "2 suites + 1 mountain nook", "Terrasse sud de 8 m²", "8 m² south terrace", "600 000", "600,000"),
    (11, "4 pièces", "3-bedroom", "75", 3, "Sud et ouest", "South and west", "3 chambres + 1 coin montagne", "3 bedrooms + 1 mountain nook", "Terrasse", "Terrace", "655 000", "655,000"),
    (12, "Le dernier étage", "The top floor", "140 (105 Carrez)", 4, "Sud-est", "South-east", "4 chambres dont 2 suites", "4 bedrooms incl. 2 suites", "Jacuzzi possible face aux pistes · terrasses ouest 15 m² et sud 19 m²", "Optional hot tub facing the slopes · 15 m² west and 19 m² south terraces", "1 150 000", "1,150,000"),
    (13, "Le grand familial", "The family residence", "134", 3, "Sud-ouest-est", "South-west-east", "5 chambres dont 4 suites", "5 bedrooms incl. 4 suites", "Sauna privatif · 2 terrasses", "Private sauna · 2 terraces", "1 255 000", "1,255,000"),
]

T = {
    "fr": {
        "lang": "fr", "root": "/", "title": "Les Airelles aux 2 Alpes — Dossier du projet",
        "desc": "Dossier du projet Les Airelles aux 2 Alpes : perspectives 3D, plans, prix et simulation de TVA.",
        "floor": lambda n: "1<sup>er</sup> étage" if n == 1 else f"{n}<sup>e</sup> étage",
        "ht": "HT", "lot": "Lot", "surface": "Surface", "floor_l": "Étage", "expo": "Exposition", "rooms": "Couchages",
        "persp": "Perspective 3D — image non contractuelle",
        "contact": "Une question ? Discutons sur WhatsApp",
        "prev": "Page précédente", "next": "Page suivante", "goto": "Aller à la page",
        "cover_kicker": "Dossier du projet · Édition 2026",
        "cover_pill": "Les 2 Alpes · Isère · 1 650 m", "cover_brand": "Immobilier d'exception",
        "cover_meta": "Brochure confidentielle · Document non contractuel",
        "m_eye": "Bienvenue aux Airelles", "m_h": "Votre appartement premium <em>à 200 m des pistes.</em>",
        "m_body": "Sur la place de Venosc, cœur historique des 2 Alpes, l'ancien hôtel Les Airelles devient une résidence de onze appartements neufs. Pierre naturelle, chêne, bois sculpté, et de grandes baies ouvertes sur les sommets.",
        "m_stats": [("200 m", "des pistes"), ("11", "appartements"), ("3 600 m", "le glacier")],
        "cover_sub": "Onze appartements neufs sur la place de Venosc, à deux cents mètres des pistes. Les 2 Alpes, 1 650 m.",
        "cover_foot": ("Vendu sur plan", "Place de Venosc · 38860 Les 2 Alpes"),
        "p2_eye": "Le lieu", "p2_h": "La place où rien <em>n'était à vendre.</em>",
        "p2_body": [
            "La place de Venosc est le cœur historique des 2 Alpes : les terrasses, les restaurants, les boutiques, et les remontées à deux cents mètres. Tout le monde rêve d'y habiter. Il n'y avait jamais rien à vendre.",
            "L'ancien hôtel Les Airelles est entièrement repensé en une résidence de seulement onze appartements neufs. Le bâtiment est surélevé, reçoit une toiture neuve et des façades en bois et en pierre.",
        ],
        "p2_before": "Aujourd'hui", "p2_after": "Demain",
        "p3_eye": "Le projet en chiffres", "p3_h": "L'essentiel, <em>en un coup d'œil.</em>",
        "p3_stats": [("11", "appartements seulement"), ("6", "encore disponibles"), ("200 m", "des remontées"), ("59 à 140 m²", "du 3 pièces au grand familial"), ("8", "couchages jusqu'à"), ("20 %", "de TVA récupérés")],
        "p3_list_h": "Pour chaque appartement",
        "p3_list": ["Un casier à ski et une cave", "Pierre naturelle, parquet en chêne, bois sculpté", "Cuisine équipée", "Presque tous avec terrasse", "Parking couvert juste en face", "Conciergerie pour la location"],
        "p4_eye": "L'architecture", "p4_h": "Le bois, la pierre, <em>la lumière du soir.</em>",
        "p4_body": "Une façade de chalet contemporain : bardage bois, soubassement en pierre, grands balcons. La nuit, sous la neige, la résidence s'allume au cœur de la station.",
        "p5_eye": "L'intérieur", "p5_h": "Sous la charpente, <em>les sommets.</em>",
        "p5_body": "Le séjour du dernier étage s'ouvre sous la charpente en bois, avec une grande baie sur les sommets. Partout, des matières nobles et chaleureuses.",
        "p5_mat": [("Pierre naturelle", "Murs et détails"), ("Chêne massif", "Parquet naturel"), ("Bois sculpté", "Décor de montagne"), ("Grandes baies", "Ouvertes sur les sommets")],
        "p6_eye": "Les chambres", "p6_h": "Des chambres pour <em>toute la famille.</em>",
        "p6_body": "Des suites avec leur salle d'eau, et des coins montagne avec lits superposés pour les enfants. Deux salles d'eau au minimum : personne n'attend le matin.",
        "p6_c1": "Une chambre, le sommet dans la fenêtre", "p6_c2": "Le coin montagne, pour les enfants",
        "p7_eye": "Le bien-être", "p7_h": "Un jacuzzi qui fume, <em>face aux pistes.</em>",
        "p7_body": "Au dernier étage, la terrasse peut accueillir un jacuzzi face au domaine skiable. Le grand appartement familial du troisième étage a son propre sauna.",
        "p8_eye": "Les appartements disponibles", "p8_h": "La grille des lots, <em>de 525 000 € à 1 255 000 € HT.</em>",
        "p8_th": ["Lot", "Type", "Surface", "Étage", "Exposition", "Prix HT"],
        "p8_status": "4 appartements vendus · 1 sous offre · 6 encore disponibles. Disponibilité de chaque lot à confirmer avec nous.",
        "p8_note": "Prix hors taxes, sous réserve de disponibilité. Surfaces indicatives.",
        "lot_eye": "Plan de vente", "lot_cta": "Réserver cet appartement",
        "lot_tva": "de TVA récupérable sur ce lot", "lot_inc_h": "Inclus",
        "lot_inc": ["Casier à ski", "Cave", "Parking couvert en face", "Cuisine équipée", "Parquet en chêne", "Conciergerie"],
        "tva_eye": "Simulation de TVA", "tva_h": "Vous achetez hors taxes. <em>La TVA vous revient.</em>",
        "tva_body": "L'appartement est exploité avec des services, comme à l'hôtel : quand vous n'êtes pas là, une conciergerie le loue. En contrepartie, vous achetez hors taxes et récupérez la TVA de 20 %, avec des frais de notaire réduits. Vous gardez vos séjours quand vous voulez.",
        "tva_rows": [("Prix de l'appartement, hors taxes", "620 000 €"), ("TVA à 20 %", "124 000 €"), ("Prix toutes taxes comprises", "744 000 €"), ("TVA récupérée", "− 124 000 €")],
        "tva_total": ("Votre coût net", "620 000 € HT"),
        "tva_big": "124 000 €", "tva_big_l": "qui vous reviennent sur un appartement à 620 000 € HT",
        "tva_cond_h": "Les conditions",
        "tva_cond": ["Services para-hôteliers assurés par une conciergerie", "Engagement de mise en location", "Liberté de séjourner chez vous quand vous le souhaitez", "Un expert-comptable fait les déclarations à votre place"],
        "tva_note": "Simulation indicative pour un appartement à 620 000 € HT. À valider avec votre conseil selon votre situation.",
        "rev_eye": "Les revenus", "rev_h": "Une résidence secondaire <em>qui rapporte.</em>",
        "rev_big": "≈ 27 000 €", "rev_big_l": "de revenus locatifs par an, pour un appartement à 620 000 €",
        "rev_yield": "4,4 % nets de gestion · 3,4 % après charges",
        "rev_points": [("La demande est là", "La moitié des visiteurs de la station viennent de l'étranger, en premier lieu les Britanniques."), ("Une station quatre saisons", "Le ski de fin novembre à début juillet grâce au glacier, puis le VTT, la randonnée, les lacs."), ("Pas de bail commercial", "Vous choisissez votre conciergerie, les loyers vous reviennent directement."), ("+40 % en cinq ans", "La progression des prix dans une station qui investit près de 150 M€ dans son téléphérique.")],
        "rev_note": "Rendements indicatifs, non garantis.",
        "svc_eye": "Sans jamais vous en occuper", "svc_h": "Propriétaire à la montagne, <em>comme à l'hôtel.</em>",
        "svc": [("La conciergerie", "Réservations, accueil des locataires, ménage, linge. Le jour où vous venez, l'appartement est prêt."), ("L'expert-comptable", "Il récupère votre TVA et fait toutes vos déclarations en France, y compris pour les non-résidents."), ("Dans votre langue", "Une agence internationale vous accompagne pendant tout l'achat."), ("Vos séjours", "Vous gardez vos semaines, quand vous voulez. Le reste du temps, l'appartement travaille pour vous.")],
        "st_eye": "Les 2 Alpes", "st_h": "Une station qui vit <em>presque toute l'année.</em>",
        "st_stats": [("1 650 m", "le village"), ("3 600 m", "le glacier"), ("200 km", "de pistes"), ("17 min", "jusqu'au glacier")],
        "st_winter_h": "L'hiver", "st_winter": ["Ski de fin novembre à début juillet", "Le Jandri, téléphérique neuf (2025, près de 150 M€)", "La Grave et la Meije juste derrière le glacier"],
        "st_summer_h": "L'été", "st_summer": ["Randonnée dans le Parc national des Écrins", "Lacs de montagne", "Bike park, VTT et parapente"],
        "acc_eye": "Accès", "acc_h": "Plus près <em>que vous ne le pensez.</em>",
        "acc": [("1 h 30", "de Grenoble"), ("2 h", "de l'aéroport de Lyon-Saint-Exupéry"), ("200 m", "des remontées, à pied")],
        "acc_body": "L'hiver, des vols directs relient Londres, Manchester, Bristol et Édimbourg à Grenoble. Sur place, la voiture reste au parking couvert en face de la résidence : tout se fait à pied, les pistes, la boulangerie, les magasins de ski et les soixante-dix restaurants de la station.",
        "cal_eye": "Calendrier", "cal_h": "Le bon moment, <em>c'est maintenant.</em>",
        "cal": [("Aujourd'hui", "Pré-réservation ouverte. Quatre appartements vendus, un sous offre."), ("Travaux", "Surélévation, toiture neuve, façades bois et pierre, aménagement intérieur."), ("2nd semestre 2028", "Livraison prévisionnelle.")],
        "cal_body": "Vendu sur plan : c'est le moment où le choix est le plus large, avant que les meilleurs étages et les plus belles expositions ne partent.",
        "fin_eye": "La suite", "fin_h": "Un appartement <em>vous attend.</em>",
        "fin_body": "Choisissez votre lot, posez vos questions, réservez. Nous répondons personnellement, dans votre langue.",
        "fin_btn": "Nous contacter",
        "fin_legal": "Document non contractuel · Perspectives 3D et photographies d'ambiance non contractuelles · Prix hors taxes, sous réserve de disponibilité · Rendements indicatifs non garantis.",
        "back": "Retour au site",
    },
    "en": {
        "lang": "en", "root": "/en/", "title": "Les Airelles, Les 2 Alpes — Project brochure",
        "desc": "Les Airelles, Les 2 Alpes project brochure: 3D renderings, floor plans, prices and VAT simulation.",
        "floor": lambda n: {1: "1st floor", 2: "2nd floor", 3: "3rd floor"}.get(n, f"{n}th floor"),
        "ht": "excl. VAT", "lot": "Lot", "surface": "Area", "floor_l": "Floor", "expo": "Aspect", "rooms": "Bedrooms",
        "persp": "3D rendering — non-contractual image",
        "contact": "A question? Chat with us on WhatsApp",
        "prev": "Previous page", "next": "Next page", "goto": "Go to page",
        "cover_kicker": "Project brochure · 2026 edition",
        "cover_pill": "Les 2 Alpes · French Alps · 1,650 m", "cover_brand": "Exceptional real estate",
        "cover_meta": "Confidential brochure · Non-contractual document",
        "m_eye": "Welcome to Les Airelles", "m_h": "Your premium apartment, <em>200 m from the slopes.</em>",
        "m_body": "On Place de Venosc, the historic heart of Les 2 Alpes, the former Hôtel Les Airelles becomes a residence of eleven new apartments. Natural stone, oak, carved wood, and wide picture windows onto the peaks.",
        "m_stats": [("200 m", "from the slopes"), ("11", "apartments"), ("3,600 m", "the glacier")],
        "cover_sub": "Eleven new apartments on Place de Venosc, two hundred metres from the slopes. Les 2 Alpes, 1,650 m.",
        "cover_foot": ("Sold off-plan", "Place de Venosc · 38860 Les 2 Alpes · France"),
        "p2_eye": "The setting", "p2_h": "The square where nothing <em>was ever for sale.</em>",
        "p2_body": [
            "Place de Venosc is the historic heart of Les 2 Alpes: terraces, restaurants, shops, and the lifts two hundred metres away. Everyone dreams of living here. Nothing was ever for sale.",
            "The former Hôtel Les Airelles is being completely reimagined as a residence of just eleven new apartments. The building gains an extra storey, a new roof, and timber and stone façades.",
        ],
        "p2_before": "Today", "p2_after": "Tomorrow",
        "p3_eye": "The project in figures", "p3_h": "The essentials, <em>at a glance.</em>",
        "p3_stats": [("11", "apartments only"), ("6", "still available"), ("200 m", "from the lifts"), ("59–140 m²", "from 2-bed to family residence"), ("8", "guests, up to"), ("20%", "VAT recovered")],
        "p3_list_h": "With every apartment",
        "p3_list": ["A ski locker and a private cellar", "Natural stone, oak parquet, carved wood", "Fully fitted kitchen", "A terrace for almost all", "Covered car park just opposite", "Concierge service for rentals"],
        "p4_eye": "The architecture", "p4_h": "Timber, stone, <em>evening light.</em>",
        "p4_body": "A contemporary chalet façade: timber cladding, a stone base, generous balconies. At night, under the snow, the residence glows at the heart of the resort.",
        "p5_eye": "The interiors", "p5_h": "Under the beams, <em>the peaks.</em>",
        "p5_body": "The top-floor living room opens beneath the timber roof structure, with a wide picture window onto the peaks. Noble, warm materials throughout.",
        "p5_mat": [("Natural stone", "Walls and details"), ("Solid oak", "Natural parquet"), ("Carved wood", "Alpine décor"), ("Picture windows", "Open onto the peaks")],
        "p6_eye": "The bedrooms", "p6_h": "Bedrooms for <em>the whole family.</em>",
        "p6_body": "Suites with their own shower rooms, and mountain nooks with bunk beds for the children. At least two shower rooms: nobody waits in the morning.",
        "p6_c1": "A bedroom, the summit in the window", "p6_c2": "The mountain nook, for the children",
        "p7_eye": "Wellbeing", "p7_h": "A steaming hot tub, <em>facing the slopes.</em>",
        "p7_body": "On the top floor, the terrace can take a hot tub facing the ski area. The large family apartment on the third floor has its own sauna.",
        "p8_eye": "Available apartments", "p8_h": "The price list, <em>€525,000 to €1,255,000 excl. VAT.</em>",
        "p8_th": ["Lot", "Type", "Area", "Floor", "Aspect", "Price excl. VAT"],
        "p8_status": "4 apartments sold · 1 under offer · 6 still available. Please confirm each lot's availability with us.",
        "p8_note": "Prices excluding VAT, subject to availability. Areas are indicative.",
        "lot_eye": "Sales plan", "lot_cta": "Reserve this apartment",
        "lot_tva": "of recoverable VAT on this lot", "lot_inc_h": "Included",
        "lot_inc": ["Ski locker", "Private cellar", "Covered car park opposite", "Fitted kitchen", "Oak parquet", "Concierge service"],
        "tva_eye": "VAT simulation", "tva_h": "You buy excluding VAT. <em>The VAT comes back to you.</em>",
        "tva_body": "The apartment is run with hotel-style services: when you are away, a concierge rents it out. In return, you buy excluding VAT and recover the 20% VAT, with reduced notary fees. You keep your stays whenever you like.",
        "tva_rows": [("Apartment price, excluding VAT", "€620,000"), ("VAT at 20%", "€124,000"), ("Price including VAT", "€744,000"), ("VAT recovered", "− €124,000")],
        "tva_total": ("Your net cost", "€620,000 excl. VAT"),
        "tva_big": "€124,000", "tva_big_l": "back to you on a €620,000 (excl. VAT) apartment",
        "tva_cond_h": "The conditions",
        "tva_cond": ["Hotel-style services provided by a concierge", "A commitment to rent the apartment out", "Freedom to stay whenever you wish", "A chartered accountant files your returns for you"],
        "tva_note": "Indicative simulation for a €620,000 (excl. VAT) apartment. To be confirmed with your adviser for your own situation.",
        "rev_eye": "Rental income", "rev_h": "A second home <em>that pays its way.</em>",
        "rev_big": "≈ €27,000", "rev_big_l": "of rental income a year, for a €620,000 apartment",
        "rev_yield": "4.4% net of management · 3.4% after charges",
        "rev_points": [("The demand is there", "Half of the resort's visitors come from abroad, led by the British."), ("A four-season resort", "Skiing from late November to early July thanks to the glacier, then mountain biking, hiking, lakes."), ("No commercial lease", "You choose your concierge, and the rent comes straight to you."), ("+40% in five years", "Price growth in a resort investing nearly €150m in its new cable car.")],
        "rev_note": "Indicative yields, not guaranteed.",
        "svc_eye": "Without lifting a finger", "svc_h": "Owning in the mountains, <em>the hotel way.</em>",
        "svc": [("The concierge", "Bookings, guest check-in, cleaning, linen. The day you arrive, the apartment is ready."), ("The accountant", "Recovers your VAT and files all your French returns, including for non-residents."), ("In your language", "An international agency guides you through the whole purchase."), ("Your stays", "Keep your weeks, whenever you like. The rest of the time, the apartment works for you.")],
        "st_eye": "Les 2 Alpes", "st_h": "A resort alive <em>almost all year round.</em>",
        "st_stats": [("1,650 m", "the village"), ("3,600 m", "the glacier"), ("200 km", "of pistes"), ("17 min", "to the glacier")],
        "st_winter_h": "Winter", "st_winter": ["Skiing from late November to early July", "The Jandri, a brand-new cable car (2025, nearly €150m)", "La Grave and La Meije just beyond the glacier"],
        "st_summer_h": "Summer", "st_summer": ["Hiking in the Écrins National Park", "Mountain lakes", "Bike park, mountain biking and paragliding"],
        "acc_eye": "Getting there", "acc_h": "Closer <em>than you think.</em>",
        "acc": [("1 h 30", "from Grenoble"), ("2 h", "from Lyon-Saint-Exupéry airport"), ("200 m", "to the lifts, on foot")],
        "acc_body": "In winter, direct flights link London, Manchester, Bristol and Edinburgh to Grenoble. Once there, the car stays in the covered car park opposite the residence: everything is on foot — the slopes, the bakery, the ski shops and the resort's seventy restaurants.",
        "cal_eye": "Timeline", "cal_h": "The right moment <em>is now.</em>",
        "cal": [("Today", "Pre-reservations open. Four apartments sold, one under offer."), ("Construction", "Extra storey, new roof, timber and stone façades, interior fit-out."), ("2nd half of 2028", "Expected completion.")],
        "cal_body": "Sold off-plan: this is when the choice is widest, before the best floors and finest aspects are gone.",
        "fin_eye": "Next steps", "fin_h": "An apartment <em>is waiting for you.</em>",
        "fin_body": "Choose your lot, ask your questions, reserve. We answer personally, in your language.",
        "fin_btn": "Contact us",
        "fin_legal": "Non-contractual document · 3D renderings and lifestyle photographs are non-contractual · Prices excluding VAT, subject to availability · Indicative yields, not guaranteed.",
        "back": "Back to the website",
    },
}

CSS = r"""
:root{--nuit:#0B1019;--bois:#0E141C;--miel:#8C5F24;--cta:#8A5E25;--ambre:#E2A85C;--neige:#FBFAF7;--neige2:#EFEAE3;--encre:#1B1612;--gris:rgba(27,22,18,.62);--ligne:rgba(27,22,18,.14);--serif:'Cormorant Garamond','Times New Roman',serif;--sans:'Jost',-apple-system,sans-serif;--scale:1}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#15171B}
body{font-family:var(--sans);color:var(--encre);font-size:10.5pt;line-height:1.55;font-weight:300;padding:1.25rem 1rem 6rem;-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%}
em{font-style:italic;color:var(--miel)}
.brochure{max-width:210mm;margin:0 auto;position:relative}
.page{width:210mm;height:297mm;margin:0 auto calc(1.5rem - (1 - var(--scale))*297mm);background:var(--neige);position:relative;overflow:hidden;box-shadow:0 16px 48px rgba(0,0,0,.45);padding:20mm 18mm;display:none;animation:fadeIn 320ms ease-out;transform:scale(var(--scale));transform-origin:top center}
.page.is-active{display:block}
.page--dark{background:var(--nuit);color:var(--neige);--miel:var(--ambre)}
.page--wood{background:var(--bois);color:var(--neige);--miel:var(--ambre)}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.eyebrow{font-size:7.5pt;letter-spacing:.32em;text-transform:uppercase;color:var(--miel);margin-bottom:3mm;font-weight:400}
.h2{font-family:var(--serif);font-weight:400;font-size:27pt;line-height:1.05;margin-bottom:5mm}
.rule{width:16mm;height:1px;background:var(--miel);margin:0 0 6mm}
.body{color:var(--gris);margin-bottom:4mm}
.page--dark .body,.page--wood .body{color:rgba(246,242,234,.75)}
.photo{position:relative;overflow:hidden;border-radius:1px}
.photo img{width:100%;height:100%;object-fit:cover}
.persp::after{content:attr(data-p);position:absolute;right:2.5mm;bottom:2mm;font-size:6pt;color:rgba(255,255,255,.85);text-shadow:0 1px 2px rgba(0,0,0,.6);letter-spacing:.04em}
.cap{font-size:8pt;color:var(--gris);margin-top:2mm}
.page-num{position:absolute;bottom:10mm;right:18mm;font-size:7.5pt;letter-spacing:.3em;color:var(--gris)}
.page--dark .page-num,.page--wood .page-num{color:rgba(246,242,234,.5)}
.page-num::before{content:'';display:inline-block;width:6mm;height:1px;background:var(--miel);vertical-align:middle;margin-right:2.5mm}
.brand-foot{position:absolute;bottom:10mm;left:18mm;font-family:var(--serif);font-size:9pt;letter-spacing:.2em;color:var(--gris)}
.page--dark .brand-foot,.page--wood .brand-foot{color:rgba(246,242,234,.5)}
.page-contact{position:absolute;bottom:8.5mm;left:50%;transform:translateX(-50%);display:inline-flex;align-items:center;gap:2mm;padding:2.2mm 5mm;background:#25D366;color:#fff;font-size:7pt;letter-spacing:.14em;text-transform:uppercase;font-weight:500;text-decoration:none;border-radius:100px;white-space:nowrap;box-shadow:0 4px 12px rgba(37,211,102,.3);z-index:3}
.page-contact:hover{background:#128C7E}
.page-contact svg{width:3.6mm;height:3.6mm;fill:currentColor}
/* Couverture */
.cover{padding:0;color:#fff;background:var(--nuit);--miel:var(--ambre)}
.cover>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cover::before{content:'';position:absolute;inset:0;background:linear-gradient(to top,rgba(8,12,19,.94) 0%,rgba(8,12,19,.45) 42%,rgba(8,12,19,.1) 68%,rgba(8,12,19,.55) 100%);z-index:1}
.cover::after{content:'';position:absolute;inset:7mm;border:1px solid rgba(226,168,92,.45);z-index:2;pointer-events:none}
.cover__c{position:relative;z-index:3;height:100%;display:flex;flex-direction:column;justify-content:space-between;padding:20mm 18mm 18mm}
.cover__brand img{width:42mm;height:auto;display:block}
.cover__brand small{display:block;font-size:6.8pt;letter-spacing:.3em;text-transform:uppercase;color:rgba(255,255,255,.75);margin-top:2mm}
.cover__pill{display:inline-flex;align-items:center;gap:2.2mm;padding:2mm 4.5mm;border:1px solid rgba(226,168,92,.6);border-radius:100px;font-size:7.2pt;letter-spacing:.22em;text-transform:uppercase;margin-bottom:6mm}
.cover__pill i{width:1.6mm;height:1.6mm;background:var(--ambre);transform:rotate(45deg)}
.cover h1{font-family:var(--serif);font-weight:400;font-size:56pt;line-height:.95;letter-spacing:.02em;text-transform:uppercase}
.cover h1 em{display:block;text-transform:none;font-weight:300;color:var(--ambre);font-size:.72em;letter-spacing:0;margin-top:2mm}
.cover__sub{font-size:10.5pt;max-width:120mm;margin-top:6mm;color:rgba(255,255,255,.88)}
.cover__meta{display:flex;justify-content:space-between;align-items:center;gap:6mm;margin-top:9mm;padding-top:4mm;border-top:1px solid rgba(255,255,255,.22);font-size:6.8pt;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.65)}
.cover__wa{display:inline-flex;align-items:center;gap:1.8mm;color:#fff;text-decoration:none;letter-spacing:.14em}
.cover__wa svg{width:3.6mm;height:3.6mm;fill:#25D366}
.cover .persp-c{position:absolute;right:18mm;top:20mm;z-index:3;font-size:6pt;opacity:.7}
/* Manifeste */
.manif{padding:0}
.manif__img{position:relative;height:168mm;overflow:hidden}
.manif__img img{width:100%;height:100%;object-fit:cover}
.manif__img::after{content:'';position:absolute;inset:auto 0 0 0;height:40%;background:linear-gradient(to top,var(--nuit),transparent)}
.manif__c{padding:2mm 18mm 0}
.manif .h2{font-size:30pt}
.mstats{display:grid;grid-template-columns:repeat(3,1fr);margin-top:7mm;border-top:1px solid rgba(226,168,92,.35)}
.mstats div{padding:5mm 0 0}
.mstats strong{display:block;font-family:var(--serif);font-weight:300;font-size:26pt;line-height:1;color:var(--ambre);font-variant-numeric:lining-nums}
.mstats span{display:block;margin-top:1.5mm;font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:rgba(246,242,234,.65)}
/* Avant/après */
.ba2{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin:6mm 0}
.ba2 .photo{aspect-ratio:4/3}
.tag{position:absolute;left:2.5mm;top:2.5mm;background:rgba(8,12,19,.7);color:#fff;font-size:6.5pt;letter-spacing:.2em;text-transform:uppercase;padding:1mm 2.5mm}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:8mm}
/* Stats */
.stats{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--ligne);border-left:1px solid var(--ligne);margin:6mm 0 8mm}
.stats div{border-right:1px solid var(--ligne);border-bottom:1px solid var(--ligne);padding:6mm 4mm}
.stats strong{display:block;font-family:var(--serif);font-weight:300;font-size:24pt;line-height:1;color:var(--miel);font-variant-numeric:lining-nums}
.stats span{display:block;margin-top:2mm;font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--gris)}
.page--dark .stats,.page--dark .stats div{border-color:rgba(246,242,234,.16)}
.page--dark .stats span{color:rgba(246,242,234,.65)}
.page--dark .stats strong{color:var(--ambre)}
.checks{list-style:none;columns:2;column-gap:8mm}
.checks li{position:relative;padding-left:6mm;margin-bottom:2.5mm;break-inside:avoid}
.checks li::before{content:'';position:absolute;left:0;top:.7em;width:3.5mm;height:1px;background:var(--miel)}
.h3{font-family:var(--serif);font-size:15pt;font-weight:500;margin-bottom:3mm}
/* Matières */
.mat{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:5mm}
.mat div{border-top:1px solid var(--miel);padding-top:3mm}
.mat strong{display:block;font-family:var(--serif);font-size:13pt;font-weight:500}
.mat span{font-size:8pt;color:var(--gris)}
/* Tableau */
table{width:100%;border-collapse:collapse;margin:6mm 0 4mm;font-size:9pt}
th{font-size:6.8pt;letter-spacing:.18em;text-transform:uppercase;color:var(--gris);font-weight:400;text-align:left;padding:2.5mm 2mm;border-bottom:1px solid var(--encre)}
td{padding:3.2mm 2mm;border-bottom:1px solid var(--ligne)}
td.n{font-family:var(--serif);font-size:13pt}
td.p,td.n,.lot-head .price strong,.sim strong,.specs strong{font-variant-numeric:lining-nums tabular-nums}
td.p{font-family:var(--serif);font-size:12.5pt;text-align:right;white-space:nowrap}
th:last-child{text-align:right}
tr.star td{background:rgba(148,101,38,.08)}
.status{display:inline-flex;gap:2mm;align-items:center;font-size:8.5pt;margin-top:2mm}
.status i{width:2.2mm;height:2.2mm;border-radius:50%;background:var(--miel)}
.note{font-size:7.5pt;color:var(--gris);margin-top:3mm}
/* Page lot */
.lot-head{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1px solid var(--ligne);padding-bottom:4mm;margin-bottom:5mm}
.lot-head .h2{margin:0}
.lot-head .price{text-align:right}
.lot-head .price strong{display:block;font-family:var(--serif);font-weight:400;font-size:24pt;line-height:1}
.lot-head .price span{font-size:7pt;letter-spacing:.2em;text-transform:uppercase;color:var(--gris)}
.plan{background:#fff;border:1px solid var(--ligne);padding:3mm;height:150mm;display:flex;align-items:center;justify-content:center}
.plan img{max-height:100%;width:auto;max-width:100%;object-fit:contain}
.specs{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:5mm}
.specs small{display:block;font-size:6.8pt;letter-spacing:.18em;text-transform:uppercase;color:var(--gris)}
.specs strong{font-family:var(--serif);font-weight:500;font-size:12.5pt;line-height:1.2}
.lotbox{display:grid;grid-template-columns:1fr 1.4fr;gap:5mm;margin-top:6mm;border-top:1px solid var(--ligne);padding-top:5mm}
.lotbox .big{font-size:26pt}
.lotbox ul{list-style:none;columns:2;column-gap:5mm;font-size:8.5pt}
.lotbox li{padding:1mm 0 1mm 4.5mm;position:relative;break-inside:avoid}
.lotbox li::before{content:'';position:absolute;left:0;top:.75em;width:2.5mm;height:1px;background:var(--miel)}
.extra{margin-top:4mm;display:inline-block;background:rgba(148,101,38,.14);padding:1.5mm 3mm;font-size:8.5pt}
/* TVA */
.sim{border:1px solid var(--ligne);margin:5mm 0}
.sim div{display:flex;justify-content:space-between;padding:3.2mm 5mm;border-bottom:1px solid var(--ligne)}
.sim div:last-child{border-bottom:0}
.sim strong{font-family:var(--serif);font-weight:500;font-size:12.5pt}
.sim .tot{background:var(--nuit);color:var(--neige)}
.sim .tot strong{color:var(--ambre);font-size:14pt}
.sim .rec strong{color:#5E7D5A}
.big{font-family:var(--serif);font-weight:300;font-size:46pt;line-height:1;color:var(--miel);font-variant-numeric:lining-nums}
.page--dark .big,.page--wood .big{color:var(--ambre)}
.bigl{font-size:9pt;color:var(--gris);margin-top:2mm}
.page--dark .bigl,.page--wood .bigl{color:rgba(246,242,234,.7)}
.yield{display:inline-block;margin-top:4mm;border:1px solid var(--ambre);color:var(--ambre);padding:2mm 4mm;font-size:8.5pt;letter-spacing:.06em}
.pts{display:grid;grid-template-columns:1fr 1fr;gap:6mm 8mm;margin-top:8mm}
.pts strong{display:block;font-family:var(--serif);font-weight:500;font-size:14pt;margin-bottom:1.5mm}
.pts p{font-size:9pt;color:var(--gris)}
.page--dark .pts p,.page--wood .pts p{color:rgba(246,242,234,.72)}
.num{display:block;font-family:var(--serif);color:var(--miel);margin-bottom:1mm}
/* Station */
.seasons2{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:5mm}
.seasons2 .photo{height:62mm}
.seasons2 ul{list-style:none;margin-top:3mm;font-size:9pt}
.seasons2 li{padding:1.3mm 0;border-bottom:1px solid var(--ligne)}
/* Calendrier */
.tl{border-left:1px solid var(--miel);margin:8mm 0 8mm 2mm;padding-left:8mm}
.tl div{position:relative;margin-bottom:8mm}
.tl div::before{content:'';position:absolute;left:-10mm;top:2.2mm;width:3.5mm;height:3.5mm;border-radius:50%;background:var(--miel)}
.tl strong{display:block;font-family:var(--serif);font-size:17pt;font-weight:400}
.tl span{color:rgba(246,242,234,.75)}
/* Fin */
.final{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;height:100%;position:relative;z-index:2}
.final .h2{font-size:34pt}
.final .body{max-width:120mm}
.final__btn{display:inline-flex;margin-top:8mm;padding:4mm 8mm;background:var(--cta);color:#fff;text-decoration:none;font-size:8pt;letter-spacing:.22em;text-transform:uppercase}
.final__legal{position:absolute;left:18mm;right:18mm;bottom:12mm;text-align:center;font-size:6.5pt;color:rgba(246,242,234,.5);z-index:2}
.back{display:inline-block;margin-top:6mm;font-size:7.5pt;letter-spacing:.2em;text-transform:uppercase;color:rgba(246,242,234,.7)}
/* Navigation */
.nav-bar{position:fixed;bottom:1.25rem;left:50%;transform:translateX(-50%);background:rgba(8,12,19,.94);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);padding:.45rem .6rem;border-radius:100px;display:flex;align-items:center;gap:.35rem;z-index:1000;box-shadow:0 14px 40px rgba(0,0,0,.4)}
.nav-btn{width:44px;height:44px;display:flex;align-items:center;justify-content:center;background:transparent;border:0;color:#F6F2EA;cursor:pointer;border-radius:50%}
.nav-btn:hover{background:rgba(246,242,234,.1)}
.nav-btn:disabled{opacity:.25;cursor:default}
:focus-visible{outline:2px solid var(--ambre);outline-offset:3px}
.nav-btn svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:1.8}
.nav-counter{font-size:.7rem;letter-spacing:.2em;color:var(--ambre);font-family:var(--serif);padding:0 .7rem;min-width:64px;text-align:center;white-space:nowrap}
.nav-dots{display:flex;gap:5px;padding:0 .5rem 0 .75rem;border-left:1px solid rgba(246,242,234,.15);margin-left:.25rem}
.dot{width:6px;height:6px;border-radius:50%;background:rgba(246,242,234,.25);border:0;cursor:pointer;padding:0}
.dot.is-active{background:var(--ambre);transform:scale(1.45)}
.lang{position:fixed;top:1rem;right:1rem;z-index:1000;display:flex;gap:.3rem;background:rgba(8,12,19,.85);padding:.35rem .5rem;border-radius:100px;font-size:.7rem;letter-spacing:.16em}
.lang a{color:#F6F2EA;text-decoration:none;padding:.2rem .45rem;opacity:.55}
.lang a.is-active{opacity:1;color:var(--ambre)}
/* Pages A4 : la dernière photo remplit l'espace libre jusqu'au pied de page */
@media (min-width:907px){
  .page.is-active:not(.cover){display:flex;flex-direction:column;padding-bottom:24mm}
  .page>*{flex-shrink:0}
  .page>.photo.grow,.page>.cols.grow{flex:1 1 0;min-height:30mm;height:auto!important}
  .page>.cols.grow>.photo{height:100%!important}
  .manif.is-active .manif__img{flex:1 1 0;height:auto;min-height:150mm}
  .manif.is-active{padding-bottom:26mm}
}
/* Responsive : sous la largeur A4, les pages s'empilent */
@media (max-width:906px){
  body{padding:0 0 6rem;font-size:10pt}
  .page{width:100%;height:auto;min-height:0;padding:12mm 7mm 26mm;margin:0 0 .75rem;transform:none}
  .cover{min-height:92vh;padding:0}
  .cover__c{min-height:92vh;padding:16mm 7mm 10mm}
  .cover .persp-c{top:auto;bottom:4mm;right:7mm}
  .cover::after{inset:4mm}
  .manif__img{height:62vw}
  .manif__c{padding:2mm 7mm 0}
  .cover__meta{flex-direction:column;align-items:flex-start}
  .cover h1{font-size:40pt}
  .h2{font-size:22pt}
  .cols,.ba2,.seasons2,.pts{grid-template-columns:1fr}
  .stats{grid-template-columns:repeat(2,1fr)}
  .mat,.specs{grid-template-columns:repeat(2,1fr)}
  .checks{columns:1}
  .plan{height:auto}
  .photo[style*="height"]{height:56vw!important}
  table{font-size:8pt}
  th:nth-child(5),td:nth-child(5){display:none}
  .final{min-height:80vh}
  .final__legal{position:static;margin-top:8mm}
  .page-contact{bottom:9mm}
  .nav-dots{display:none}
}
@media print{
  html,body{background:#fff;padding:0}
  .page{display:block!important;box-shadow:none;margin:0;transform:none;page-break-after:always}
  .nav-bar,.lang{display:none}
}
"""

JS = r"""
(() => {
  const pages = document.querySelectorAll('.page');
  const total = pages.length;
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const counter = document.getElementById('navCounter');
  const dotsEl = document.getElementById('navDots');
  const label = dotsEl.dataset.label;
  let current = 1;
  for (let i = 1; i <= total; i++) {
    const dot = document.createElement('button');
    dot.className = 'dot' + (i === 1 ? ' is-active' : '');
    dot.setAttribute('aria-label', `${label} ${i}`);
    dot.addEventListener('click', () => goTo(i));
    dotsEl.appendChild(dot);
  }
  const dots = dotsEl.querySelectorAll('.dot');
  const pad = n => String(n).padStart(2, '0');
  const goTo = n => {
    if (n < 1 || n > total) return;
    pages.forEach((p, i) => p.classList.toggle('is-active', i + 1 === n));
    dots.forEach((d, i) => d.classList.toggle('is-active', i + 1 === n));
    counter.textContent = `${pad(n)} / ${pad(total)}`;
    prevBtn.disabled = n === 1;
    nextBtn.disabled = n === total;
    current = n;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };
  prevBtn.addEventListener('click', () => goTo(current - 1));
  nextBtn.addEventListener('click', () => goTo(current + 1));
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(current - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); goTo(current + 1); }
  });
  // Swipe sur mobile
  let x0 = null;
  document.addEventListener('touchstart', e => { x0 = e.changedTouches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 60) goTo(current + (dx < 0 ? 1 : -1));
    x0 = null;
  }, { passive: true });
  // La page A4 tient entière dans la fenêtre
  const updateScale = () => {
    const MM = 3.7795275591, pageH = 297 * MM, pageW = 210 * MM;
    if (window.innerWidth < 907) { document.documentElement.style.setProperty('--scale', 1); return; }
    const scale = Math.min((window.innerHeight - 130) / pageH, (window.innerWidth - 80) / pageW, 1);
    document.documentElement.style.setProperty('--scale', scale);
  };
  window.addEventListener('resize', updateScale);
  updateScale();
  // Mémorise le choix de langue
  document.querySelectorAll('.lang a').forEach(a => a.addEventListener('click', () => {
    try { localStorage.setItem('langChoice', a.getAttribute('lang')); } catch (e) {}
  }));
})();
"""


def img(name, w, alt="", cls=""):
    return f'<img src="/assets/img/{name}-{w}.webp" alt="{alt}" loading="lazy" decoding="async"{cls} />'


def build(lang):
    t = T[lang]
    P = t["persp"]
    pages = []
    num = [0]

    def contact():
        if not CONTACT_URL:
            return ""
        return f'<a class="page-contact" href="{CONTACT_URL}" target="_blank" rel="noopener noreferrer">{WA_SVG}{t["contact"]}</a>'

    def page(body, cls="", foot=True):
        num[0] += 1
        # La dernière photo de la page s'étire pour remplir la page A4 jusqu'au pied
        last = body.rstrip().splitlines()[-1] if body.strip() else ""
        if cls not in ("cover", "manif") and last.startswith('<div class="cols"') and 'class="photo' in last:
            k = body.rfind('<div class="cols"')
            body = body[:k] + '<div class="cols grow"' + body[k + len('<div class="cols"'):]
        else:
            i = body.rfind('class="photo')
            if i >= 0 and cls not in ("cover", "manif"):
                body = body[:i] + 'class="photo grow' + body[i + len('class="photo'):]
        f = f'<div class="brand-foot">LES AIRELLES</div>{contact()}<div class="page-num">{num[0]:02d}</div>' if foot else ""
        active = " is-active" if num[0] == 1 else ""
        pages.append(f'<section class="page{(" " + cls) if cls else ""}{active}" data-page="{num[0]}">\n{body}\n{f}\n</section>')

    # 1 — Couverture
    page(f'''<img src="/assets/img/facade-nuit-2560.webp" alt="" />
<span class="persp-c">{P}</span>
<div class="cover__c">
  <div class="cover__brand"><img src="/assets/brand/prodigio-blanc.png" alt="Prodigio" /><small>{t["cover_brand"]}</small></div>
  <div class="cover__title">
    <div class="cover__pill"><i></i>{t["cover_pill"]}</div>
    <h1>Les Airelles<em>aux 2 Alpes</em></h1>
    <p class="cover__sub">{t["cover_sub"]}</p>
    <div class="cover__meta"><span>{t["cover_meta"]}</span><a class="cover__wa" href="{CONTACT_URL}" target="_blank" rel="noopener noreferrer">{WA_SVG}WhatsApp</a></div>
  </div>
</div>''', "cover", foot=False)

    # 2 — Manifeste
    ms = "".join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in t["m_stats"])
    page(f'''<div class="manif__img persp" data-p="{P}"><img src="/assets/img/sejour-2560.webp" alt="" /></div>
<div class="manif__c">
  <div class="eyebrow">{t["m_eye"]}</div>
  <h2 class="h2">{t["m_h"]}</h2>
  <p class="body">{t["m_body"]}</p>
  <div class="mstats">{ms}</div>
</div>''', "page--dark manif")

    # 2 — Le lieu
    page(f'''<div class="eyebrow">{t["p2_eye"]}</div>
<h2 class="h2">{t["p2_h"]}</h2><div class="rule"></div>
<div class="ba2">
  <div class="photo"><img src="/assets/img/facade-avant-1000.webp" alt="" loading="lazy" /><span class="tag">{t["p2_before"]}</span></div>
  <div class="photo persp" data-p="{P}"><img src="/assets/img/facade-apres-1280.webp" alt="" loading="lazy" /><span class="tag">{t["p2_after"]}</span></div>
</div>
<div class="cols"><p class="body">{t["p2_body"][0]}</p><p class="body">{t["p2_body"][1]}</p></div>
<div class="photo" style="height:62mm;margin-top:2mm"><img src="/assets/img/station-ete-1000.webp" alt="" loading="lazy" /></div>''')

    # 3 — Chiffres
    stats = "".join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in t["p3_stats"])
    checks = "".join(f"<li>{x}</li>" for x in t["p3_list"])
    page(f'''<div class="eyebrow">{t["p3_eye"]}</div>
<h2 class="h2">{t["p3_h"]}</h2><div class="rule"></div>
<div class="stats">{stats}</div>
<div class="h3">{t["p3_list_h"]}</div>
<ul class="checks">{checks}</ul>
<div class="photo" style="height:78mm;margin-top:6mm"><img src="/assets/img/feu-cheminee-1280.webp" alt="" loading="lazy" /></div>''')

    # 4 — Architecture
    page(f'''<div class="eyebrow">{t["p4_eye"]}</div>
<h2 class="h2">{t["p4_h"]}</h2><div class="rule"></div>
<p class="body" style="max-width:140mm">{t["p4_body"]}</p>
<div class="photo persp" data-p="{P}" style="height:118mm;margin-top:4mm"><img src="/assets/img/facade-nuit-1920.webp" alt="" loading="lazy" /></div>
<div class="photo" style="height:52mm;margin-top:4mm"><img src="/assets/img/aube-sommets-1280.webp" alt="" loading="lazy" /></div>''', "page--dark")

    # 5 — Intérieur
    mats = "".join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in t["p5_mat"])
    page(f'''<div class="eyebrow">{t["p5_eye"]}</div>
<h2 class="h2">{t["p5_h"]}</h2><div class="rule"></div>
<p class="body" style="max-width:140mm">{t["p5_body"]}</p>
<div class="photo persp" data-p="{P}" style="height:112mm;margin-top:3mm"><img src="/assets/img/sejour-1920.webp" alt="" loading="lazy" /></div>
<div class="mat">{mats}</div>
<div class="cols" style="margin-top:5mm;gap:4mm"><div class="photo" style="height:40mm"><img src="/assets/img/chalet-feu-828.webp" alt="" loading="lazy" /></div><div class="photo" style="height:40mm"><img src="/assets/img/fenetre-bois-828.webp" alt="" loading="lazy" /></div></div>''')

    # 6 — Chambres
    page(f'''<div class="eyebrow">{t["p6_eye"]}</div>
<h2 class="h2">{t["p6_h"]}</h2><div class="rule"></div>
<p class="body" style="max-width:140mm">{t["p6_body"]}</p>
<div class="photo persp" data-p="{P}" style="height:96mm;margin-top:3mm"><img src="/assets/img/chambre-1920.webp" alt="" loading="lazy" /></div>
<p class="cap">{t["p6_c1"]}</p>
<div class="photo persp" data-p="{P}" style="height:96mm;margin-top:4mm"><img src="/assets/img/coin-montagne-1920.webp" alt="" loading="lazy" /></div>
<p class="cap">{t["p6_c2"]}</p>''')

    # 7 — Bien-être
    page(f'''<div class="eyebrow">{t["p7_eye"]}</div>
<h2 class="h2">{t["p7_h"]}</h2><div class="rule"></div>
<p class="body" style="max-width:140mm">{t["p7_body"]}</p>
<div class="photo persp" data-p="{P}" style="height:122mm;margin-top:3mm"><img src="/assets/img/terrasse-1920.webp" alt="" loading="lazy" /></div>
<div class="cols" style="margin-top:4mm;gap:4mm"><div class="photo" style="height:58mm"><img src="/assets/img/jacuzzi-neige-828.webp" alt="" loading="lazy" /></div><div class="photo" style="height:58mm"><img src="/assets/img/vin-chaud-828.webp" alt="" loading="lazy" /></div></div>''', "page--wood")

    # 8 — Tableau des lots
    rows = ""
    for L in LOTS:
        n, tfr, ten, m2, fl, efr, een, cfr, cen, xfr, xen, pfr, pen = L
        typ = tfr if lang == "fr" else ten
        expo = efr if lang == "fr" else een
        price = f"{pfr} €" if lang == "fr" else f"€{pen}"
        star = ' class="star"' if n in (12, 13) else ""
        rows += f'<tr{star}><td class="n">{n}</td><td>{typ}</td><td>{m2} m²</td><td>{t["floor"](fl)}</td><td>{expo}</td><td class="p">{price}</td></tr>'
    th = "".join(f"<th>{x}</th>" for x in t["p8_th"])
    page(f'''<div class="eyebrow">{t["p8_eye"]}</div>
<h2 class="h2">{t["p8_h"]}</h2><div class="rule"></div>
<div class="status"><i></i>{t["p8_status"]}</div>
<table><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>
<p class="note">{t["p8_note"]}</p>
<div class="photo" style="height:60mm;margin-top:6mm"><img src="/assets/img/famille-neige-1280.webp" alt="" loading="lazy" /></div>''')

    # 9 à 17 — Une page par lot
    for L in LOTS:
        n, tfr, ten, m2, fl, efr, een, cfr, cen, xfr, xen, pfr, pen = L
        fr = lang == "fr"
        price = f"{pfr} €" if fr else f"€{pen}"
        extra = (xfr if fr else xen)
        extra_html = f'<div class="extra">{extra}</div>' if extra else ""
        v = round(int(pfr.replace(" ", "")) * 0.2)
        tva = f"{v:,} €".replace(",", " ") if fr else f"€{v:,}"
        inc = "".join(f"<li>{x}</li>" for x in t["lot_inc"])
        page(f'''<div class="eyebrow">{t["lot_eye"]} · {t["lot"]} {n}</div>
<div class="lot-head"><h2 class="h2">{tfr if fr else ten}</h2><div class="price"><strong>{price}</strong><span>{t["ht"]}</span></div></div>
<div class="plan"><img src="/assets/plans/lot-{n:02d}-1800.webp" alt="{t["lot"]} {n}" loading="lazy" /></div>
<div class="specs">
  <div><small>{t["surface"]}</small><strong>{m2} m²</strong></div>
  <div><small>{t["floor_l"]}</small><strong>{t["floor"](fl)}</strong></div>
  <div><small>{t["expo"]}</small><strong>{efr if fr else een}</strong></div>
  <div><small>{t["rooms"]}</small><strong>{cfr if fr else cen}</strong></div>
</div>
{extra_html}
<div class="lotbox">
  <div><div class="big">{tva}</div><p class="bigl">{t["lot_tva"]}</p></div>
  <div><div class="h3">{t["lot_inc_h"]}</div><ul>{inc}</ul></div>
</div>''')

    # TVA
    sim = "".join(f'<div class="{"rec" if i == 3 else ""}"><span>{a}</span><strong>{b}</strong></div>' for i, (a, b) in enumerate(t["tva_rows"]))
    cond = "".join(f"<li>{x}</li>" for x in t["tva_cond"])
    page(f'''<div class="eyebrow">{t["tva_eye"]}</div>
<h2 class="h2">{t["tva_h"]}</h2><div class="rule"></div>
<p class="body">{t["tva_body"]}</p>
<div class="cols" style="align-items:center;margin-top:4mm">
  <div><div class="big">{t["tva_big"]}</div><p class="bigl">{t["tva_big_l"]}</p></div>
  <div class="sim">{sim}<div class="tot"><span>{t["tva_total"][0]}</span><strong>{t["tva_total"][1]}</strong></div></div>
</div>
<div class="h3" style="margin-top:6mm">{t["tva_cond_h"]}</div>
<ul class="checks">{cond}</ul>
<div class="photo" style="height:52mm;margin-top:5mm"><img src="/assets/img/serviettes-1280.webp" alt="" loading="lazy" /></div>
<p class="note">{t["tva_note"]}</p>''')

    # Revenus
    pts = "".join(f'<div><strong>{a}</strong><p>{b}</p></div>' for a, b in t["rev_points"])
    page(f'''<div class="eyebrow">{t["rev_eye"]}</div>
<h2 class="h2">{t["rev_h"]}</h2><div class="rule"></div>
<div class="big">{t["rev_big"]}</div><p class="bigl">{t["rev_big_l"]}</p>
<div class="yield">{t["rev_yield"]}</div>
<div class="pts">{pts}</div>
<div class="photo" style="height:62mm;margin-top:8mm"><img src="/assets/img/village-aube-1280.webp" alt="" loading="lazy" /></div>
<p class="note" style="color:rgba(246,242,234,.55)">{t["rev_note"]}</p>''', "page--dark")

    # Service
    svc = "".join(f'<div><span class="num">0{i + 1}</span><strong>{a}</strong><p>{b}</p></div>' for i, (a, b) in enumerate(t["svc"]))
    page(f'''<div class="eyebrow">{t["svc_eye"]}</div>
<h2 class="h2">{t["svc_h"]}</h2><div class="rule"></div>
<div class="photo" style="height:92mm"><img src="/assets/img/pieds-feu-1280.webp" alt="" loading="lazy" /></div>
<div class="pts">{svc}</div>''')

    # Station
    st = "".join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in t["st_stats"])
    w = "".join(f"<li>{x}</li>" for x in t["st_winter"])
    s = "".join(f"<li>{x}</li>" for x in t["st_summer"])
    page(f'''<div class="eyebrow">{t["st_eye"]}</div>
<h2 class="h2">{t["st_h"]}</h2><div class="rule"></div>
<div class="stats" style="grid-template-columns:repeat(4,1fr);margin:3mm 0 4mm">{st}</div>
<div class="seasons2">
  <div><div class="photo"><img src="/assets/img/poudreuse-1280.webp" alt="" loading="lazy" /></div><div class="h3" style="margin-top:4mm">{t["st_winter_h"]}</div><ul>{w}</ul></div>
  <div><div class="photo"><img src="/assets/img/lac-ete-1280.webp" alt="" loading="lazy" /></div><div class="h3" style="margin-top:4mm">{t["st_summer_h"]}</div><ul>{s}</ul></div>
</div>
<div class="photo" style="height:44mm;margin-top:5mm"><img src="/assets/img/telepherique-1280.webp" alt="" loading="lazy" /></div>''')

    # Accès
    acc = "".join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in t["acc"])
    page(f'''<div class="eyebrow">{t["acc_eye"]}</div>
<h2 class="h2">{t["acc_h"]}</h2><div class="rule"></div>
<div class="stats">{acc}</div>
<p class="body">{t["acc_body"]}</p>
<div class="photo" style="height:120mm;margin-top:6mm"><img src="/assets/img/ski-glacier-1920.webp" alt="" loading="lazy" /></div>''', "page--dark")

    # Calendrier
    cal = "".join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in t["cal"])
    page(f'''<div class="eyebrow">{t["cal_eye"]}</div>
<h2 class="h2">{t["cal_h"]}</h2><div class="rule"></div>
<div class="tl">{cal}</div>
<p class="body" style="max-width:140mm">{t["cal_body"]}</p>
<div class="photo persp" data-p="{P}" style="height:96mm;margin-top:6mm"><img src="/assets/img/facade-apres-1280.webp" alt="" loading="lazy" /></div>''', "page--wood")

    # Fin
    btn = f'<a class="final__btn" href="{CONTACT_URL}" target="_blank" rel="noopener noreferrer">{t["fin_btn"]}</a>' if CONTACT_URL else ""
    page(f'''<img src="/assets/img/facade-nuit-1920.webp" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.35" />
<div class="final">
  <div class="eyebrow">{t["fin_eye"]}</div>
  <h2 class="h2">{t["fin_h"]}</h2>
  <p class="body">{t["fin_body"]}</p>
  {btn}
  <a class="back" href="{t["root"]}">{t["back"]}</a>
</div>
<div class="final__legal">© 2026 Les Airelles aux 2 Alpes — {t["fin_legal"]}</div>''', "page--dark", foot=False)

    total = num[0]
    fr_active = ' class="is-active" aria-current="true"' if lang == "fr" else ""
    en_active = ' class="is-active" aria-current="true"' if lang == "en" else ""
    return f'''<!DOCTYPE html>
<html lang="{t["lang"]}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="noindex, nofollow" />
<title>{t["title"]}</title>
<meta name="description" content="{t["desc"]}" />
<link rel="alternate" hreflang="fr" href="/brochure/" />
<link rel="alternate" hreflang="en" href="/en/brochure/" />
<link rel="alternate" hreflang="x-default" href="/brochure/" />
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet" />
<!-- Fichier généré par _tools/gen_brochure.py : modifier le script, pas ce fichier. -->
<style>{CSS}</style>
</head>
<body>
<nav class="lang" aria-label="Langue / Language"><a href="/brochure/" lang="fr" hreflang="fr"{fr_active}>FR</a><a href="/en/brochure/" lang="en" hreflang="en"{en_active}>EN</a></nav>
<div class="brochure">
{chr(10).join(pages)}
</div>
<nav class="nav-bar" aria-label="Brochure">
  <button class="nav-btn" id="prevBtn" aria-label="{t["prev"]}" disabled><svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
  <div class="nav-counter" id="navCounter">01 / {total:02d}</div>
  <button class="nav-btn" id="nextBtn" aria-label="{t["next"]}"><svg viewBox="0 0 24 24"><path d="M9 18l6-6-6-6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
  <div class="nav-dots" id="navDots" data-label="{t["goto"]}"></div>
</nav>
<script>{JS}</script>
</body>
</html>
'''


if __name__ == "__main__":
    for lang, out in (("fr", ROOT / "brochure" / "index.html"), ("en", ROOT / "en" / "brochure" / "index.html")):
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build(lang), encoding="utf-8")
        print("écrit", out.relative_to(ROOT))
