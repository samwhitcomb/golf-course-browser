#!/usr/bin/env python3
"""
Parse final course descriptions from course description.txt (lines 660-760) and add them to courses.json
"""

import json
import re
from pathlib import Path

COURSES_FILE = Path('courses.json')

# Descriptions from lines 660-760
DESCRIPTIONS = {
    'Cape Kidnappers Golf Course': [
        "Perched 140 meters above the Pacific Ocean on a dramatic ridge-and-valley landscape in Hawke's Bay, Cape Kidnappers is a modern marvel designed by Tom Doak and opened in 2004. The course is not a traditional links but delivers a definitive seaside experience, with fairways and greens planted on narrow fingers of land that jut towards the cliff edge. Three times, players must execute shots from the end of one ridge to the next, with the 6th and 15th holes offering the perilous—and unforgettable—possibility of sending an errant approach on a ten-second plummet into the ocean below.",
        "The strategic character is defined by firm, fast conditions, constant wind, and deep, penal bunkers that cling to the edges of greens. A round here is as much about navigating the breathtaking, overwhelming terrain as it is about golf, set within a 6,000-acre private sanctuary for native wildlife. Its global reputation was solidified by hosting the PGA Tour's Kiwi Challenge and consistent rankings among the world's Top 100 courses, making it a bucket-list adventure for any serious golfer."
    ],
    'Tara Iti Golf Club': [
        "Tom Doak's 2015 design, Tara Iti, is a private club set on a reclaimed stretch of coastline an hour and a half north of Auckland. Cleared of non-native pines, the property was a blank canvas transformed into a pure, fescue-covered links that plays 200 meters inland from the Pacific, offering expansive ocean views from every hole. The architecture is strategically brilliant, highlighted by a celebrated trio of driveable par-four holes (the 4th, 7th, and 13th) that invite daring play and varied strategies.",
        "The experience is walking-only, with a caddie, emphasizing a traditional and immersive round. The challenge peaks at the controversial 480-yard 12th hole, featuring a blind tee shot and a fiercely sloping green that draws comparisons to Merion's famous 5th, often playing as one of the toughest pars in golf. Tara Iti debuted to immediate acclaim, landing high on global rankings and establishing itself as the premier private club in the Southern Hemisphere, celebrated for its flawless routing and fun, strategic shot-making."
    ],
    'Barnbougle Dunes Golf Links': [
        "Carved into the wild coastline of northeast Tasmania, Barnbougle Dunes is Australia's premier links experience, a collaborative 2004 design by Tom Doak and Mike Clayton. The course masterfully channels the spirit of Scottish and Irish links, with wide, rumpled fairways of fescue and bent grass meandering through massive, natural sand dunes. Notable features include the fourth hole, which boasts the largest bunker in the Southern Hemisphere, a testament to the scale and drama of the design.",
        "Play demands creativity and strategic thought, with lively greens contoured to the natural land and running at speeds reminiscent of the classic British links. Since opening, it has consistently been ranked among the top public-access courses in the world, praised for delivering thrilling golf in a breathtaking, isolated setting. The combination of pristine, windswept conditions and a design that feels both ancient and exhilarating makes Barnbougle a pilgrimage site for golfers seeking authentic links play."
    ],
    'King Island Golf Clubs (Cape Wickham Links & Ocean Dunes)': [
        "On remote King Island in the Bass Strait, two world-class courses offer some of golf's most dramatic oceanside play. Cape Wickham Links, a Mike DeVries design, features an unparalleled nine holes directly along a rocky coastline, framed by the Southern Hemisphere's tallest lighthouse. Its closing trio—the par-4 16th along the cliffs, the par-3 17th over a beach, and the risk-reward par-4 18th over Victoria Cove—is breathtaking. Nearby, Graeme Grant's Ocean Dines incorporates rolling dunes and heroic carries, with several par-3s played spectacularly over the surging ocean.",
        "The experience is defined by isolation, powerful winds, and raw, untamed beauty. Reaching King Island requires a dedicated flight, but golfers are rewarded with conditions and vistas that are rarely matched. Together, these courses have transformed this island known for cheese and shipwrecks into one of the world's most exotic and rewarding golf destinations, where every round feels like a true expedition."
    ],
    'Praia d\'El Rey Golf & Beach Resort': [
        "Cabell Robinson's 1997 design on Portugal's Silver Coast is a thrilling mix of links and parkland, set between the Atlantic Ocean and a protected pine forest. The front nine plays over rolling dunes with constant ocean views, while the back nine moves into a more wooded landscape. The standout par-3 4th hole requires a dramatic carry over a cliff and beach to a green perched above the surf, encapsulating the course's dramatic seaside character.",
        "The experience is defined by the ever-present wind off the ocean, which greatly influences club selection and strategy. The conditions are firm and fast, enhancing the links-like feel of the opening holes. It is consistently ranked among the top courses in Portugal and Europe for its stunning variety and challenge. Golfers remember Praia d'El Rey for its breathtaking oceanfront holes, the contrast between its two nines, and the sense of a secluded, grand adventure."
    ],
    'Finca Cortesin Golf Club': [
        "This 2006 Cabell Robinson design in Andalusia, Spain, is a modern, expansive championship course built to host top-tier professional events. Characterized by wide, manicured fairways, enormous, undulating greens, and over 100 strategically placed bunkers, it is a bold and demanding test. The par-3 12th hole, with a green guarded by a deep, artistic bunker complex, is a signature of its strategic and visually striking design.",
        "The experience is one of luxury and scale, with the course maintained in flawless condition year-round. Its spacious layout allows for multiple playing angles but requires precise approach shots to navigate its large, complex greens. It has successfully hosted the Volvo World Match Play Championship, proving its merit as a modern stadium course. Golfers remember Finca Cortesin for its impeccable presentation, its challenging yet fair design, and its status as a premier modern golf destination on the Costa del Sol."
    ],
    'Real Club Valderrama': [
        "Robert Trent Jones Sr.'s 1974 masterpiece in Sotogrande, Spain, is the undisputed benchmark for championship golf on continental Europe. Famous for its incredibly tight, cork-oak tree-lined fairways, small, lightning-fast greens, and iconic green-tinted bunkers, Valderrama is a relentless test of precision. The par-5 17th hole, with its creek-guarded layup and perilous two-tiered green, is a legendary risk-reward challenge that decided the historic 1997 Ryder Cup.",
        "Playing Valderrama is an exercise in intense strategic discipline, where position off every tee is paramount. The heavy clay soil is expertly managed to provide firm, fast conditions. As the long-time host of the Volvo Masters and the seminal 1997 Ryder Cup, it cemented a reputation for flawless conditioning and unyielding difficulty. Golfers remember it for its claustrophobic, demanding beauty and the pride of conquering a course that has tested the world's best under the highest pressure."
    ],
    'Naruo Golf Club': [
        "A 1932 C.H. Alison design located near Osaka, Naruo is considered one of Japan's \"Big Three\" classic courses and a masterpiece of strategic design. Built on hilly, wooded terrain, it features dramatic elevation changes, beautifully sculpted bunkers, and subtly contoured greens. The course is renowned for its brilliant routing and the challenging par-4 18th, which plays uphill to a green nestled in front of the classic clubhouse.",
        "The experience is one of traditional, thoughtful golf that emphasizes shot placement and strategy over power. The club maintains an atmosphere of deep reverence for the game and its history. Consistently ranked among the top courses in Japan, it has hosted numerous Japan Opens. Golfers remember Naruo for its timeless Alison architecture, its serene and beautiful setting, and its status as a cornerstone of Japanese golf heritage."
    ],
    'The Club at Nine Bridges': [
        "The original course on Jeju Island, South Korea, this 2001 Ronald Fream design is set on a high plateau with stunning views of Hallasan Mountain and the surrounding landscape. Its character blends traditional strategic elements with dramatic, modern features, including significant water hazards and expertly crafted bunkering. The par-3 9th hole, playing over a deep valley to a green framed by stone walls, is a signature of its scenic drama.",
        "Playing Nine Bridges offers a luxurious and secluded experience, with immaculate conditioning and a peaceful, mountainous setting. The wind is a frequent and significant factor. As the founding course of the exclusive club, it set a high standard for luxury golf in Asia. Golfers remember it for its spectacular, elevated scenery, its challenging and enjoyable design, and its role in establishing Jeju Island as a world-class golf destination."
    ],
    'Mission Hills Golf Club (World Cup Course)': [
        "Jack Nicklaus's 1994 design at the massive Mission Hills complex in Shenzhen, China, was purpose-built to host the World Cup of Golf. It is a classic, demanding Nicklaus layout with tree-lined fairways, strategically placed bunkers, and water hazards that come into play on 11 holes. The course is known for its excellent conditioning and the challenging, scenic par-3 16th hole, which plays over a lake to a well-bunkered green.",
        "The experience is one of championship-scale golf, requiring both length and precision. The course successfully hosted the 1995 World Cup, introducing high-profile international golf to China. It remains a centerpiece of the world's largest golf facility. Golfers remember the World Cup Course for its historic significance in Chinese golf, its classic Nicklaus design principles, and its pristine, parkland beauty."
    ],
    'Siam Country Club (Old Course)': [
        "This 1976 design by Japanese architect Ichizo Ishibashi in Pattaya is a classic, tree-lined parkland and the oldest course in the region. Lush with tropical vegetation, water lilies, and coconut palms, it winds through a gently rolling landscape. The course is famous for its narrow, demanding fairways, small greens, and the distinctive, challenging par-3 17th hole surrounded by water.",
        "The experience offers a classic, strategic test that has stood the test of time in Thailand's golf landscape. The conditions are consistently excellent, with smooth, quick greens. It has hosted the LPGA Tour's Honda event for many years, showcasing its quality to a global audience. Golfers remember the Old Course for its traditional, charming character, its mature, beautiful setting, and its reputation as a stern and fair championship test."
    ],
    'Alpine Golf Club': [
        "A 1996 Schmidt-Curley design located north of Bangkok, Alpine is a modern, championship parkland known for its pristine, lush conditioning and challenging layout. The course features generous, rolling fairways, large, undulating greens, and over 100 strategically placed bunkers. Water comes into play on several holes, most notably on the signature par-3 17th, which demands a precise carry over a lake.",
        "Playing Alpine is a demanding but fair test where approach shots and putting are key to scoring. The club is known for its exceptional maintenance standards and service. It has a history of hosting professional tournaments, including Asian Tour events. Golfers remember Alpine for its immaculate, country-club conditioning, its modern and challenging design, and its status as one of Thailand's premier private golf experiences."
    ],
    'Arabella Golf Club': [
        "Set on the banks of the Bot River lagoon near Hermanus, South Africa, this Peter Matkovich design (1999) is celebrated for its stunning natural beauty. The course seamlessly blends parkland, wetland, and links elements, with several holes playing along the water's edge. The par-5 8th hole, requiring a strategic decision on whether to carry a section of the lagoon, is a signature risk-reward challenge.",
        "The experience is defined by breathtaking vistas of the lagoon and mountains, alongside a thoughtful, strategic design. The wind is a constant and shaping factor. It is consistently ranked among the top courses in South Africa for its spectacular setting and high-quality layout. Golfers remember Arabella for its incredible scenic diversity, its engaging and fun design, and the peaceful, natural environment."
    ],
    'Gary Player Country Club': [
        "The centerpiece of Sun City Resort, this 1979 Gary Player design is a long, demanding championship course set in the Pilanesberg region. Known for its length and difficulty, the course features wide, forgiving fairways that lead to large, well-bunkered greens. The par-5 9th and par-3 16th holes are particularly famous, with water and bunkers creating dramatic challenges.",
        "Playing here is a true test of endurance and skill, with elevation changes and the African sun adding to the challenge. The conditions are always meticulously maintained. It has hosted the prestigious Nedbank Golf Challenge for decades, drawing the world's best players. Golfers remember it for its scale, its championship history, and the unique experience of playing a world-class course in the heart of a South African entertainment resort."
    ],
    'Cabot Links': [
        "Rod Whitman's 2012 design in Inverness, Nova Scotia, is Canada's first authentic links course. Built right along the shoreline of the Gulf of St. Lawrence, the course features firm, fescue-covered fairways, natural dunes, and greens that blend into the landscape. The routing offers constant ocean views, with holes like the par-4 14th and 15th playing directly along the beach.",
        "The experience is a pure, walking-only links adventure, where the wind dictates strategy and creativity is rewarded. The conditions are firm and fast, true to its Scottish and Irish inspirations. As the founding course of the Cabot destination, it sparked a golf renaissance in Cape Breton. Golfers remember Cabot Links for its incredible accessibility to the sea, its fun, strategic design, and the raw, authentic links feel it delivers."
    ],
    'Hamilton Golf and Country Club': [
        "This classic Harry Colt design from 1914 in Ancaster, Ontario, is a strategic, rolling parkland and a perennial Canadian Open venue. The course is characterized by its superb routing over the natural terrain of the Niagara Escarpment, featuring small, well-guarded greens, strategic bunkering, and tree-lined fairways. The par-4 4th and the par-3 6th are standout examples of Colt's genius for creating memorable, strategic holes.",
        "Playing Hamilton is a traditional, thoughtful test that emphasizes position and precision over brute force. The conditions are always championship-caliber. It has hosted the RBC Canadian Open six times, with its classic design receiving praise from modern professionals. Golfers remember it for its timeless Colt architecture, its challenging yet fair layout, and its deep history as a cornerstone of Canadian championship golf."
    ],
    'El Camaleón Golf Club': [
        "Greg Norman's 2006 design at Mayakoba on Mexico's Riviera Maya is a unique and visually striking course. It winds through three distinct ecosystems: tropical jungle, dense mangroves, and stunning oceanfront limestone canals. The opening tee shot from a jungle chute to a fairway bisected by a massive cenote (sinkhole) is one of golf's most dramatic starts.",
        "The experience is one of adventure and variety, where each hole presents a different visual and strategic challenge. The paspalum grass thrives in the coastal environment, providing excellent conditions. As the host of the PGA Tour's Mayakoba Classic (now World Wide Technology Championship), it brings professional golf to Mexico. Golfers remember El Camaleón for its incredible ecological diversity, its fun and engaging design, and the thrill of its unique opening hole."
    ]
}

# Course name to ID mappings
COURSE_MAPPINGS = {
    'Cape Kidnappers Golf Course': 'cape-kidnappers',
    'Tara Iti Golf Club': 'tara-iti',
    'Barnbougle Dunes Golf Links': 'barnbougle-dunes',
    'King Island Golf Clubs (Cape Wickham Links & Ocean Dunes)': 'king-island',
    'Praia d\'El Rey Golf & Beach Resort': 'praia-del-rey',
    'Finca Cortesin Golf Club': 'finca-cortesin',
    'Real Club Valderrama': 'real-club-valderrama',
    'Naruo Golf Club': 'naruo',
    'The Club at Nine Bridges': 'club-nine-bridges',
    'Mission Hills Golf Club (World Cup Course)': 'mission-hills-world-cup',
    'Siam Country Club (Old Course)': 'siam-old',
    'Alpine Golf Club': 'alpine-golf',
    'Arabella Golf Club': 'arabella',
    'Gary Player Country Club': 'gary-player-country-club',
    'Cabot Links': 'cabot-links',
    'Hamilton Golf and Country Club': 'hamilton-gcc',
    'El Camaleón Golf Club': 'el-camaleon',
}

def find_course_id_by_name(courses, course_name):
    """Find course ID by matching name"""
    # Try direct mapping first
    if course_name in COURSE_MAPPINGS:
        course_id = COURSE_MAPPINGS[course_name]
        # Verify it exists
        for course in courses:
            if course['id'] == course_id:
                return course_id
    
    # Try fuzzy matching
    course_name_lower = course_name.lower()
    # Remove common suffixes for matching
    course_name_clean = re.sub(r'\s*\(.*?\)\s*', '', course_name_lower)
    
    for course in courses:
        course_json_name = course['name'].lower()
        course_json_clean = re.sub(r'\s*\(.*?\)\s*', '', course_json_name)
        
        # Check if names match (handle variations)
        if course_name_clean == course_json_clean:
            return course['id']
        if course_name_lower in course_json_name or course_json_name in course_name_lower:
            return course['id']
        
        # Check for partial matches
        name_parts = course_name_clean.split()
        json_parts = course_json_clean.split()
        if len(name_parts) > 0 and name_parts[0] in json_parts:
            return course['id']
    
    return None

def main():
    # Load courses
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    updated = 0
    not_found = []
    
    # Update courses with descriptions
    for course_name, blurb in DESCRIPTIONS.items():
        course_id = find_course_id_by_name(courses, course_name)
        
        if course_id:
            # Find the course and update it
            for course in courses:
                if course['id'] == course_id:
                    course['blurb'] = blurb
                    updated += 1
                    print(f"✓ Updated {course['name']} ({course_id})")
                    break
        else:
            not_found.append(course_name)
            print(f"✗ Could not find course: {course_name}")
    
    # Save updated courses
    with open(COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated} courses")
    print(f"  Not found: {len(not_found)}")
    if not_found:
        print(f"\nCourses not found:")
        for name in not_found:
            print(f"  - {name}")
    
    # Regenerate public/courses.json
    print(f"\nRegenerating public/courses.json...")
    import subprocess
    result = subprocess.run(['python3', 'update_courses_for_static.py'], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

if __name__ == '__main__':
    main()

