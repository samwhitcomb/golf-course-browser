#!/usr/bin/env python3
"""
Script to update courses.json with static image paths for GitHub Pages hosting.
This replicates the backend logic that adds image paths dynamically.
"""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
COURSES_FILE = BASE_DIR / 'courses.json'
PUBLIC_COURSES_FILE = BASE_DIR / 'public' / 'courses.json'
IMAGES_DIR = BASE_DIR / 'public' / 'images'

def find_image_paths(course_id):
    """
    Find all existing images for a course (hero, 1, 2)
    Returns dict with 'hero', '1', '2' keys containing (filename, extension) or None
    """
    images = {'hero': None, '1': None, '2': None}
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    for slot in ['hero', '1', '2']:
        for ext in extensions:
            filename = f"{course_id}_{slot}{ext}"
            image_path = IMAGES_DIR / filename
            if image_path.exists():
                images[slot] = (filename, ext)
                break
    
    return images

def load_descriptions():
    """Load course descriptions from JSON file if it exists"""
    descriptions_file = BASE_DIR / 'course_descriptions.json'
    if descriptions_file.exists():
        try:
            with open(descriptions_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def main():
    # Load courses
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    descriptions = load_descriptions()
    
    # Process each course
    for course in courses:
        course_id = course['id']
        
        # Check for images in all slots
        image_paths = find_image_paths(course_id)
        
        # Build images object
        images = {
            'hero': None,
            'additional': []
        }
        
        # Hero image
        if image_paths['hero']:
            filename, ext = image_paths['hero']
            images['hero'] = f"/images/{filename}"
        
        # Additional images from file system (slot 1 and 2)
        for slot in ['1', '2']:
            if image_paths[slot]:
                filename, ext = image_paths[slot]
                images['additional'].append(f"/images/{filename}")
        
        # Preserve any existing additional images that aren't from file system slots
        # (e.g., gameplay images that were manually added)
        if 'images' in course and 'additional' in course['images']:
            existing_additional = course['images']['additional']
            if isinstance(existing_additional, list):
                for existing_img in existing_additional:
                    # Only add if it's not already in the list and not a slot image
                    if existing_img not in images['additional']:
                        # Check if it's not a slot image (doesn't match pattern _1 or _2)
                        if not any(f"_{slot}" in existing_img for slot in ['1', '2']):
                            images['additional'].append(existing_img)
        
        course['images'] = images
        
        # Preserve blurb for igolf courses (they have single-paragraph descriptions)
        if course.get('isIgolf', False) and 'blurb' not in course:
            # If igolf course has description but no blurb, create blurb array
            if course.get('description'):
                course['blurb'] = [course['description']]
        
        # Backward compatibility: set hasImage and imageUrl from hero
        # Preserve hasImage: false for igolf courses (to exclude from carousels)
        # But preserve imageUrl if it exists (for display in search results and modal)
        if course.get('isIgolf', False):
            course['hasImage'] = False  # Keep false to exclude from carousels
            # For igolf courses, use gameplay image if imageUrl is set
            if course.get('imageUrl') and 'Courses Gameplay' in course.get('imageUrl', ''):
                images['hero'] = course['imageUrl']  # Set images.hero to gameplay image
                course['images'] = images  # Update images object
            # Preserve existing imageUrl if set (e.g., gameplay image)
            if 'imageUrl' not in course or not course.get('imageUrl'):
                course['imageUrl'] = images['hero'] if images['hero'] else None
        else:
            course['hasImage'] = images['hero'] is not None
            course['imageUrl'] = images['hero']
        
        # Add descriptions if available
        if course_id in descriptions:
            course['blurb'] = descriptions[course_id]
    
    # Ensure public directory exists
    PUBLIC_COURSES_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Save updated courses to public directory
    with open(PUBLIC_COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)
    
    print(f"Updated courses.json with static image paths")
    print(f"Saved to: {PUBLIC_COURSES_FILE}")
    print(f"Total courses processed: {len(courses)}")
    
    # Count courses with images
    courses_with_images = sum(1 for c in courses if c.get('hasImage', False))
    print(f"Courses with images: {courses_with_images}")

if __name__ == '__main__':
    main()

