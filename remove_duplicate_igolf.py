#!/usr/bin/env python3
"""
Remove duplicate igolf courses from courses.json
"""

import json
from pathlib import Path

COURSES_FILE = Path('courses.json')

def remove_duplicates(courses):
    """Remove duplicate courses based on ID"""
    seen_ids = set()
    unique_courses = []
    duplicates_removed = 0
    
    for course in courses:
        course_id = course.get('id')
        if course_id not in seen_ids:
            seen_ids.add(course_id)
            unique_courses.append(course)
        else:
            duplicates_removed += 1
            print(f"  Removed duplicate: {course.get('name')} ({course_id})")
    
    return unique_courses, duplicates_removed

def main():
    print(f"Loading courses from {COURSES_FILE}...")
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    print(f"Found {len(courses)} courses (including duplicates)")
    
    # Remove duplicates
    unique_courses, removed = remove_duplicates(courses)
    
    print(f"\nRemoved {removed} duplicate courses")
    print(f"Remaining courses: {len(unique_courses)}")
    
    # Count by type
    igolf_count = sum(1 for c in unique_courses if c.get('isIgolf'))
    regular_count = sum(1 for c in unique_courses if not c.get('isIgolf'))
    print(f"  Regular courses: {regular_count}")
    print(f"  iGolf courses: {igolf_count}")
    
    # Save updated courses
    print(f"\nSaving updated courses to {COURSES_FILE}...")
    with open(COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(unique_courses, f, indent=2, ensure_ascii=False)
    
    print("✓ Duplicates removed")
    
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

