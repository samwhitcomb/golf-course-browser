#!/usr/bin/env python3
"""
Parse course descriptions from course description.txt and add them to courses.json
"""

import json
import re
from pathlib import Path

COURSES_FILE = Path('courses.json')
DESCRIPTIONS_FILE = Path('course description.txt')

# Course name mappings (some names in file might differ slightly from JSON)
COURSE_NAME_MAPPINGS = {
    'Bethpage State Park (Black Course)': 'bethpage-black',
    'Bethpage State Park (Black)': 'bethpage-black',
    'Maidstone Club': 'maidstone-club',
    'Baltusrol Golf Club (Lower Course)': 'baltusrol-lower',
    'Baltusrol Golf Club (Lower)': 'baltusrol-lower',
    'Ridgewood Country Club (East/West Combo)': 'ridgewood',
    'Ridgewood Country Club': 'ridgewood',
    'Los Angeles Country Club (North Course)': 'los-angeles-north',
    'Los Angeles Country Club (North)': 'los-angeles-north',
    'Garden City Golf Club': 'garden-city',
    'Congressional Country Club (Blue Course)': 'congressional',
    'Congressional Country Club': 'congressional',
    'Riviera Country Club': 'riviera',
    'Seminole Golf Club': 'seminole',
    'Bay Hill Club & Lodge': 'bay-hill',
    'Bay Hill': 'bay-hill',
    'Hazeltine National Golf Club': 'hazeltine',
    'Hazeltine': 'hazeltine',
    'San Francisco Golf Club': 'san-francisco-golf',
    'Olympic Club (Lake Course)': 'olympic-lake',
    'Olympic Club': 'olympic-lake',
    'Quaker Ridge Golf Club': 'quaker-ridge',
    'Quaker Ridge': 'quaker-ridge',
}

def parse_descriptions(start_line=491, end_line=534):
    """Parse descriptions from the text file, optionally from specific line range"""
    with open(DESCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    
    # Extract the specific range if provided
    if start_line and end_line:
        lines = [line.strip() for line in all_lines[start_line-1:end_line] if line.strip()]
    else:
        lines = [line.strip() for line in all_lines if line.strip()]
    
    descriptions = {}
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a course name (not starting with "Paragraph")
        if not line.startswith('Paragraph'):
            course_name = line
            
            # Look for the two paragraphs
            para1 = None
            para2 = None
            
            # Check next line for Paragraph 1
            if i + 1 < len(lines) and lines[i + 1].startswith('Paragraph 1:'):
                para1 = lines[i + 1].replace('Paragraph 1:', '').strip()
            
            # Check next line for Paragraph 2
            if i + 2 < len(lines) and lines[i + 2].startswith('Paragraph 2:'):
                para2 = lines[i + 2].replace('Paragraph 2:', '').strip()
            
            if para1 and para2:
                descriptions[course_name] = [para1, para2]
                i += 3
            else:
                i += 1
        else:
            i += 1
    
    return descriptions

def find_course_id_by_name(courses, course_name):
    """Find course ID by matching name"""
    # Try direct mapping first
    if course_name in COURSE_NAME_MAPPINGS:
        course_id = COURSE_NAME_MAPPINGS[course_name]
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
        
        # Check for partial matches (e.g., "Bethpage" matches "Bethpage State Park")
        name_parts = course_name_lower.split()
        json_parts = course_json_name.split()
        if len(name_parts) > 0 and name_parts[0] in json_parts:
            return course['id']
    
    return None

def main():
    # Load courses
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    # Parse descriptions from lines 491-534
    descriptions = parse_descriptions(start_line=491, end_line=534)
    
    print(f"Found {len(descriptions)} course descriptions in file")
    
    # Update courses
    updated = 0
    not_found = []
    
    for course_name, blurb in descriptions.items():
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

