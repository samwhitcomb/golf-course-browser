#!/usr/bin/env python3
"""
Update all igolf courses to use the gameplay image
"""

import json
from pathlib import Path

COURSES_FILE = Path('courses.json')
PUBLIC_COURSES_FILE = Path('public') / 'courses.json'
GAMEPLAY_IMAGE = '/images/Courses Gameplay.png'

def update_igolf_images(courses):
    """Update igolf courses to use gameplay image"""
    updated = 0
    
    for course in courses:
        if course.get('isIgolf', False):
            # Set imageUrl to gameplay image
            course['imageUrl'] = GAMEPLAY_IMAGE
            
            # Set images.hero to gameplay image
            if 'images' not in course:
                course['images'] = {'hero': None, 'additional': []}
            course['images']['hero'] = GAMEPLAY_IMAGE
            
            # Keep hasImage as false to exclude from carousels
            # But set imageUrl so it displays in modal and search results
            updated += 1
    
    return updated

def main():
    # Load courses
    print(f"Loading courses from {COURSES_FILE}...")
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    print(f"Found {len(courses)} courses")
    
    # Update igolf courses
    updated = update_igolf_images(courses)
    
    # Save updated courses
    print(f"\nSaving updated courses to {COURSES_FILE}...")
    with open(COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Updated {updated} igolf courses with gameplay image")
    
    # Regenerate public/courses.json
    print(f"\nRegenerating {PUBLIC_COURSES_FILE}...")
    import subprocess
    result = subprocess.run(['python3', 'update_courses_for_static.py'], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

if __name__ == '__main__':
    main()

