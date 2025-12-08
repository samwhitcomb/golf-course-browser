import json
import re
from pathlib import Path

# Read courses.json
with open('courses.json', 'r', encoding='utf-8') as f:
    courses = json.load(f)

# Manual descriptions from the user's attached selection
additional_descriptions = {
    "Valderrama Golf Club": [
        "Located in the sun-drenched hills of Sotogrande, Spain, Valderrama is Robert Trent Jones Sr.'s 1974 masterpiece, famously tightened and refined by the club in the 1980s. Its character is defined by incredibly narrow, tree-lined fairways of cork oak, small, fiercely guarded greens, and immaculate, green-tinted sand in its strategic bunkers. The par-5 17th, with its creek-guarded layup and two-tiered green, is one of Europe's most famous risk-reward holes, having decided the fate of the 1997 Ryder Cup.",
        "The experience is one of intense precision and strategy, where position off every tee is non-negotiable. The heavy, clay-based soil can play surprisingly firm and fast. As the perennial host of the Volvo Masters and the seminal 1997 Ryder Cup—the first held on continental Europe—it cemented its reputation as the continent's premier championship test. Golfers remember it for its flawless, demanding conditioning and the claustrophobic pressure of threading shots through its iconic, arboreal corridors."
    ],
    "Le Golf National (Albatros Course)": [
        "Built for the 1991 French Open and now its permanent home, the Albatros Course near Paris is a modern, stadium-style design by Hubert Chesneau and Robert Von Hagge. Its character is defined by vast, sculpted lakes and winding streams that come into play on 14 holes, creating a dramatic, risk-reward spectacle. The final four holes, known as \"The Finish,\" are a brutal and thrilling amphitheater, with water menacing every shot into the par-3 16th and the long, watery par-4 18th.",
        "Playing here is a test of nerve and execution under pressure, designed to create drama for spectators. The rough is thick, and the wind can whip across the open property. It achieved global fame by hosting the epic 2018 Ryder Cup, where the European team's mastery of its perils was decisive. Golfers remember Le Golf National for its unapologetically modern, penal design and the electric atmosphere of its stadium layout, a stark contrast to Europe's classic heathland and links courses."
    ],
    "Morfontaine Golf Club (Vallière Course)": [
        "Hidden in the forest of Chantilly, Tom Simpson's 1927 design is considered the most beautiful and natural heathland course in France, if not all of Europe. The routing is a work of genius, flowing seamlessly through a secluded forest of pine, birch, and heather without a single weak hole. Its character is defined by wild, undulating fairways, exquisitely shaped bunkers that blend into the landscape, and brilliantly contoured greens that demand imaginative approach play.",
        "The experience is one of pure, serene, and strategic golf on fast-running, sandy soil. There are no housing developments or distractions—only the game and the forest. Its exclusivity and perfection have earned it a cult-like reverence among global architecture aficionados. Golfers remember Morfontaine for its sublime tranquility, the flawless harmony between the course and its natural setting, and the feeling of playing a perfectly preserved work of art from the golden age of design."
    ],
    "Oitavos Dunes": [
        "Nestled within a protected natural park in Cascais, Portugal, Arthur Hills' 2001 design is a stunning and sustainable links-style course. It plays over rolling, sandy terrain covered in native dunes vegetation with constant, panoramic views of the Atlantic Ocean and the Sintra mountains. The par-4 6th, playing along an oceanfront cliff, and the long, demanding par-4 18th back to the modernist clubhouse are standout holes that encapsulate its scenic and challenging character.",
        "The experience is defined by the strong coastal winds and firm, fast conditions that reward the ground game. Environmental stewardship is paramount, with minimal irrigation and a focus on native flora. It has hosted the Portuguese Open multiple times, showcasing its championship quality. Golfers remember Oitavos for its breathtaking natural beauty, its eco-friendly ethos, and the rare gift of a true, walkable links experience under the reliable sun of the Iberian coast."
    ],
    "Golf de Chantilly (Vineuil Course)": [
        "Located in the historic heart of French golf near the Château de Chantilly, the Vineuil Course is a classic 1909 Tom Simpson design built on perfect sandy soil. It is a quintessential heathland masterpiece, featuring tree-lined fairways, majestic stands of oak and pine, and strategic bunkering that frames each hole beautifully. The opening stretch, particularly the par-4 2nd and 3rd, and the challenging finish are revered for their strategic demands and timeless beauty.",
        "Playing Chantilly is a walk through history, with a refined, traditional atmosphere. The course demands thoughtful positioning and precise iron play to its subtly contoured greens. It has hosted the French Open more than a dozen times, testing legends from Henry Cotton to Seve Ballesteros. Golfers remember it for its elegant, parkland beauty, its strategic sophistication, and the palpable sense of playing one of continental Europe's most historic and dignified championship venues."
    ],
    "Hirono Golf Club": [
        "Often called \"The Pine Valley of the East,\" Hirono in Kobe is C.H. Alison's 1932 masterpiece and Japan's undisputed architectural crown jewel. Carved through dense pine forests and dramatic, rugged valleys, the course features dramatic elevation changes, deep, penal bunkers, and brilliantly sited greens. The par-4 7th, descending into a valley, and the perilous par-3 11th over a deep ravine are world-class holes that define its challenging and majestic character.",
        "The experience is one of awe and rigorous examination, where accuracy and strategy are paramount on every shot. The club maintains an atmosphere of profound tradition and reverence for the game. Consistently ranked as the number one course in Japan, its influence on Asian golf is immeasurable. Golfers remember Hirono for its perfect fusion of breathtaking natural terrain with Alison's bold, strategic design, creating a secluded and unforgettable pilgrimage."
    ],
    "Kasumigaseki Country Club (East Course)": [
        "The East Course, a 1929 Kinya Fujita design later renovated by Tom and Logan Fazio, is a classic, tree-lined parkland that became the center of the golf world during the 2020 Olympics. Its character blends traditional Japanese golf with modern championship refinements, featuring strategic bunkering, subtly contoured greens, and beautiful stands of Japanese zelkova and pine trees. The risk-reward par-5 18th, with its creek-crossing approach, provided a dramatic finale for the Olympic competition.",
        "Playing Kasumigaseki is a test of precision and course management on impeccably groomed surfaces. The course's ability to challenge the world's best while remaining fair was proven during the Olympic events. As one of Japan's most historic clubs, it has hosted numerous Japan Opens. Golfers remember it for its dignified atmosphere, its flawless conditioning, and its place in history as the stage where Xander Schauffele and Nelly Korda won Olympic gold."
    ],
    "Nine Bridges (Jeju Island)": [
        "Located on the volcanic island of Jeju, Nine Bridges is a stunning 2001 design by Ronald Fream and David Dale that masterfully incorporates natural and man-made elements. The front nine plays through a rugged, wooded valley, while the back nine opens to dramatic vistas with large lakes and rock formations. Its signature is the par-3 16th, featuring a green on a peninsula in a lake, and the par-5 18th, which plays around water back to the iconic clubhouse.",
        "The experience blends resort luxury with a serious, strategic championship test. The wind is a constant factor, and the course conditions are perpetually pristine. It has hosted the PGA Tour's CJ Cup for multiple years, introducing its quality to a global audience. Golfers remember Nine Bridges for its dramatic beauty, the seamless blend of its two distinct nines, and its status as the flagship course of Korean golf."
    ],
    "Leopard Creek Country Club": [
        "Designed by Gary Player and situated on the southern border of Kruger National Park, Leopard Creek offers a truly unique safari-golf experience. The course is strategically routed to provide breathtaking views of the Crocodile River and the African bush beyond, with animals often visible from the fairways. Its most famous hole is the par-5 13th, where the green juts into the river, protected by the \"Crocodile Trap\" bunker, offering a direct view into the national park.",
        "The experience is one of immersive wildlife and nature, combined with a challenging and beautifully maintained parkland layout. Sophisticated fencing and landscaping allow wildlife to roam nearby while protecting the course. It hosts the Alfred Dunhill Championship, a flagship event on the European Tour. Golfers remember Leopard Creek not just for the quality of the golf, but for the unforgettable sensation of playing a round accompanied by the sights and sounds of the African wilderness."
    ],
    "Fancourt (The Links)": [
        "Gary Player's 2000 design in George, South Africa, is a monumental and controversial masterpiece—a manufactured links built on reclaimed farmland. With no ocean in sight, it mimics the classic links through vast, rolling fairways, deep pot bunkers, towering dunes covered in fescue, and enormous, double greens. The finish, particularly the par-4 17th (\"The Rumble\") and par-3 18th, is as demanding and dramatic as any in world golf.",
        "The experience is a windswept, walking-only test of power, patience, and creativity. It is a relentless challenge that polarizes opinion but commands respect. It famously hosted the 2003 Presidents Cup, which ended in a dramatic tie. Golfers remember The Links at Fancourt for its sheer audacity and scale, its incredible conditioning, and the surreal achievement of creating a truly authentic linksland experience far from any coast."
    ],
    "Cabot Cliffs": [
        "The 2015 Coore & Crenshaw design in Inverness, Nova Scotia, is a modern marvel of dramatic coastal golf. Perched on towering cliffs high above the Gulf of St. Lawrence, the routing delivers a succession of breathtaking ocean vistas. The back nine is legendary, featuring the cliff-edge par-4 15th, the iconic par-3 16th over a chasm, and the risk-reward par-4 17th that dares players to cut off the corner of the sea.",
        "Playing Cabot Cliffs is an exhilarating walk through some of the most dramatic scenery in golf, where the wind dictates every shot. The firm, fescue-covered ground encourages creative play. Since opening, it has skyrocketed to the top of global course rankings. Golfers remember it for its awe-inspiring beauty, the thrilling, strategic design of its cliffside holes, and its instant-classic status as a must-play pilgrimage site."
    ],
    "St. George's Golf and Country Club": [
        "Stanley Thompson's 1929 design in Toronto is a classic, rolling parkland and the architectural heart of Canadian golf. Built on the sandy, rolling terrain of the Humber River Valley, it features Thompson's signature bold bunkering, strategic use of natural landforms, and brilliantly contoured greens. The par-3 3rd (\"The Vault\") over a deep valley and the par-4 13th are standout examples of his genius for creating dramatic, memorable holes.",
        "The experience is one of traditional, strategic golf on a walkable, beautifully treed property. It has hosted the Canadian Open six times, most recently in 2010, where it was praised for challenging the modern professional game. Golfers remember St. George's for its timeless design, its superb conditioning, and its role as a beloved, classic test that has shaped golf in Canada for nearly a century."
    ],
    "Punta Espada Golf Club": [
        "The first of Jack Nicklaus's three courses at Cap Cana in the Dominican Republic, Punta Espada (2006) is a breathtaking oceanfront spectacle. Eight holes play directly along or over the turquoise waters of the Caribbean Sea, with forced carries from the tee creating thrilling risk-reward decisions. The signature par-3 13th, requiring a full carry over a bay to a cliffside green, is one of the most photographed and exhilarating one-shotters in the world.",
        "The experience is defined by stunning visuals, luxury, and target golf, where precision is rewarded and mistakes are amplified by the sea. The course conditions are immaculate, with paspalum turf thriving in the coastal environment. It has hosted a PGA Tour Champions event for many years. Golfers remember Punta Espada for its jaw-dropping beauty, the sheer number of dramatic ocean carries, and the feeling of playing a high-stakes, resort-style masterpiece."
    ],
    "Corales Golf Club": [
        "Tom Fazio's 2010 design at Puntacana Resort is a dramatic and visually stunning course that culminates in a legendary finishing stretch known as \"The Devil's Elbow.\" The course plays along rugged cliffs, natural coral quarries, and coves of the Caribbean Sea. The final three holes—the perilous par-4 16th along the water, the par-3 17th over the ocean, and the par-4 18th requiring a bold carry over the cliff-edge bay—are as dramatic a finish as exists in golf.",
        "The play experience emphasizes strategy and shot-making, with wide fairways giving way to demanding approach shots. The wind is a constant and shaping force. It now hosts the PGA Tour's Corales Puntacana Championship. Golfers remember Corales for its rugged, natural beauty, its exceptional Fazio design that builds to an unforgettable climax, and its status as a stern championship test in a paradise setting."
    ],
    "Royal Adelaide Golf Club": [
        "Dr. Alister MacKenzie's 1926 design in the sandbelt of Adelaide is a quintessential Australian masterpiece, later refined by C.H. Alison. The course is famed for its strategic brilliance and the iconic \"Crater\" bunker complex on the par-4 3rd hole, where the fairway passes between two massive, cross-bunkers. The routing creatively incorporates the coastal dunes and the historic Glanville railway line, which runs through the property.",
        "Playing Royal Adelaide is a lesson in strategic ground-game golf on fast-running, sandy soil. The bunkering is both artistic and penal, and the greens are subtly contoured. It has hosted the Australian Open numerous times, crowning champions like Gary Player and Jordan Spieth. Golfers remember it for its timeless, cerebral design, its perfect integration with the natural sandbelt landscape, and its welcoming, traditional club atmosphere."
    ],
    "New South Wales Golf Club": [
        "Perched on the rugged, wind-swept headland at La Perouse in Sydney, this Alister MacKenzie design (with later work by Eric Apperly and others) is one of the world's most spectacular clifftop links. The course offers panoramic views of Botany Bay, the Pacific Ocean, and the city skyline. The stretch from the par-4 4th to the par-3 6th plays along the cliff's edge, with the ocean a constant companion and hazard.",
        "The experience is defined by the powerful, often gale-force winds that sweep across the exposed headland, demanding creativity and resilience. The conditions are firm and fast, true to its links character. It consistently ranks among the world's top courses for its unparalleled setting and thrilling test. Golfers remember New South Wales for its raw, breathtaking beauty, the exhilarating challenge of its cliffside holes, and the feeling of playing golf on the very edge of the continent."
    ]
}

# Manual mappings
manual_mappings = {
    "Valderrama Golf Club": "valderrama",
    "Le Golf National (Albatros Course)": "le-golf-national",
    "Morfontaine Golf Club (Vallière Course)": "morfontaine",
    "Oitavos Dunes": "oitavos-dunes",
    "Golf de Chantilly (Vineuil Course)": "chantilly-vineuil",
    "Hirono Golf Club": "hirono",
    "Kasumigaseki Country Club (East Course)": "kasumigaseki-east",
    "Nine Bridges (Jeju Island)": "nine-bridges",
    "Leopard Creek Country Club": "leopard-creek",
    "Fancourt (The Links)": "fancourt-links",
    "Cabot Cliffs": "cabot-cliffs",
    "St. George's Golf and Country Club": "st-georges-toronto",
    "Punta Espada Golf Club": "punta-espada",
    "Corales Golf Club": "corales",
    "Royal Adelaide Golf Club": "royal-adelaide",
    "New South Wales Golf Club": "new-south-wales",
}

# Match and update courses
matched_count = 0
for desc_name, desc_text in additional_descriptions.items():
    if desc_name in manual_mappings:
        course_id = manual_mappings[desc_name]
        for course in courses:
            if course['id'] == course_id:
                course['blurb'] = desc_text
                matched_count += 1
                print(f"✓ Matched: {desc_name} -> {course['name']}")
                break

# Save updated courses.json
with open('courses.json', 'w', encoding='utf-8') as f:
    json.dump(courses, f, indent=2, ensure_ascii=False)

# Also update course_descriptions.json
course_descriptions = {}
for course in courses:
    if course.get('blurb') and isinstance(course['blurb'], list):
        course_descriptions[course['id']] = course['blurb']

with open('course_descriptions.json', 'w', encoding='utf-8') as f:
    json.dump(course_descriptions, f, indent=2, ensure_ascii=False)

print(f"\nMatched {matched_count} descriptions to courses")
print(f"Total courses with descriptions: {len(course_descriptions)}")


