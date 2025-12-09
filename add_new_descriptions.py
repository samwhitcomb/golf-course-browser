#!/usr/bin/env python3
"""
Parse course descriptions from lines 491-534 of course description.txt and add them to courses.json
"""

import json
from pathlib import Path

COURSES_FILE = Path('courses.json')

# Course name to ID mappings
COURSE_MAPPINGS = {
    'Bethpage State Park (Black Course)': 'bethpage-black',
    'Maidstone Club': 'maidstone-club',
    'Baltusrol Golf Club (Lower Course)': 'baltusrol-lower',
    'Ridgewood Country Club (East/West Combo)': 'ridgewood',
    'Los Angeles Country Club (North Course)': 'los-angeles-north',
    'Garden City Golf Club': 'garden-city',
    'Congressional Country Club (Blue Course)': 'congressional',
    'Riviera Country Club': 'riviera',
    'Seminole Golf Club': 'seminole',
    'Bay Hill Club & Lodge': 'bay-hill',
    'Hazeltine National Golf Club': 'hazeltine',
    'San Francisco Golf Club': 'san-francisco-golf',
    'Olympic Club (Lake Course)': 'olympic-lake',
    'Quaker Ridge Golf Club': 'quaker-ridge',
}

# Descriptions from the file (lines 491-534)
DESCRIPTIONS = {
    'Bethpage State Park (Black Course)': [
        "A.W. Tillinghast's 1936 public-access monster on Long Island is famously preceded by a \"Warning\" sign about its extreme difficulty. Its character is defined by vast, rolling fairways, thick, punishing rough, and deep, strategic bunkers. The opening stretch, particularly the long par-4 4th and the par-3 3rd with its elevated green, sets a grueling tone that never relents across the 7,400-yard layout, all on a walk-only, hilly property.",
        "The experience is a physical and mental marathon, where par is a tremendous score. Its conditioning is maintained to a high standard, befitting its major championship status. As the first truly public course to host the U.S. Open (2002, won by Tiger Woods), it broke barriers in golf. Golfers remember it for the democratic thrill of conquering the same brutal test as the pros, the iconic warning sign, and the pride of surviving one of golf's great public challenges."
    ],
    'Maidstone Club': [
        "This timeless 1891 links-style course in the Hamptons, with later refinements by Willie Park Jr. and others, occupies a stunning, rolling parcel between the Atlantic Ocean and freshwater lakes. Its character is defined by fast, firm fairways, natural fescue rough, and small, well-guarded greens. The unique back-to-back par-3s at the 4th and 5th holes, and the approach over a pond to the par-4 18th green, are memorable highlights of its classic, windswept routing.",
        "Playing Maidstone is a pure, traditional experience focused on ground-game strategy and controlling the ball in the sea breeze. The conditions are kept intentionally rustic and natural. Its exclusivity and classic design have made it a revered retreat for over a century. Golfers remember it for its understated, old-world charm, its breathtaking natural setting amidst dunes and lakes, and the serene, walkable test it provides."
    ],
    'Baltusrol Golf Club (Lower Course)': [
        "A.W. Tillinghast's 1922 redesign of this New Jersey landmark created a monumental, tree-lined championship parkland. The Lower Course is famed for its back-to-back par-5 finishing holes (the 17th and 18th), both demanding long, precise shots to well-bunkered greens. The course builds in drama, with the difficult par-3 4th over water and the long, demanding par-4 16th serving as pivotal tests before the famous finish.",
        "The experience is one of traditional, major-championship intensity on impeccably conditioned turf. It has hosted nine U.S. Opens, with historic wins by Jack Nicklaus (1967 & 1980) and Phil Mickelson (2005). The club's history is palpable, from its name (derived from a murdered farmer) to its stately clubhouse. Golfers remember Baltusrol for its classic, demanding architecture, its history of crowning legends, and the thrilling, two-hole par-5 climax."
    ],
    'Ridgewood Country Club (East/West Combo)': [
        "A.W. Tillinghast's 1929 masterpiece in New Jersey ingeniously combines nines from three original courses into a 27-hole facility, with the classic championship routing using the East and West nines. The design is famous for its \"Five Farms\" hole, a par-5 with a fairway split by a massive tree, demanding a strategic choice off the tee. Mature hardwoods frame undulating fairways and large, subtly contoured greens.",
        "The challenge is strategic and varied, requiring thoughtful play on every shot. The conditions are always pristine, supporting its role as a regular host of professional events. It has hosted the PGA Tour's Barclays/FedEx Cup playoff events multiple times. Golfers remember Ridgewood for its clever, timeless Tillinghast design, its peaceful, wooded setting, and the unique strategic puzzle presented by iconic holes like \"Five Farms.\""
    ],
    'Los Angeles Country Club (North Course)': [
        "Following a transformative 2010 restoration by Gil Hanse, the North Course re-emerged as a brilliant George Thomas design from 1921. Located in the heart of Beverly Hills, it is a strategic masterpiece on rolling, sandy terrain with barrancas and majestic trees. Its character is defined by vast, wild fairways, bold, artistic bunkering, and large, complex greens. The par-3 15th, with its dramatically sunken green, is one of the most unique and challenging one-shotters in golf.",
        "Playing LACC North is a cerebral test of angles and creativity, where multiple routes to each hole exist. The firm, fast conditions encourage the ground game. Its coming-out party was the 2023 U.S. Open, which showcased its subtle genius to the world. Golfers remember it for its stunning restoration, its strategic depth that reveals itself over multiple rounds, and the surreal contrast of pristine, natural golf in an urban epicenter."
    ],
    'Garden City Golf Club': [
        "This historic Long Island club, founded in 1899, features a supremely strategic and subtle design by Walter J. Travis (with later input by Devereux Emmet). Built on sandy, rolling terrain, it is famous for its small, fiercely defended greens, treacherous cross-bunkers, and thick, native rough. The par-4 opening hole and the long, demanding par-4 10th are classic examples of its cerebral, positional challenge.",
        "Playing Garden City demands precision, patience, and superb course management over power. The wind is often a factor on its open, links-like property. It has a storied amateur history, hosting multiple Walker Cups and U.S. Amateurs. Golfers remember it for its old-world, traditional character, its incredibly clever design that rewards intelligence, and the sense of competing on a course that has tested the game's greatest amateurs for over a century."
    ],
    'Congressional Country Club (Blue Course)': [
        "A classic, tree-lined parkland in Bethesda, Maryland, the Blue Course (originally by Devereux Emmet, redesigned by Rees Jones) is a long, demanding championship test. Its character is defined by narrow, bending fairways, thick rough, and water hazards in play on several key holes. The par-4 18th, with its iconic island green, is one of the most recognizable and dramatic finishing holes in championship golf.",
        "The experience is one of unrelenting pressure, where accuracy off the tee is paramount to scoring. The conditions are kept immaculate for its major championships. It has hosted three U.S. Opens, a PGA Championship, and multiple Quicken Loans National events, with Rory McIlroy's record-setting 2011 U.S. Open win being its most famous moment. Golfers remember Congressional for its stately, traditional feel and the intense, demanding finish around and over the water on the 18th."
    ],
    'Riviera Country Club': [
        "George Thomas's 1926 masterpiece in Pacific Palisades is a strategic and iconic test that has hosted the PGA Tour's Genesis Invitational since 1929. Its character is defined by kikuyu grass rough, strategic bunkering, and unique holes like the par-4 10th—a drivable, risk-reward puzzle with a narrow, bunker-guarded green. The par-3 6th hole with its bunker in the middle of the green is another instantly recognizable feature.",
        "Playing \"Hogan's Alley\" (where Ben Hogan won three times) is a lesson in shot-making and strategy, not just power. The classic, understated routing has remained a consistent, revered test for the world's best. Its history is woven into Hollywood and golf lore. Golfers remember Riviera for its timeless, no-frills design, its perfect, temperate climate, and the sense of walking in the footsteps of countless legends on a course that never becomes obsolete."
    ],
    'Seminole Golf Club': [
        "Donald Ross's 1929 design in Juno Beach, Florida, is a legendary links-style course laid out on rolling, sandy dunes just inland from the Atlantic. Its genius lies in its routing, which ensures the challenging crosswinds are faced from every direction. The course is defined by its firm, fast fairways, large, undulating greens, and perfectly placed bunkers. The par-4 16th, playing directly into the prevailing wind, is one of its most demanding tests.",
        "The experience is one of pure, wind-swept golf that demands total control of ball flight. The club is famously private and exclusive, with a storied history of hosting the world's elite for informal matches. It has recently gained more visibility by hosting the Walker Cup and a high-profile charity match. Golfers remember Seminole for its peerless Donald Ross design, its incredibly challenging and consistent wind conditions, and its aura of quiet, understated prestige."
    ],
    'Bay Hill Club & Lodge': [
        "The spiritual home of Arnold Palmer, who purchased the club in 1976 and oversaw its continuous refinement, Bay Hill is a classic Florida test of water and sand. Its character is defined by generous fairways that lead to large, well-bunkered greens, with numerous lakes and ponds coming into play. The closing three holes—the risk-reward par-5 16th, the difficult par-3 17th over water, and the demanding par-4 18th along a lake—form \"The Bear Trap\" of Orlando.",
        "The experience is a tribute to Palmer's philosophy of aggressive, rewarding golf, but mistakes are punished by water. The conditions are maintained to PGA Tour standards year-round. As the annual host of the Arnold Palmer Invitational, it is a beloved stop where players pay homage to The King. Golfers remember Bay Hill for its warm, welcoming atmosphere, its challenging yet fair design, and the palpable presence of Arnold Palmer's legacy everywhere on the property."
    ],
    'Hazeltine National Golf Club': [
        "Robert Trent Jones Sr.'s 1962 design in Chaska, Minnesota, was built with the explicit purpose of hosting major championships. It is a long, brawny, and demanding test set around Lake Hazeltine, with tree-lined fairways, thick rough, and large, heavily contoured greens. The par-4 16th, a long dogleg around the lake, is one of the most famous and pivotal holes in Ryder Cup history, often deciding matches.",
        "The experience is one of championship-scale golf, where length and precision are both required. The course has been successfully modernized by Rees Jones to keep pace with the game. It has hosted two Ryder Cups (1991 & 2016), two U.S. Opens, and multiple PGA Championships, cementing its reputation. Golfers remember Hazeltine for its massive scale, its history of dramatic team and major championships, and the intense, stadium-like atmosphere of its closing holes."
    ],
    'San Francisco Golf Club': [
        "A.W. Tillinghast's 1918 design, set in the hills south of the city, is a majestic and serene parkland masterpiece. The course is renowned for its breathtaking setting, with panoramic views of the Pacific Ocean and the city, and its brilliant use of the natural, rolling terrain. The par-4 7th hole, \"Vista,\" and the dramatic, downhill par-3 17th are highlights of a routing that blends beauty with strategic challenge.",
        "Playing SFGC is a walk through a timeless, peaceful landscape with immaculate conditions. The challenge is strategic and subtle, with Tillinghast's trademark bunkering and green complexes demanding thoughtful play. It is a highly private club with a deep sense of tradition. Golfers remember it for its stunning, secluded beauty, its flawless Tillinghast architecture, and the feeling of playing one of America's most perfect and unspoiled classic courses."
    ],
    'Olympic Club (Lake Course)': [
        "Set in the sand dunes near San Francisco's Ocean Beach, the Lake Course (originally by Sam Whiting, remodeled by Bill Love) is a relentlessly tight, tree-lined test known for its steep, sloping fairways and small, firm greens. Its character is defined by a brutally difficult opening six holes, a stretch that has derailed many championship hopes, and a finish that offers little respite.",
        "The experience is one of survival, where par is a prized score from the first tee shot. The course famously favors a left-to-right ball flight, confounding many of the game's greats. It has hosted five U.S. Opens, with a reputation for producing shocking upsets (Fleck over Hogan in '55, Simpson over Watson in '87). Golfers remember Olympic for its unyielding, claustrophobic difficulty, its history of drama, and its unique, counterintuitive challenge."
    ],
    'Quaker Ridge Golf Club': [
        "This 1918 A.W. Tillinghast design in Scarsdale, New York, is a classic, strategic parkland considered one of his finest works. The course is built on rolling, wooded terrain and is famed for its brilliant, strategic bunkering, undulating fairways, and superb, challenging green complexes. The par-4 6th hole, with its dramatic, elevated green, and the long, difficult par-4 16th are standout examples of Tillinghast's genius.",
        "Playing Quaker Ridge is a thoughtful, demanding experience that rewards course management and precise iron play. The conditions are consistently excellent, maintaining its championship caliber. It has hosted elite amateur events like the Walker Cup and the PGA Tour's Northern Trust. Golfers remember it for its pristine, traditional presentation, its intelligent and fair Tillinghast design, and its status as a quietly revered gem among America's golden-age classics."
    ]
}

def main():
    # Load courses
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    updated = 0
    not_found = []
    
    # Update courses with descriptions
    for course_name, blurb in DESCRIPTIONS.items():
        course_id = COURSE_MAPPINGS.get(course_name)
        
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
            print(f"✗ No mapping found for: {course_name}")
    
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

