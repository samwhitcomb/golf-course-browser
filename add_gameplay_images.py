#!/usr/bin/env python3
"""
Add the gameplay image to each course's additional images array
"""

import json
from pathlib import Path

COURSES_FILE = Path('courses.json')
PUBLIC_COURSES_FILE = Path('public') / 'courses.json'
GAMEPLAY_IMAGE = 'Courses Gameplay.png'

def add_gameplay_image(courses):
    """Add gameplay image to each course's additional images"""
    gameplay_path = f'/images/{GAMEPLAY_IMAGE}'
    
    updated_count = 0
    
    for course in courses:
        # Initialize images object if it doesn't exist
        if 'images' not in course:
            course['images'] = {
                'hero': course.get('imageUrl', ''),
                'additional': []
            }
        
        # Ensure additional is a list
        if 'additional' not in course['images']:
            course['images']['additional'] = []
        elif not isinstance(course['images']['additional'], list):
            course['images']['additional'] = []
        
        # Check if gameplay image is already in additional images
        if gameplay_path not in course['images']['additional']:
            # Add gameplay image to additional images
            course['images']['additional'].append(gameplay_path)
            updated_count += 1
    
    return updated_count

def main():
    # Load courses from source file
    print(f"Loading courses from {COURSES_FILE}...")
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    print(f"Found {len(courses)} courses")
    
    # Add gameplay image to each course
    updated_count = add_gameplay_image(courses)
    
    # Save updated courses
    print(f"\nSaving updated courses to {COURSES_FILE}...")
    with open(COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Updated {updated_count} courses with gameplay image")
    
    # Regenerate public/courses.json
    print(f"\nRegenerating {PUBLIC_COURSES_FILE}...")
    import subprocess
    result = subprocess.run(['python3', 'update_courses_for_static.py'], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Total courses: {len(courses)}")
    print(f"  Courses with gameplay image: {updated_count}")
    print(f"  Gameplay image path: /images/{GAMEPLAY_IMAGE}")

if __name__ == '__main__':
    main()

