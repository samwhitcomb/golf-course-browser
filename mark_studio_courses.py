#!/usr/bin/env python3
"""
Mark certain courses as Studio courses with dual-version support
"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
COURSES_FILE = BASE_DIR / 'courses.json'

# Top-tier courses to mark as Studio (these will have both Standard and Studio versions)
STUDIO_COURSE_IDS = [
    'tara-iti',
    'cabot-cliffs',
    'cypress-point',  # Cypress Point
    'pebble-beach'
]

# Load courses
with open(COURSES_FILE, 'r', encoding='utf-8') as f:
    courses = json.load(f)

updated_count = 0

for course in courses:
    if course.get('id') in STUDIO_COURSE_IDS:
        # Mark as Studio course
        course['isStudio'] = True
        course['hasStandardVersion'] = True  # All Studio courses have standard version
        
        # Add Studio features
        course['studioFeatures'] = {
            'mappingType': 'Lidar',
            'resolution': 'True 4K Native',
            'physics': 'Advanced Slope Engine',
            'accuracy': 'Sub-Centimeter',
            'fileSize': '5 GB'
        }
        
        # Add Standard features for comparison
        course['standardFeatures'] = {
            'mappingType': 'Satellite',
            'resolution': 'HD (1080p)',
            'physics': 'Standard Terrain Model',
            'accuracy': '1m',
            'fileSize': '500 MB'
        }
        
        updated_count += 1
    else:
        # Remove Studio status from courses not in the list
        if course.get('isStudio'):
            course['isStudio'] = False
            # Optionally remove Studio features if you want to clean up
            # del course['studioFeatures']
            # del course['standardFeatures']
            # del course['hasStandardVersion']

# Save updated courses
with open(COURSES_FILE, 'w', encoding='utf-8') as f:
    json.dump(courses, f, indent=2, ensure_ascii=False)

print(f"Marked {updated_count} courses as Studio courses")
print(f"Total courses: {len(courses)}")

