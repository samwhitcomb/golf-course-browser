#!/usr/bin/env python3
"""
Parse additional course descriptions from course description.txt (lines 534-658) and add them to courses.json
"""

import json
import re
from pathlib import Path

COURSES_FILE = Path('courses.json')

# Course name to ID mappings for the new descriptions
COURSE_MAPPINGS = {
    'Chambers Bay Golf Course': 'chambers-bay',
    'Whistling Straits (Straits Course)': 'whistling-straits-irish',  # Note: might need to check actual ID
    'Whistling Straits (Irish Course)': 'whistling-straits-irish',
    'Trump National Doral (Blue Monster)': 'trump-doral',
    'Trump National Doral': 'trump-doral',
    'Torrey Pines Golf Course (South)': 'torrey-pines-south',
    'Torrey Pines Golf Course': 'torrey-pines-south',
    'Spyglass Hill Golf Course': 'spyglass-hill',
    'PGA West (Stadium Course)': 'pga-west-stadium',
    'PGA West': 'pga-west-stadium',
    'Indian Wells Golf Resort (Celebrity Course)': 'indian-wells',
    'Indian Wells Golf Resort': 'indian-wells',
    'Desert Highlands Golf Club': 'desert-highlands',
    'Four Seasons Resort Scottsdale (Talon Course)': 'four-seasons-scottsdale',
    'Four Seasons Resort Scottsdale': 'four-seasons-scottsdale',
    'Tidewater Golf Club': 'tidewater',
    'Eagle Point Golf Club': 'eagle-point',
    'Bay Harbor Golf Club (Links/Quarry)': 'bay-harbor',
    'Bay Harbor Golf Club': 'bay-harbor',
    'Blackwolf Run (River Course)': 'kohler-blackwolf',
    'Blackwolf Run': 'kohler-blackwolf',
    'Pete Dye Golf Club': 'pete-dye-gc',
    'The Greenbrier (The Old White TPC)': 'greenbrier',
    'The Greenbrier': 'greenbrier',
    'The Homestead (Cascades Course)': 'homestead-cascades',
    'The Homestead': 'homestead-cascades',
    'Kingsmill Resort (River Course)': 'kingsmill',
    'Kingsmill Resort': 'kingsmill',
    'Golden Horseshoe Golf Club (Gold Course)': 'golden-horseshoe',
    'Golden Horseshoe Golf Club': 'golden-horseshoe',
    'Kiawah Island Golf Resort (River Course)': 'kiawah-river',
    'Kiawah Island Golf Resort': 'kiawah-river',
    'Wild Dunes Resort (Links Course)': 'wild-dunes',
    'Wild Dunes Resort': 'wild-dunes',
    'Kauri Cliffs Golf Course': 'kauri-cliffs',
}

# Descriptions from lines 534-658
DESCRIPTIONS = {
    'Chambers Bay Golf Course': [
        "Built on the site of a former sand and gravel quarry on the shores of Puget Sound, Robert Trent Jones Jr.'s 2007 design is a massive, walking-only links that hosted the 2015 U.S. Open. Its character is defined by vast, fescue-covered dunes, dramatic elevation changes of over 250 feet, and panoramic views of the water and mountains. The par-4 18th, playing downhill to a stadium green, provided a dramatic and controversial Open finish.",
        "The experience is one of a true, firm-and-fast British-style links, where the ground game is essential and the wind is a constant factor. The fine fescue turf and lack of trees create a stark, minimalist beauty. Its U.S. Open debut, famous for its brown visuals and tricky greens, cemented its place as a unique and demanding public championship test. Golfers remember it for its rugged, industrial-scale beauty and the physically demanding walk across its dramatic terrain."
    ],
    'Whistling Straits (Straits Course)': [
        "Pete Dye's 1998 creation on the bluffs of Lake Michigan in Kohler, Wisconsin, is a manufactured masterpiece designed to mimic the rugged links of Ireland. With over 1,000 bunkers (many just for show), fescue-covered dunes, and constant vistas of the vast lake, the course is defined by its visual intimidation. The closing stretch along the water, particularly the par-3 17th and the demanding par-4 18th, provides a dramatic finish worthy of its major championship status.",
        "The experience is walking-only with a caddie, enhancing the links-like feel. The challenge is severe, with windy conditions, uneven lies, and penal rough. It has hosted three PGA Championships and the 2021 Ryder Cup, where its stadium-style layout created thrilling spectator moments. Golfers remember it for its breathtaking scale and scenery, the sheer difficulty of its setup, and the surreal achievement of bringing coastal drama to the American Midwest."
    ],
    'Trump National Doral (Blue Monster)': [
        "The legendary Blue Monster at Doral, originally a Dick Wilson design (1962) and famously redesigned by Gil Hanse in 2014, is a Florida icon defined by water. Its character is summed up by the terrifying par-4 18th, where a long carry over a lake is required to reach a fairway that then bends left around the same lake to a narrow green. Water is in play on nearly every hole, creating relentless pressure.",
        "Playing the Blue Monster is a nerve-wracking exercise in target golf where risk must be carefully measured. The conditions are lush and tropical, with towering palms lining the fairways. It hosted a PGA Tour event for over 50 years, creating a rich history of dramatic finishes on the 18th. Golfers remember it for its intimidating, water-laden design, the specific, daunting challenge of the 18th hole, and its legacy as a classic Florida resort test."
    ],
    'Torrey Pines Golf Course (South)': [
        "This William F. Bell design (1957) on the clifftops above the Pacific Ocean in La Jolla is a beloved public municipal course and U.S. Open venue. Its character is defined by narrow, tree-lined fairways, thick kikuyu grass rough, and small greens perched above canyons and ocean vistas. The par-4 12th along the cliffs and the dramatic par-5 18th, where Tiger Woods forced his famous playoff in 2008, are its most famous tests.",
        "The experience offers the public golfer a taste of major-championship conditions, though the weekend setups are more forgiving. The ocean views are spectacular, and the sea breeze is a constant factor. Hosting the annual Farmers Insurance Open and the 2008 & 2021 U.S. Opens has cemented its place in golf lore. Golfers remember Torrey South for its incredible public-access value, its stunning coastal setting, and walking the same fairways as legends during dramatic major moments."
    ],
    'Spyglass Hill Golf Course': [
        "Robert Trent Jones Sr.'s 1966 design on the Monterey Peninsula begins with a breathtaking, unforgettable opening five holes that plunge through dunes and forests to the Pacific Ocean. The character then shifts inland to a demanding, tree-lined test through Del Monte forest. The first five holes, named after treasures from \"Treasure Island,\" are among the most beautiful and difficult opening stretches in golf.",
        "The experience is a tale of two nines: a dramatic, links-like start followed by a tough, strategic parkland challenge. It is consistently rated as one of the most difficult public courses in America, with sloping fairways and slick greens. As a regular host of the AT&T Pebble Beach Pro-Am, it is often the scoring differentiator. Golfers remember Spyglass for the sheer thrill of its opening ocean holes and the pride of conquering its relentless, full-length test."
    ],
    'PGA West (Stadium Course)': [
        "Pete Dye's 1986 design in La Quinta, California, was built as the ultimate \"Stadium Course\" for spectator viewing and professional torture. Its character is defined by extreme features: the island green on the par-3 17th (\"Alcatraz\"), massive waste bunkers, and the infamous, 20-foot-deep bunker on the par-5 16th. The course is a bold, in-your-face collection of dramatic, risk-reward challenges.",
        "Playing the Stadium Course is an adventurous and sometimes frustrating experience where big numbers lurk everywhere. The desert setting and wind add to the difficulty. It famously debuted at the 1987 Bob Hope Classic, where it was deemed too tough by pros, but has since become a celebrated and fun challenge. Golfers remember it for its collection of iconic, extreme holes and the bragging rights that come from surviving Dye's desert gauntlet."
    ],
    'Indian Wells Golf Resort (Celebrity Course)': [
        "A Clive Clark design (2006) in the Coachella Valley, the Celebrity Course is a lush, target-style desert resort layout known for its stunning mountain vistas and dramatic water features. Its character is defined by immaculate conditioning, dramatic rockwork, and several memorable holes where water and strategy intersect, such as the par-3 14th with its peninsula green and the risk-reward par-5 15th.",
        "The experience is one of resort luxury and scenic beauty, with a challenging but playable design for all skill levels. The course is a favorite for its pristine presentation and the stark contrast of emerald fairways against the desert and mountain backdrop. It regularly hosts high-level amateur events. Golfers remember Indian Wells for its breathtaking mountain scenery, its fun and engaging design, and its reputation as one of the prettiest and best-maintained public resort courses in the desert."
    ],
    'Desert Highlands Golf Club': [
        "Jack Nicklaus's 1983 design in Scottsdale was a groundbreaking course that helped define luxury desert golf. Routed through massive granite boulders and natural arroyos, it introduced signature Nicklaus strategic concepts to the Sonoran Desert, including the iconic \"Devil's Asshole\" bunker complex on the par-5 8th hole. The course blends dramatic, target-style carries with strategic options.",
        "Playing Desert Highlands is a scenic and thoughtful test where positioning is key to accessing its large, undulating greens. The conditions are always impeccable, and the views of Pinnacle Peak are spectacular. It hosted the inaugural Skins Game in 1983, bringing match-play drama to a national TV audience. Golfers remember it for its historical significance in desert architecture, its dramatic natural setting, and its classic Nicklaus design intelligence."
    ],
    'Four Seasons Resort Scottsdale (Talon Course)': [
        "The Talon Course at Troon North, a Dana Garmany & Tom Weiskopf design (1996), is a quintessential Scottsdale desert experience. It winds through dramatic foothills and valleys, with holes framed by giant saguaro cacti and rugged rock outcroppings. Its character is defined by its natural integration with the desert, offering generous landing areas that lead to challenging, well-bunkered green complexes.",
        "The experience offers a enjoyable yet challenging round for players of various skill levels, with multiple tee boxes. The conditions are consistently excellent, and the service is top-tier, matching the luxury resort setting. The panoramic views of the McDowell Mountains are a constant backdrop. Golfers remember the Talon Course for its beautiful desert aesthetics, its fun and playable design, and the reliable, high-quality resort golf experience it provides."
    ],
    'Tidewater Golf Club': [
        "Situated on a scenic peninsula in North Myrtle Beach, Ken Tomlinson's 1990 design is often called the \"Pebble Beach of the East\" for its stunning use of coastal landscapes. Nine holes play along either the Intracoastal Waterway or the salt marshes of Cherry Grove, offering breathtaking water views. The par-3 3rd over marshland and the par-4 9th along the waterway are particularly memorable.",
        "The play experience emphasizes precision and smart course management, as the wind off the water is a constant factor. The conditions are typically superb, with lush Bermuda grass throughout. It is consistently ranked as one of the top public courses in the Myrtle Beach area for its beauty and challenge. Golfers remember Tidewater for its exceptional scenic variety, its demanding yet fair layout, and the peaceful, natural setting that feels removed from the busy Grand Strand."
    ],
    'Eagle Point Golf Club': [
        "This 2000 Tom Fazio design in Wilmington, North Carolina, is a lowcountry masterpiece built on a secluded peninsula surrounded by tidal creeks and marshes. The course is characterized by its elegant, strategic routing through pine forests and open meadows, with water in play on half the holes. The par-3 17th, with its green perched above the marsh, and the closing par-5 18th around a lake are standout finishes.",
        "The experience is one of exclusive, tranquil beauty and impeccable conditioning on a walking-friendly layout. It is a private club that has hosted the PGA Tour's Wells Fargo Championship, showcasing its championship quality to a wide audience. Golfers remember Eagle Point for its serene, natural setting, its flawless Fazio design that offers both beauty and brains, and its ability to stand out as a world-class course in a region filled with great golf."
    ],
    'Bay Harbor Golf Club (Links/Quarry)': [
        "Arthur Hills' 1997 design on the shores of Lake Michigan is actually three distinct 9-hole courses; the most famous combination is the Links/Quarry nines. The Links nine plays along 150-foot bluffs with stunning lake views, while the Quarry nine plunges into a dramatic, abandoned shale quarry with cliffs and water. The transition between these wildly different landscapes is breathtaking.",
        "The experience is one of spectacular visual drama and variety, unlike any other course in the Midwest. The conditions are resort-level pristine, and the wind off the lake significantly impacts play. It is a premier destination course that has hosted senior professional events. Golfers remember Bay Harbor for the thrilling contrast between its two nines—the majestic lakeside vistas and the surreal, immersive quarry landscape—creating a round of unforgettable contrasts."
    ],
    'Blackwolf Run (River Course)': [
        "Pete Dye's 1988 design along the banks of the Sheboygan River in Kohler, Wisconsin, is a dramatic, naturalistic test. The course is famous for its back-to-back par-4s at the 14th and 15th holes, known as \"The Dueling Dogs,\" which require carries over a deep river chasm. The routing constantly brings the river and its steep, wooded banks into play, creating both beauty and peril.",
        "Playing Blackwolf Run is a strategic and often perilous journey where accuracy is paramount. The natural, rugged beauty of the river valley is integral to the experience. It has hosted multiple USGA championships, including the U.S. Women's Open. Golfers remember it for its intimate yet demanding interaction with the river, the specific, dramatic challenge of the Dueling Dogs, and its status as a classic, natural Pete Dye design."
    ],
    'Pete Dye Golf Club': [
        "Located in the hills of West Virginia, this 1994 Pete Dye design is one of his most secluded and naturally integrated masterpieces. Built on former mining land, the course follows the contours of dramatic hills and valleys, with few parallel fairways. Its character is defined by rugged, natural beauty, strategic bunkering, and Dye's signature use of railroad ties and small, undulating greens.",
        "The experience is a pure, walking-only golf adventure in a remote, peaceful setting. The elevation changes are significant, and the conditions are firm and fast. It is a private club that has garnered a cult reputation among architecture enthusiasts for its purity and challenge. Golfers remember it for its stunning, untouched mountain scenery, its quintessential and thoughtful Dye design, and the total escape from the outside world it provides."
    ],
    'The Greenbrier (The Old White TPC)': [
        "The historic Old White course, dating to 1914 with a C.B. Macdonald design influence and restored by Lester George, is a classic parkland with a storied past. It features template holes like the \"Redan\" par-3 8th and the \"Road Hole\" par-4 13th, paying homage to the British links. The course is tree-lined and demands strategic positioning on its rolling fairways.",
        "Playing the Old White is a walk through golf history at America's classic resort. The conditions are impeccably manicured. It served as a longtime PGA Tour venue (the Greenbrier Classic) and has hosted a Presidents Cup. Golfers remember it for its deep sense of tradition, its charming, classical design that emphasizes fun and strategy over length, and the timeless elegance of the entire Greenbrier experience."
    ],
    'The Homestead (Cascades Course)': [
        "William S. Flynn's 1923 design in the Allegheny Mountains of Virginia is a classic, timeless mountain course. Its character is defined by dramatic elevation changes, crystal-clear mountain streams that cross fairways, and small, well-guarded greens. The par-3 4th, dropping 150 feet to a green by a creek, and the long, uphill par-4 18th are iconic tests.",
        "The experience is one of traditional, walking-friendly golf in a serene mountain setting. The course has hosted multiple USGA championships and is known for its excellent, classic conditioning. It is the centerpiece of America's oldest resort, The Homestead. Golfers remember the Cascades Course for its beautiful, natural routing through the hills, its historic Flynn design, and the cool, refreshing mountain air that defines a round there."
    ],
    'Kingsmill Resort (River Course)': [
        "Pete Dye's 1975 design on the banks of the James River in Williamsburg is a strategic, risk-reward test. Its most famous stretch is the three-hole finish along the river: the demanding par-4 16th, the long par-3 17th over water, and the scenic par-4 18th alongside the historic waterway. Mature trees and elevation changes add to the challenge away from the river.",
        "The experience combines resort playability with moments of significant challenge, particularly on the closing holes. The conditions are consistently very good. It hosted a PGA Tour event for over 20 years and now hosts an LPGA Tour event. Golfers remember the River Course for its scenic riverside setting, its classic Pete Dye strategic elements, and the enjoyable, well-rounded resort test it provides."
    ],
    'Golden Horseshoe Golf Club (Gold Course)': [
        "Robert Trent Jones Sr.'s 1963 design in Colonial Williamsburg is a classic, tree-lined championship parkland. The course is known for its exceptional conditioning, strategic bunkering, and the famous par-3 16th hole, where the tee shot carries over a deep, wooded ravine to a well-bunkered green—a dramatic and beautiful one-shotter.",
        "Playing the Gold Course is a traditional, strategic experience that demands well-placed tee shots and precise approaches. The setting amidst Virginia woods feels secluded and historic. It has hosted multiple USGA national championships. Golfers remember it for its timeless Trent Jones design, its immaculate presentation, and the specific, thrilling challenge of the signature 16th hole."
    ],
    'Kiawah Island Golf Resort (River Course)': [
        "Tom Fazio's 1995 design takes a different approach from the Ocean Course, weaving through maritime forests, salt marshes, and along the Kiawah River. Its character is defined by beautiful Lowcountry scenery, with large, stately oaks and palms lining the fairways. Water comes into play on 15 holes, but the course offers width and strategic options rather than sheer punishment.",
        "The experience is one of scenic, resort-friendly golf that is challenging but less windswept and intimidating than its famous sibling. The conditions are always pristine. It offers a more relaxed but still engaging strategic test. Golfers remember the River Course for its stunning natural beauty, its excellent Fazio design that is both fun and thoughtful, and its role as a perfect complement to the brutal Ocean Course."
    ],
    'Wild Dunes Resort (Links Course)': [
        "Tom Fazio's first solo design (1980) on the Isle of Palms near Charleston is a classic Lowcountry links. The front nine plays through marsh and forest, while the back nine delivers a stunning finish along the Atlantic Ocean beach. The final two holes—the par-3 17th along the surf and the par-4 18th with the beach and dunes in play—form one of the most dramatic finishes in American resort golf.",
        "The experience is defined by its fantastic seaside setting, with the sound of crashing waves on the closing holes. The wind is a major factor, creating a true links challenge. While hurricanes have altered the exact routing, the oceanfront drama remains intact. Golfers remember Wild Dunes for its breathtaking beachfront finish, its fun and playable design, and the pure vacation joy of playing golf so close to the sea."
    ],
    'Kauri Cliffs Golf Course': [
        "David Harman's 2000 design on the North Island of New Zealand is a breathtaking clifftop course with 15 holes offering panoramic views of the Pacific Ocean. The property features lush, rolling farmland, native forest, and dramatic cliffs plunging to secluded bays. The par-4 6th, playing along a cliff edge to a green above Pink Beach, is its most photographed masterpiece.",
        "The experience is one of awe-inspiring beauty and isolation, where the quality of the golf matches the scenery. The conditions are immaculate, and the wind can be fierce. It is consistently ranked among the world's top courses and is a cornerstone of New Zealand's luxury golf tourism. Golfers remember Kauri Cliffs for its overwhelming natural beauty, the thrilling sensation of playing on the edge of the world, and its flawless integration of sport and spectacle."
    ]
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
    for course in courses:
        course_json_name = course['name'].lower()
        # Check if names match (handle variations)
        if course_name_lower in course_json_name or course_json_name in course_name_lower:
            return course['id']
        
        # Check for partial matches
        name_parts = course_name_lower.split()
        json_parts = course_json_name.split()
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

