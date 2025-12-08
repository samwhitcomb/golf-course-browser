import json
import re

# Read the descriptions file line by line
with open('course description.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Read courses.json
with open('courses.json', 'r', encoding='utf-8') as f:
    courses = json.load(f)

course_name_map = {course['name']: course['id'] for course in courses}

# Batch definitions
batch_mappings = {
    'Batch 1: The Absolute Icons & Major Venues': 'Absolute Icons & Major Venues',
    'Batch 2: Premier Global Links & Sandbelt': 'Premier Global Links & Sandbelt',
    'Batch 3: Classic American Golden Age Designs': 'Classic American Golden Age Designs',
    'Batch 4: Historic & Championship International Links': 'Historic & Championship International Links',
    'Batch 5: Modern American Icons & Stadium Courses': 'Modern American Icons & Stadium Courses',
    'Batch 6: Destination & Scenic Resort Courses': 'Destination & Scenic Resort Courses',
    'Batch 7: Desert & Mountain Classics': 'Desert & Mountain Classics',
    'Batch 8: Strategic & Artistic Gems': 'Strategic & Artistic Gems',
}

# Parse file to find batches and courses
current_batch = None
course_batches = {}

i = 0
while i < len(lines):
    line = lines[i].strip()
    
    # Check for batch header
    for batch_key, batch_name in batch_mappings.items():
        if batch_key in line:
            current_batch = batch_name
            break
    
    # Check for course header (### **Course Name**)
    if line.startswith('### **') and line.endswith('**'):
        course_name = line[6:-2].strip()  # Remove ### ** and **
        if current_batch:
            course_batches[course_name] = current_batch
    
    i += 1

# Normalize names for matching (same as parse_descriptions.py)
def normalize_name(name):
    """Normalize course name for matching"""
    name = re.sub(r'\s*\([^)]*\)', '', name)
    name = re.sub(r'\s*(Golf Club|Golf Course|Country Club|Resort|Golf Links|Club|Championship Course|Championship Links|West Course|East Course|Straits Course|Irish Course|Red Course|Blue Course|Lake Course|North Course|South Course|Plantation Course|Makai Course|Gold Course|Stadium Course|Old Course|Ailsa Course|Balgownie Links|Dunluce Links|Saguaro Course|Monument Course|Weiskopf Course|Black Course|Ocean Course|State Park).*$', '', name, flags=re.IGNORECASE)
    return name.strip().lower()

# Manual mappings for tricky cases (same as parse_descriptions.py)
manual_batch_mappings = {
    "Kiawah Island Golf Resort (Ocean Course)": "Modern American Icons & Stadium Courses",
    "Garden City Golf Club": "Classic American Golden Age Designs",
    "Eastward Ho! Country Club": "Strategic & Artistic Gems",
    "The Loop at Forest Dunes (Black/Red)": "Strategic & Artistic Gems",
}

# Match batches to courses
for course in courses:
    course_name = course['name']
    matched_batch = None
    
    # Try manual mapping first
    if course_name in manual_batch_mappings:
        matched_batch = manual_batch_mappings[course_name]
    # Try exact match
    elif course_name in course_batches:
        matched_batch = course_batches[course_name]
    else:
        # Try normalized matching
        course_norm = normalize_name(course_name)
        best_match = None
        best_score = 0
        
        for desc_name, batch_name in course_batches.items():
            desc_norm = normalize_name(desc_name)
            
            if desc_norm == course_norm:
                matched_batch = batch_name
                break
            
            # Word-based matching
            course_words = set(course_norm.split())
            desc_words = set(desc_norm.split())
            overlap = len(course_words & desc_words)
            total = len(course_words | course_words)
            if total > 0:
                score = overlap / total
                if desc_norm in course_norm or course_norm in desc_norm:
                    score += 0.3
                if score > best_score and score > 0.3:
                    best_score = score
                    best_match = batch_name
        
        if best_match:
            matched_batch = best_match
    
    # Add batch tag to course
    if matched_batch:
        course['batch'] = matched_batch

# Save updated courses.json
with open('courses.json', 'w', encoding='utf-8') as f:
    json.dump(courses, f, indent=2, ensure_ascii=False)

# Print summary
batched = [c for c in courses if c.get('batch')]
print(f"Added batch tags to {len(batched)} courses")
print(f"\nBatch distribution:")
from collections import Counter
batch_counts = Counter(c.get('batch') for c in courses if c.get('batch'))
for batch, count in sorted(batch_counts.items()):
    print(f"  {batch}: {count} courses")

unbatched = [c for c in courses if not c.get('batch')]
if unbatched:
    print(f"\nCourses without batch tags ({len(unbatched)}):")
    for c in unbatched[:10]:
        print(f"  - {c['name']}")
