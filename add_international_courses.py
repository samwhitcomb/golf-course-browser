import json
from pathlib import Path

# Load existing courses
courses_file = Path(__file__).parent / 'courses.json'
with open(courses_file, 'r', encoding='utf-8') as f:
    courses = json.load(f)

# Get existing IDs to avoid duplicates
existing_ids = {course['id'] for course in courses}

# New international courses to add
new_courses = [
    {
        "id": "valderrama",
        "name": "Valderrama Golf Club",
        "description": "Exclusive championship course that hosted the 1997 Ryder Cup",
        "location": "Sotogrande, Spain",
        "rating": 4.7,
        "category": "recommended",
        "batch": "Modern American Icons & Stadium Courses",
        "type": "championship",
        "architect": "Robert Trent Jones Sr.",
        "established": 1974,
        "yardage": 7000,
        "continent": "Europe"
    },
    {
        "id": "le-golf-national",
        "name": "Le Golf National (Albatros Course)",
        "description": "Stadium-style championship course that hosted the 2018 Ryder Cup",
        "location": "Paris, France",
        "rating": 4.5,
        "category": "recommended",
        "batch": "Modern American Icons & Stadium Courses",
        "type": "championship",
        "architect": "Hubert Chesneau",
        "established": 1990,
        "yardage": 7200,
        "continent": "Europe"
    },
    {
        "id": "morfontaine",
        "name": "Morfontaine Golf Club",
        "description": "Classic heathland course by Tom Simpson, one of France's finest",
        "location": "Mortefontaine, France",
        "rating": 4.6,
        "category": "recommended",
        "batch": "Strategic & Artistic Gems",
        "type": "parkland",
        "architect": "Tom Simpson",
        "established": 1927,
        "yardage": 6800,
        "continent": "Europe"
    },
    {
        "id": "oitavos-dunes",
        "name": "Oitavos Dunes",
        "description": "Links-style course on Portugal's Atlantic coast",
        "location": "Cascais, Portugal",
        "rating": 4.4,
        "category": "recommended",
        "batch": "Premier Global Links & Sandbelt",
        "type": "links",
        "architect": "Arthur Hills",
        "established": 2001,
        "yardage": 7100,
        "continent": "Europe"
    },
    {
        "id": "praia-del-rey",
        "name": "Praia d'El Rey Golf & Beach Resort",
        "description": "Scenic oceanfront course with dramatic Atlantic views",
        "location": "Óbidos, Portugal",
        "rating": 4.3,
        "category": "recommended",
        "batch": "Destination & Scenic Resort Courses",
        "type": "coastal",
        "architect": "Cabell Robinson",
        "established": 1997,
        "yardage": 7000,
        "continent": "Europe"
    },
    {
        "id": "chantilly-vineuil",
        "name": "Golf de Chantilly (Vineuil Course)",
        "description": "Classic Tom Simpson design that has hosted the French Open",
        "location": "Chantilly, France",
        "rating": 4.5,
        "category": "recommended",
        "batch": "Classic American Golden Age Designs",
        "type": "parkland",
        "architect": "Tom Simpson",
        "established": 1909,
        "yardage": 6900,
        "continent": "Europe"
    },
    {
        "id": "finca-cortesin",
        "name": "Finca Cortesin Golf Club",
        "description": "Modern championship course in Andalusia, Spain",
        "location": "Casares, Spain",
        "rating": 4.6,
        "category": "recommended",
        "batch": "Modern American Icons & Stadium Courses",
        "type": "championship",
        "architect": "Cabell Robinson",
        "established": 2006,
        "yardage": 7100,
        "continent": "Europe"
    },
    {
        "id": "real-club-valderrama",
        "name": "Real Club Valderrama",
        "description": "Prestigious Spanish course, host of multiple European Tour events",
        "location": "Sotogrande, Spain",
        "rating": 4.7,
        "category": "recommended",
        "batch": "Modern American Icons & Stadium Courses",
        "type": "championship",
        "architect": "Robert Trent Jones Sr.",
        "established": 1974,
        "yardage": 6950,
        "continent": "Europe"
    },
    {
        "id": "hirono",
        "name": "Hirono Golf Club",
        "description": "Classic C.H. Alison design, one of Japan's most revered courses",
        "location": "Kobe, Japan",
        "rating": 4.8,
        "category": "recommended",
        "batch": "Classic American Golden Age Designs",
        "type": "parkland",
        "architect": "C.H. Alison",
        "established": 1932,
        "yardage": 7050,
        "continent": "Asia"
    },
    {
        "id": "kasumigaseki-east",
        "name": "Kasumigaseki Country Club (East Course)",
        "description": "Historic Japanese course that hosted the 2020 Olympics",
        "location": "Saitama, Japan",
        "rating": 4.6,
        "category": "recommended",
        "batch": "Historic & Championship International Links",
        "type": "championship",
        "architect": "Kinya Fujita",
        "established": 1929,
        "yardage": 7150,
        "continent": "Asia"
    },
    {
        "id": "naruo",
        "name": "Naruo Golf Club",
        "description": "Traditional Japanese course by C.H. Alison",
        "location": "Osaka, Japan",
        "rating": 4.5,
        "category": "recommended",
        "batch": "Classic American Golden Age Designs",
        "type": "parkland",
        "architect": "C.H. Alison",
        "established": 1930,
        "yardage": 6900,
        "continent": "Asia"
    },
    {
        "id": "nine-bridges",
        "name": "Nine Bridges",
        "description": "Modern championship course on Jeju Island, host of CJ Cup",
        "location": "Jeju Island, South Korea",
        "rating": 4.7,
        "category": "recommended",
        "batch": "Modern American Icons & Stadium Courses",
        "type": "championship",
        "architect": "Ronald Fream",
        "established": 2001,
        "yardage": 7200,
        "continent": "Asia"
    },
    {
        "id": "club-nine-bridges",
        "name": "The Club at Nine Bridges",
        "description": "Scenic mountain course on Jeju Island",
        "location": "Jeju Island, South Korea",
        "rating": 4.5,
        "category": "recommended",
        "batch": "Destination & Scenic Resort Courses",
        "type": "mountain",
        "architect": "Ronald Fream",
        "established": 2001,
        "yardage": 7100,
        "continent": "Asia"
    },
    {
        "id": "mission-hills-world-cup",
        "name": "Mission Hills Golf Club (World Cup Course)",
        "description": "Jack Nicklaus design that hosted the World Cup",
        "location": "Shenzhen, China",
        "rating": 4.4,
        "category": "recommended",
        "batch": "Modern American Icons & Stadium Courses",
        "type": "championship",
        "architect": "Jack Nicklaus",
        "established": 1994,
        "yardage": 7300,
        "continent": "Asia"
    },
    {
        "id": "siam-old",
        "name": "Siam Country Club (Old Course)",
        "description": "Classic Thai course that has hosted LPGA events",
        "location": "Pattaya, Thailand",
        "rating": 4.3,
        "category": "recommended",
        "batch": "Destination & Scenic Resort Courses",
        "type": "parkland",
        "architect": "Ichizo Kato",
        "established": 1971,
        "yardage": 7000,
        "continent": "Asia"
    },
    {
        "id": "alpine-golf",
        "name": "Alpine Golf Club",
        "description": "Championship course in Thailand with strategic design",
        "location": "Pathum Thani, Thailand",
        "rating": 4.4,
        "category": "recommended",
        "batch": "Modern American Icons & Stadium Courses",
        "type": "championship",
        "architect": "Schmidt-Curley Design",
        "established": 1996,
        "yardage": 7100,
        "continent": "Asia"
    },
    {
        "id": "leopard-creek",
        "name": "Leopard Creek Country Club",
        "description": "Gary Player design bordering Kruger National Park",
        "location": "Mpumalanga, South Africa",
        "rating": 4.6,
        "category": "recommended",
        "batch": "Destination & Scenic Resort Courses",
        "type": "parkland",
        "architect": "Gary Player",
        "established": 1996,
        "yardage": 7000,
        "continent": "Africa"
    },
    {
        "id": "fancourt-links",
        "name": "Fancourt (Links Course)",
        "description": "Gary Player design that hosted the Presidents Cup",
        "location": "George, South Africa",
        "rating": 4.7,
        "category": "recommended",
        "batch": "Premier Global Links & Sandbelt",
        "type": "links",
        "architect": "Gary Player",
        "established": 2000,
        "yardage": 7200,
        "continent": "Africa"
    },
    {
        "id": "arabella",
        "name": "Arabella Golf Club",
        "description": "Scenic coastal course with mountain views",
        "location": "Kleinmond, South Africa",
        "rating": 4.4,
        "category": "recommended",
        "batch": "Destination & Scenic Resort Courses",
        "type": "coastal",
        "architect": "Peter Matkovich",
        "established": 1999,
        "yardage": 6900,
        "continent": "Africa"
    },
    {
        "id": "gary-player-country-club",
        "name": "Gary Player Country Club",
        "description": "Championship course that hosts the Nedbank Golf Challenge",
        "location": "Sun City, South Africa",
        "rating": 4.5,
        "category": "recommended",
        "batch": "Modern American Icons & Stadium Courses",
        "type": "championship",
        "architect": "Gary Player",
        "established": 1979,
        "yardage": 7100,
        "continent": "Africa"
    },
    {
        "id": "cabot-cliffs",
        "name": "Cabot Cliffs",
        "description": "Coore & Crenshaw design with dramatic coastal views",
        "location": "Inverness, Nova Scotia, Canada",
        "rating": 4.8,
        "category": "recommended",
        "batch": "Premier Global Links & Sandbelt",
        "type": "coastal",
        "architect": "Bill Coore",
        "established": 2015,
        "yardage": 7100,
        "continent": "North America"
    },
    {
        "id": "cabot-links",
        "name": "Cabot Links",
        "description": "Authentic links experience on Canada's Atlantic coast",
        "location": "Inverness, Nova Scotia, Canada",
        "rating": 4.7,
        "category": "recommended",
        "batch": "Premier Global Links & Sandbelt",
        "type": "links",
        "architect": "Rod Whitman",
        "established": 2011,
        "yardage": 7000,
        "continent": "North America"
    },
    {
        "id": "st-georges-toronto",
        "name": "St. George's Golf and Country Club",
        "description": "Classic Stanley Thompson design, host of Canadian Open",
        "location": "Toronto, Canada",
        "rating": 4.6,
        "category": "recommended",
        "batch": "Classic American Golden Age Designs",
        "type": "parkland",
        "architect": "Stanley Thompson",
        "established": 1929,
        "yardage": 6950,
        "continent": "North America"
    },
    {
        "id": "hamilton-gcc",
        "name": "Hamilton Golf and Country Club",
        "description": "Harry Colt design that has hosted the Canadian Open",
        "location": "Ancaster, Canada",
        "rating": 4.5,
        "category": "recommended",
        "batch": "Classic American Golden Age Designs",
        "type": "parkland",
        "architect": "Harry Colt",
        "established": 1914,
        "yardage": 7000,
        "continent": "North America"
    },
    {
        "id": "el-camaleon",
        "name": "El Camaleón Golf Club",
        "description": "Greg Norman design that hosts the Mayakoba Classic",
        "location": "Playa del Carmen, Mexico",
        "rating": 4.4,
        "category": "recommended",
        "batch": "Modern American Icons & Stadium Courses",
        "type": "championship",
        "architect": "Greg Norman",
        "established": 2006,
        "yardage": 7000,
        "continent": "North America"
    },
    {
        "id": "punta-espada",
        "name": "Punta Espada Golf Club",
        "description": "Jack Nicklaus design with dramatic oceanfront holes",
        "location": "Cap Cana, Dominican Republic",
        "rating": 4.6,
        "category": "recommended",
        "batch": "Destination & Scenic Resort Courses",
        "type": "coastal",
        "architect": "Jack Nicklaus",
        "established": 2006,
        "yardage": 7100,
        "continent": "North America"
    },
    {
        "id": "corales",
        "name": "Corales Golf Club",
        "description": "Tom Fazio design with stunning Caribbean views",
        "location": "Punta Cana, Dominican Republic",
        "rating": 4.5,
        "category": "recommended",
        "batch": "Destination & Scenic Resort Courses",
        "type": "coastal",
        "architect": "Tom Fazio",
        "established": 2010,
        "yardage": 7050,
        "continent": "North America"
    },
    {
        "id": "royal-adelaide",
        "name": "Royal Adelaide Golf Club",
        "description": "Alister MacKenzie design, classic Australian sandbelt course",
        "location": "Adelaide, Australia",
        "rating": 4.7,
        "category": "recommended",
        "batch": "Premier Global Links & Sandbelt",
        "type": "sandbelt",
        "architect": "Alister MacKenzie",
        "established": 1892,
        "yardage": 6900,
        "continent": "Oceania"
    },
    {
        "id": "new-south-wales",
        "name": "New South Wales Golf Club",
        "description": "Alister MacKenzie design with dramatic clifftop setting",
        "location": "La Perouse, Australia",
        "rating": 4.8,
        "category": "recommended",
        "batch": "Premier Global Links & Sandbelt",
        "type": "coastal",
        "architect": "Alister MacKenzie",
        "established": 1926,
        "yardage": 7100,
        "continent": "Oceania"
    },
    {
        "id": "cape-kidnappers-nz",
        "name": "Cape Kidnappers",
        "description": "Tom Doak design with dramatic clifftop holes",
        "location": "Hawke's Bay, New Zealand",
        "rating": 4.7,
        "category": "recommended",
        "batch": "Destination & Scenic Resort Courses",
        "type": "coastal",
        "architect": "Tom Doak",
        "established": 2004,
        "yardage": 7000,
        "continent": "Oceania"
    }
]

# Add new courses that don't already exist
added_count = 0
for new_course in new_courses:
    if new_course['id'] not in existing_ids:
        courses.append(new_course)
        existing_ids.add(new_course['id'])
        added_count += 1
    else:
        print(f"Skipping {new_course['name']} - already exists")

# Save updated courses
with open(courses_file, 'w', encoding='utf-8') as f:
    json.dump(courses, f, indent=2, ensure_ascii=False)

print(f"\nAdded {added_count} new international courses")
print(f"Total courses: {len(courses)}")

# Print summary by continent
from collections import Counter
continent_counts = Counter(c.get('continent') for c in courses)
print(f"\nContinent distribution:")
for continent, count in sorted(continent_counts.items()):
    print(f"  {continent}: {count} courses")


