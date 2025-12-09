import json
import re
from pathlib import Path

def extract_architect(course):
    """Extract architect from course data"""
    if course.get('architect'):
        return course['architect']
    
    desc = course.get('description', '')
    blurbs = course.get('blurb', [])
    if isinstance(blurbs, list):
        blurb_text = ' '.join(blurbs)
    else:
        blurb_text = str(blurbs) if blurbs else ''
    
    full_text = (desc + ' ' + blurb_text).lower()
    
    architect_patterns = [
        ('Alister MacKenzie', ['alister mackenzie', 'mackenzie']),
        ('Donald Ross', ['donald ross', 'ross']),
        ('Pete Dye', ['pete dye', 'p. dye']),
        ('Jack Nicklaus', ['jack nicklaus', 'nicklaus']),
        ('Ben Crenshaw', ['ben crenshaw', 'crenshaw']),
        ('Bill Coore', ['bill coore', 'coore']),
        ('A.W. Tillinghast', ['tillinghast', 'a.w. tillinghast']),
        ('Hugh Wilson', ['hugh wilson']),
        ('Old Tom Morris', ['old tom morris', 'tom morris']),
        ('Harry Colt', ['harry colt', 'colt']),
        ('Tom Weiskopf', ['tom weiskopf', 'weiskopf']),
        ('Tom Fazio', ['tom fazio', 'fazio']),
        ('Robert Trent Jones', ['robert trent jones', 'rtj']),
        ('George Thomas', ['george thomas']),
        ('William Flynn', ['william flynn', 'flynn']),
        ('Perry Maxwell', ['perry maxwell', 'maxwell']),
        ('Walter Travis', ['walter travis', 'travis']),
    ]
    
    for arch_name, patterns in architect_patterns:
        for pattern in patterns:
            if pattern in full_text:
                return arch_name
    
    return None

def extract_established_year(course):
    """Extract established year from course data"""
    if course.get('established'):
        return course['established']
    
    desc = course.get('description', '')
    blurbs = course.get('blurb', [])
    if isinstance(blurbs, list):
        blurb_text = ' '.join(blurbs)
    else:
        blurb_text = str(blurbs) if blurbs else ''
    
    full_text = desc + ' ' + blurb_text
    
    year_patterns = [
        r'founded\s+(\d{4})',
        r'established\s+(\d{4})',
        r'opened\s+(\d{4})',
        r'built\s+(\d{4})',
        r'since\s+(\d{4})',
    ]
    
    for pattern in year_patterns:
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            year = int(match.group(1))
            if 1800 <= year <= 2024:
                return year
    
    return None

# Load courses
courses_file = Path(__file__).parent / 'courses.json'
descriptions_file = Path(__file__).parent / 'course_descriptions.json'

with open(courses_file, 'r', encoding='utf-8') as f:
    courses = json.load(f)

# Load descriptions
descriptions = {}
if descriptions_file.exists():
    with open(descriptions_file, 'r', encoding='utf-8') as f:
        descriptions = json.load(f)

# Enhance courses with extracted data
for course in courses:
    course_id = course['id']
    
    # Add blurbs from descriptions file
    if course_id in descriptions:
        course['blurb'] = descriptions[course_id]
    
    # Extract architect
    architect = extract_architect(course)
    if architect:
        course['architect'] = architect
    
    # Extract established year
    established = extract_established_year(course)
    if established:
        course['established'] = established

# Save enhanced courses
with open(courses_file, 'w', encoding='utf-8') as f:
    json.dump(courses, f, indent=2, ensure_ascii=False)

print(f"Enhanced {len(courses)} courses with extracted data")
architect_count = sum(1 for c in courses if c.get('architect'))
established_count = sum(1 for c in courses if c.get('established'))
print(f"  - Architects found: {architect_count}")
print(f"  - Established years found: {established_count}")


