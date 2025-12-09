#!/usr/bin/env python3
"""
Check which courses are missing the full 2-paragraph description (blurb).
"""

import json
from pathlib import Path

COURSES_FILE = Path(__file__).parent / 'courses.json'

def main():
    # Load courses
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)

    missing_blurb = []
    incomplete_blurb = []
    complete_blurb = []

    for course in courses:
        course_id = course['id']
        course_name = course['name']
        blurb = course.get('blurb', [])
        
        if not blurb:
            missing_blurb.append((course_id, course_name))
        elif not isinstance(blurb, list):
            incomplete_blurb.append((course_id, course_name, f"blurb is not a list: {type(blurb)}"))
        elif len(blurb) < 2:
            incomplete_blurb.append((course_id, course_name, f"only {len(blurb)} paragraph(s)"))
        elif len(blurb) == 2:
            # Check if paragraphs are non-empty
            if not blurb[0] or not blurb[1] or not blurb[0].strip() or not blurb[1].strip():
                incomplete_blurb.append((course_id, course_name, "one or both paragraphs are empty"))
            else:
                complete_blurb.append((course_id, course_name))
        else:
            # More than 2 paragraphs - might be okay but note it
            if len(blurb) > 2:
                incomplete_blurb.append((course_id, course_name, f"has {len(blurb)} paragraphs (expected 2)"))

    print(f"Total courses: {len(courses)}")
    print(f"\n✓ Courses with complete 2-paragraph blurb: {len(complete_blurb)}")
    print(f"✗ Courses missing blurb entirely: {len(missing_blurb)}")
    print(f"⚠ Courses with incomplete blurb: {len(incomplete_blurb)}")

    if missing_blurb:
        print(f"\n{'='*60}")
        print(f"Courses Missing Blurb ({len(missing_blurb)})")
        print(f"{'='*60}")
        for course_id, course_name in missing_blurb:
            print(f"  - {course_name} ({course_id})")

    if incomplete_blurb:
        print(f"\n{'='*60}")
        print(f"Courses with Incomplete Blurb ({len(incomplete_blurb)})")
        print(f"{'='*60}")
        for course_id, course_name, reason in incomplete_blurb:
            print(f"  - {course_name} ({course_id}): {reason}")

    if complete_blurb:
        print(f"\n{'='*60}")
        print(f"Summary")
        print(f"{'='*60}")
        print(f"Complete: {len(complete_blurb)}/{len(courses)} ({len(complete_blurb)/len(courses)*100:.1f}%)")
        print(f"Needs work: {len(missing_blurb) + len(incomplete_blurb)}/{len(courses)} ({(len(missing_blurb) + len(incomplete_blurb))/len(courses)*100:.1f}%)")

if __name__ == '__main__':
    main()

