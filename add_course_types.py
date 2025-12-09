import json
import re

# Read courses.json
with open('courses.json', 'r', encoding='utf-8') as f:
    courses = json.load(f)

# Read descriptions to extract course types
with open('course description.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Course type keywords and their normalized types
type_keywords = {
    'links': ['links', 'links-style', 'links course', 'linksland'],
    'parkland': ['parkland', 'parkland course'],
    'sandbelt': ['sandbelt', 'sand belt'],
    'desert': ['desert', 'desert course', 'desertscape'],
    'mountain': ['mountain', 'mountain course', 'high-altitude'],
    'resort': ['resort', 'resort course'],
    'championship': ['championship', 'championship course', 'championship venue'],
    'coastal': ['coastal', 'oceanfront', 'ocean', 'seaside', 'clifftop', 'cliff'],
}

# Function to extract course type from description text
def extract_course_type(course_name, description_text):
    """Extract course type from description"""
    text_lower = description_text.lower()
    course_name_lower = course_name.lower()
    
    # Check for specific patterns
    types_found = []
    
    # Links courses
    if any(kw in text_lower for kw in ['links', 'links-style', 'links course', 'linksland', 'firm, fast', 'ground game']):
        if 'parkland' not in text_lower:  # Don't tag as links if explicitly parkland
            types_found.append('links')
    
    # Sandbelt
    if 'sandbelt' in text_lower or 'sand belt' in text_lower:
        types_found.append('sandbelt')
    
    # Desert
    if any(kw in text_lower for kw in ['desert', 'desertscape', 'saguaro', 'sonoran']):
        types_found.append('desert')
    
    # Mountain
    if any(kw in text_lower for kw in ['mountain', 'high-altitude', 'foothills', 'elevation']):
        types_found.append('mountain')
    
    # Coastal/Ocean
    if any(kw in text_lower for kw in ['ocean', 'oceanfront', 'coastal', 'seaside', 'clifftop', 'pacific', 'atlantic', 'caribbean']):
        types_found.append('coastal')
    
    # Resort
    if 'resort' in text_lower or 'resort course' in text_lower:
        types_found.append('resort')
    
    # Championship
    if any(kw in text_lower for kw in ['championship', 'major', 'u.s. open', 'open championship', 'pga championship', 'masters', 'ryder cup']):
        types_found.append('championship')
    
    # Parkland (if not links and has trees/forest)
    if not types_found or ('parkland' in text_lower or ('tree' in text_lower and 'forest' in text_lower)):
        if 'links' not in text_lower:
            types_found.append('parkland')
    
    # Default to parkland if nothing found
    if not types_found:
        types_found.append('parkland')
    
    return types_found[0] if types_found else 'parkland'  # Return first/primary type

# Load course descriptions
with open('course_descriptions.json', 'r', encoding='utf-8') as f:
    descriptions = json.load(f)

# Add course types to courses
for course in courses:
    course_id = course['id']
    course_name = course['name']
    
    # Get description text if available
    if course_id in descriptions:
        desc_text = ' '.join(descriptions[course_id])
        course_type = extract_course_type(course_name, desc_text)
    else:
        # Fallback: use description field
        desc_text = course.get('description', '').lower()
        course_type = extract_course_type(course_name, desc_text)
    
    course['type'] = course_type

# Save updated courses.json
with open('courses.json', 'w', encoding='utf-8') as f:
    json.dump(courses, f, indent=2, ensure_ascii=False)

# Print summary
from collections import Counter
type_counts = Counter(c.get('type') for c in courses)
print(f"Added course types to {len(courses)} courses")
print(f"\nCourse type distribution:")
for course_type, count in sorted(type_counts.items()):
    print(f"  {course_type}: {count} courses")


