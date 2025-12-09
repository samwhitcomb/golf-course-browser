#!/usr/bin/env python3
"""
Migration script to convert existing single images to new 3-image structure.
Moves existing images to hero slot.
"""
import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent
COURSES_FILE = BASE_DIR / 'courses.json'
IMAGES_DIR = BASE_DIR / 'images'

def migrate_images():
    """Migrate existing single images to hero slot"""
    if not COURSES_FILE.exists():
        print(f"courses.json not found at {COURSES_FILE}")
        return
    
    # Load courses
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    migrated_count = 0
    
    for course in courses:
        course_id = course.get('id')
        if not course_id:
            continue
        
        # Check for old format image (without _hero suffix)
        old_image_found = False
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        
        for ext in extensions:
            old_path = IMAGES_DIR / f"{course_id}{ext}"
            if old_path.exists():
                # Move to hero slot
                new_path = IMAGES_DIR / f"{course_id}_hero{ext}"
                if not new_path.exists():
                    shutil.move(str(old_path), str(new_path))
                    print(f"Migrated {course_id}: {old_path.name} -> {new_path.name}")
                    migrated_count += 1
                    old_image_found = True
                    break
        
        if not old_image_found:
            # Check if already has hero image
            hero_exists = False
            for ext in extensions:
                hero_path = IMAGES_DIR / f"{course_id}_hero{ext}"
                if hero_path.exists():
                    hero_exists = True
                    break
    
    print(f"\nMigration complete. Migrated {migrated_count} images to hero slot.")
    print("Existing courses.json structure is compatible - no JSON changes needed.")

if __name__ == '__main__':
    migrate_images()


