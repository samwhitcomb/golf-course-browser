import json
import re
from pathlib import Path

# Read the descriptions file
with open('course description.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Read courses.json
with open('courses.json', 'r', encoding='utf-8') as f:
    courses = json.load(f)

course_name_map = {course['name']: course['id'] for course in courses}

# Parse additional descriptions (starting from line 404)
descriptions = {}
current_course_name = None
para1_lines = []
para2_lines = []
in_para1 = False
in_para2 = False

# Find where "Additional Courses:" starts
start_idx = 0
for idx, line in enumerate(lines):
    if 'Additional Courses:' in line:
        start_idx = idx
        break

if start_idx == 0:
    # Try to find it by looking for "Europe (Beyond UK/Ireland)" or just start from end
    for idx, line in enumerate(lines):
        if 'Europe (Beyond UK/Ireland)' in line or 'Valderrama Golf Club' in line:
            start_idx = idx - 1 if idx > 0 else idx
            break

print(f"Found start at line {start_idx + 1} (total lines: {len(lines)})")

# Start parsing from there
i = start_idx
while i < len(lines):
    line = lines[i].rstrip()
    
    # Skip section headers and empty lines
    if not line or line in ['Europe (Beyond UK/Ireland)', 'Asia', 'Africa', 'Canada', 'Mexico & Caribbean', 'Other Regions', 'Additional Courses:']:
        i += 1
        continue
    
    # Check for course name - it's a standalone line followed by "Paragraph 1:" on next line
    # Course names don't start with Paragraph, **, ###, or ---
    if line and not line.startswith('Paragraph') and not line.startswith('**') and not line.startswith('###') and not line.startswith('---'):
        # Check if next line starts with "Paragraph 1:"
        if i + 1 < len(lines) and 'Paragraph 1:' in lines[i + 1]:
            # Save previous course if exists
            if current_course_name and para1_lines and para2_lines:
                para1 = ' '.join(para1_lines).strip()
                para2 = ' '.join(para2_lines).strip()
                if para1 and para2:
                    descriptions[current_course_name] = [para1, para2]
                    print(f"Saved: {current_course_name}")
            
            # Start new course
            current_course_name = line.strip()
            para1_lines = []
            para2_lines = []
            in_para1 = False
            in_para2 = False
            i += 1
            continue
    
    # Check for Paragraph 1 marker
    if 'Paragraph 1:' in line:
        in_para1 = True
        in_para2 = False
        # Extract text after marker
        text = line.split('Paragraph 1:', 1)[1].strip()
        if text:
            para1_lines.append(text)
        i += 1
        continue
    
    # Check for Paragraph 2 marker
    if 'Paragraph 2:' in line:
        in_para1 = False
        in_para2 = True
        # Extract text after marker
        text = line.split('Paragraph 2:', 1)[1].strip()
        if text:
            para2_lines.append(text)
        i += 1
        continue
    
    # Accumulate text for current paragraph
    if in_para1 and line and not line.startswith('Paragraph'):
        para1_lines.append(line)
    elif in_para2 and line and not line.startswith('Paragraph'):
        para2_lines.append(line)
    
    i += 1

# Save last course
if current_course_name and para1_lines and para2_lines:
    para1 = ' '.join(para1_lines).strip()
    para2 = ' '.join(para2_lines).strip()
    if para1 and para2:
        descriptions[current_course_name] = [para1, para2]

print(f"Extracted {len(descriptions)} descriptions:")
for name in list(descriptions.keys())[:5]:
    print(f"  - {name}")

# Manual mappings for the additional courses
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

# Normalize names for matching
def normalize_name(name):
    """Normalize course name for matching"""
    name = re.sub(r'\s*\([^)]*\)', '', name)
    name = re.sub(r'\s*(Golf Club|Golf Course|Country Club|Resort|Golf Links|Club|Championship Course|Championship Links|West Course|East Course|Straits Course|Irish Course|Red Course|Blue Course|Lake Course|North Course|South Course|Plantation Course|Makai Course|Gold Course|Stadium Course|Old Course|Ailsa Course|Balgownie Links|Dunluce Links|Saguaro Course|Monument Course|Weiskopf Course|Black Course|Ocean Course|State Park|The Links|Vallière Course|Albatros Course|Vineuil Course).*$', '', name, flags=re.IGNORECASE)
    return name.strip().lower()

# Match descriptions to courses
matched_count = 0
for desc_name, desc_text in descriptions.items():
    matched_id = None
    
    # Try manual mapping first
    if desc_name in manual_mappings:
        matched_id = manual_mappings[desc_name]
    # Try exact match
    elif desc_name in course_name_map:
        matched_id = course_name_map[desc_name]
    else:
        # Try normalized matching
        desc_norm = normalize_name(desc_name)
        best_match = None
        best_score = 0
        
        for course_name, course_id in course_name_map.items():
            course_norm = normalize_name(course_name)
            
            if desc_norm == course_norm:
                matched_id = course_id
                break
            
            # Word-based matching
            course_words = set(course_norm.split())
            desc_words = set(desc_norm.split())
            overlap = len(course_words & desc_words)
            total = len(course_words | desc_words)
            if total > 0:
                score = overlap / total
                if desc_norm in course_norm or course_norm in desc_norm:
                    score += 0.3
                if score > best_score and score > 0.3:
                    best_score = score
                    best_match = course_id
        
        if best_match:
            matched_id = best_match
    
    if matched_id:
        # Update course with blurb
        for course in courses:
            if course['id'] == matched_id:
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

# Show unmatched
unmatched = [name for name in descriptions.keys() if name not in [c['name'] for c in courses if c.get('blurb')]]
if unmatched:
    print(f"\nUnmatched descriptions ({len(unmatched)}):")
    for name in unmatched:
        print(f"  - {name}")

