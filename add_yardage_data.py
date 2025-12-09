import json
import random
from pathlib import Path

# Load courses
courses_file = Path(__file__).parent / 'courses.json'
with open(courses_file, 'r', encoding='utf-8') as f:
    courses = json.load(f)

# Add realistic yardage based on course type and rating
for course in courses:
    if course.get('yardage'):
        continue  # Skip if already has yardage
    
    # Generate realistic yardage based on course characteristics
    course_type = course.get('type', 'parkland')
    rating = course.get('rating', 4.0)
    
    # Championship courses tend to be longer
    if course_type == 'championship' or rating >= 4.5:
        base = 7200
        variance = 400
    elif course_type == 'links':
        base = 7000
        variance = 500
    elif course_type == 'resort':
        base = 6800
        variance = 400
    else:
        base = 6900
        variance = 500
    
    # Add some randomness but keep it realistic
    yardage = base + random.randint(-variance, variance)
    # Round to nearest 50
    yardage = round(yardage / 50) * 50
    
    course['yardage'] = yardage

# Save updated courses
with open(courses_file, 'w', encoding='utf-8') as f:
    json.dump(courses, f, indent=2, ensure_ascii=False)

print(f"Added yardage to {len(courses)} courses")
print(f"Sample yardages:")
for course in courses[:5]:
    print(f"  {course['name']}: {course['yardage']} yards")


