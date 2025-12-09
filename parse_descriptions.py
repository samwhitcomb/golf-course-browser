import json
import re

# Read the descriptions file line by line
with open('course description.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Read courses.json
with open('courses.json', 'r', encoding='utf-8') as f:
    courses = json.load(f)

course_name_map = {course['name']: course['id'] for course in courses}

descriptions = {}
current_course = None
para1_lines = []
para2_lines = []
in_para1 = False
in_para2 = False

i = 0
while i < len(lines):
    line = lines[i].rstrip()
    
    # Check for course header (### **Course Name**)
    if line.startswith('### **') and line.endswith('**'):
        # Save previous course if exists
        if current_course and para1_lines and para2_lines:
            para1 = ' '.join(para1_lines).strip()
            para2 = ' '.join(para2_lines).strip()
            if para1 and para2:
                descriptions[current_course] = [para1, para2]
        
        # Start new course
        current_course = line[6:-2].strip()  # Remove ### ** and **
        para1_lines = []
        para2_lines = []
        in_para1 = False
        in_para2 = False
        i += 1
        continue
    
    # Check for Paragraph 1 marker
    if '**Paragraph 1:**' in line:
        in_para1 = True
        in_para2 = False
        # Extract text after marker
        text = line.split('**Paragraph 1:**', 1)[1].strip()
        if text:
            para1_lines.append(text)
        i += 1
        continue
    
    # Check for Paragraph 2 marker
    if '**Paragraph 2:**' in line:
        in_para1 = False
        in_para2 = True
        # Extract text after marker
        text = line.split('**Paragraph 2:**', 1)[1].strip()
        if text:
            para2_lines.append(text)
        i += 1
        continue
    
    # Accumulate text for current paragraph
    if in_para1 and line and not line.startswith('---') and not line.startswith('###') and not line.startswith('**') and not line.startswith('Excellent') and not line.startswith('Let\'s') and not line.startswith('This') and not line.startswith('Note:'):
        para1_lines.append(line)
    elif in_para2 and line and not line.startswith('---') and not line.startswith('###') and not line.startswith('**') and not line.startswith('Excellent') and not line.startswith('Let\'s') and not line.startswith('This') and not line.startswith('Note:') and not line.startswith('Completion'):
        para2_lines.append(line)
    
    i += 1

# Save last course
if current_course and para1_lines and para2_lines:
    para1 = ' '.join(para1_lines).strip()
    para2 = ' '.join(para2_lines).strip()
    if para1 and para2:
        descriptions[current_course] = [para1, para2]

# Create mapping by course ID with smart matching
course_descriptions = {}

def normalize_name(name):
    """Normalize course name for matching"""
    # Extract parenthetical content as alternative name
    parenthetical = re.search(r'\(([^)]+)\)', name)
    parenthetical_name = parenthetical.group(1) if parenthetical else None
    
    # Remove parenthetical info for base name
    base_name = re.sub(r'\s*\([^)]*\)', '', name)
    # Remove common suffixes
    base_name = re.sub(r'\s*(Golf Club|Golf Course|Country Club|Resort|Golf Links|Club|Championship Course|Championship Links|West Course|East Course|Straits Course|Irish Course|Red Course|Blue Course|Lake Course|North Course|South Course|Plantation Course|Makai Course|Gold Course|Stadium Course|Old Course|Ailsa Course|Balgownie Links|Dunluce Links|Saguaro Course|Monument Course|Weiskopf Course|Black Course|Ocean Course|State Park).*$', '', base_name, flags=re.IGNORECASE)
    
    return base_name.strip().lower(), parenthetical_name.strip().lower() if parenthetical_name else None

# Skip courses that don't have descriptions
skip_courses = [
    "The Loop at Crystal Downs",  # Error note, not a real course
    "Completion & Summary",  # Not a course
]

# Manual mappings for tricky cases
manual_mappings = {
    "Kiawah Island Golf Resort (Ocean Course)": "kiawah-ocean",
    "Kiawah Island Ocean Course": "kiawah-ocean",
    "Garden City Golf Club": "garden-city",  # First one (the one with description)
    "Eastward Ho! Country Club": "eastward-ho",  # Note the exclamation mark
    "The Loop at Forest Dunes (Black/Red)": "forest-dunes",  # Map to Forest Dunes
    "The Loop at Crystal Downs": None,  # This is an error note, skip it
    "Los Angeles Country Club (North)": "los-angeles-north",
    "Yeamans Hall Club": "yeamans-hall",
    "Hazeltine National Golf Club": "hazeltine",
    "San Francisco Golf Club": "san-francisco-golf",
    "Garden City Golf Club": "garden-city-gc",  # Second Garden City
    "Quaker Ridge Golf Club": "quaker-ridge",
    "Shoreacres Golf Club": "shoreacres",
    "Eastward Ho Country Club": "eastward-ho",
    "Royal Aberdeen Golf Club (Balgownie Links)": "royal-aberdeen",
    "Kingsbarns Golf Links": "kingsbarns",
    "Castle Pines Golf Club": "castle-pines",
    "Half Moon Bay Golf Links (Ocean Course)": "half-moon-bay",
    "Half Moon Bay Golf Links": "half-moon-bay",
    "Chambers Bay Golf Course": "chambers-bay",
    "Whistling Straits (Irish Course)": "whistling-straits-irish",
    "Streamsong Resort (Red Course)": "streamsong-red",
    "Streamsong Resort (Blue Course)": "streamsong-blue",
    "Trump National Doral": "trump-doral",
    "Torrey Pines Golf Course (South)": "torrey-pines-south",
    "Spyglass Hill Golf Course": "spyglass-hill",
    "French Lick Resort (Pete Dye Course)": "french-lick",
    "Bandon Trails": "bandon-trails",
    "Old Macdonald": "old-macdonald",
    "Harbour Town Golf Links": "harbour-town",
    "TPC Sawgrass (Stadium Course)": "tpc-sawgrass",
    "Shadow Creek Golf Course": "shadow-creek",
    "Cascata Golf Club": "cascata",
    "Wolf Creek Golf Club": "wolf-creek",
    "Kapalua Resort (Plantation Course)": "kapalua-plantation",
    "Mauna Kea Golf Course": "mauna-kea",
    "Princeville Resort (Makai Course)": "princeville",
    "Wailea Golf Club (Gold Course)": "wailea-gold",
    "PGA West (Stadium Course)": "pga-west-stadium",
    "Indian Wells Golf Resort": "indian-wells",
    "Desert Highlands Golf Club": "desert-highlands",
    "Troon North Golf Club (Monument Course)": "troon-north",
    "Troon North Golf Club": "troon-north",
    "We-Ko-Pa Golf Club (Saguaro Course)": "we-ko-pa",
    "We-Ko-Pa Golf Club": "we-ko-pa",
    "Four Seasons Resort Scottsdale": "four-seasons-scottsdale",
    "Tobacco Road Golf Club": "tobacco-road",
    "True Blue Golf Club": "true-blue",
    "Caledonia Golf & Fish Club": "caledonia",
    "The Dunes Golf & Beach Club": "dunes-golf-beach",
    "Tidewater Golf Club": "tidewater",
    "Eagle Point Golf Club": "eagle-point",
    "Forest Dunes Golf Club (Weiskopf Course)": "forest-dunes",
    "Forest Dunes Golf Club": "forest-dunes",
    "Arcadia Bluffs Golf Club": "arcadia-bluffs",
    "Bay Harbor Golf Club": "bay-harbor",
    "Blackwolf Run Golf Club": "kohler-blackwolf",
    "Erin Hills Golf Course": "erin-hills",
    "Pete Dye Golf Club": "pete-dye-gc",
    "The Greenbrier (Old White Course)": "greenbrier",
    "The Homestead (Cascades Course)": "homestead-cascades",
    "Kingsmill Resort": "kingsmill",
    "Golden Horseshoe Golf Club": "golden-horseshoe",
    "Kiawah Island Golf Resort (River Course)": "kiawah-river",
    "Wild Dunes Resort": "wild-dunes",
    "Kauri Cliffs Golf Course": "kauri-cliffs",
    "Cape Kidnappers Golf Course": "cape-kidnappers",
    "Tara Iti Golf Club": "tara-iti",
    "Barnbougle Dunes Golf Links": "barnbougle-dunes",
    "King Island Golf Club": "king-island",
}

# Match descriptions to courses
for desc_name, desc_text in descriptions.items():
    # Skip non-course entries
    if desc_name in skip_courses:
        continue
    
    matched_id = None
    
    # Try manual mapping first
    if desc_name in manual_mappings:
        matched_id = manual_mappings[desc_name]
    # Try exact match
    elif desc_name in course_name_map:
        matched_id = course_name_map[desc_name]
    else:
        # Normalize and try matching
        desc_base, desc_parenthetical = normalize_name(desc_name)
        best_match = None
        best_score = 0
        
        for course_name, course_id in course_name_map.items():
            course_base, course_parenthetical = normalize_name(course_name)
            
            # Check if parenthetical matches base name (e.g., "Bandon Dunes (Pacific Dunes)" -> "Pacific Dunes")
            if desc_parenthetical:
                if desc_parenthetical == course_base or desc_parenthetical in course_base or course_base in desc_parenthetical:
                    matched_id = course_id
                    break
            
            if course_parenthetical:
                if course_parenthetical == desc_base or course_parenthetical in desc_base or desc_base in course_parenthetical:
                    matched_id = course_id
                    break
            
            # Exact normalized match
            if desc_base == course_base:
                matched_id = course_id
                break
            
            # Word-based matching
            desc_words = set(desc_base.split())
            course_words = set(course_base.split())
            
            # Skip if both are too short
            if len(desc_words) < 2 and len(course_words) < 2:
                continue
            
            overlap = len(desc_words & course_words)
            total = len(desc_words | course_words)
            if total > 0:
                score = overlap / total
                # Bonus for substring match
                if desc_base in course_base or course_base in desc_base:
                    score += 0.3
                # Bonus if all words match
                if overlap == min(len(desc_words), len(course_words)) and overlap > 0:
                    score += 0.2
                if score > best_score and score > 0.3:  # Lowered threshold to 30%
                    best_score = score
                    best_match = course_id
        
        if best_match and not matched_id:
            matched_id = best_match
    
    if matched_id:
        # Handle duplicate course names - prefer the one with more specific description
        if matched_id in course_descriptions:
            # If we already have a description for this ID, keep the first one
            pass
        else:
            course_descriptions[matched_id] = desc_text

# Save as JSON
with open('course_descriptions.json', 'w', encoding='utf-8') as f:
    json.dump(course_descriptions, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(descriptions)} descriptions from file")
print(f"Matched {len(course_descriptions)} to courses")

# Show some examples
print("\nSample matches:")
for i, (cid, desc) in enumerate(list(course_descriptions.items())[:5]):
    course = next((c for c in courses if c['id'] == cid), None)
    if course:
        print(f"  ✓ {course['name']}")
        print(f"    Para1: {len(desc[0])} chars, Para2: {len(desc[1])} chars")

# Show unmatched
unmatched = [c for c in courses if c['id'] not in course_descriptions]
if unmatched:
    print(f"\nUnmatched ({len(unmatched)}):")
    for c in unmatched[:10]:
        print(f"  - {c['name']}")
