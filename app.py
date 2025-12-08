import os
import json
import re
import requests
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import urllib.parse
import time
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Configuration
BASE_DIR = Path(__file__).parent
COURSES_FILE = BASE_DIR / 'courses.json'
IMAGES_DIR = BASE_DIR / 'images'

# Ensure images directory exists
os.makedirs(IMAGES_DIR, exist_ok=True)


def json_error(message, status=400, detail=None):
    """Consistent JSON error responses."""
    payload = {'error': message}
    if detail:
        payload['detail'] = detail
    return jsonify(payload), status

def load_courses():
    """Load courses from JSON file, resilient to cwd changes"""
    try:
        with open(COURSES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"courses.json not found at {COURSES_FILE}")
        return []

def get_image_path(course_id, slot='hero', extension='.jpg'):
    """
    Get the path to an image for a course
    slot can be 'hero', '1', or '2'
    """
    if slot == 'hero':
        return IMAGES_DIR / f"{course_id}_hero{extension}"
    else:
        return IMAGES_DIR / f"{course_id}_{slot}{extension}"

def find_image_paths(course_id):
    """
    Find all existing images for a course (hero, 1, 2)
    Returns dict with 'hero', '1', '2' keys containing (path, extension) or None
    """
    images = {'hero': None, '1': None, '2': None}
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    for slot in ['hero', '1', '2']:
        for ext in extensions:
            path = get_image_path(course_id, slot, ext)
            if path.exists():
                images[slot] = (path, ext)
                break
    
    return images

def search_google_images(query, num_images=1):
    """
    Search Google Images and return image URLs
    Uses a more robust scraping approach with multiple fallbacks
    """
    try:
        # Encode the search query
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded_query}&tbm=isch&tbs=isz:m"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        image_urls = []
        
        # Method 1: Try to extract from data attributes and script tags
        # Google Images embeds image data in various ways
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # Look for image URLs in the script content
                # Pattern to find image URLs in JSON-like structures
                url_patterns = [
                    r'"ou":"([^"]+)"',  # Original URL pattern
                    r'"ow":\d+,"oh":\d+,"ou":"([^"]+)"',  # With dimensions
                    r'https?://[^\s"<>]+\.(?:jpg|jpeg|png|gif|webp)',
                ]
                
                for pattern in url_patterns:
                    matches = re.findall(pattern, script.string, re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):
                            match = match[0] if match else ''
                        if match and match.startswith('http'):
                            # Allow gstatic/googleusercontent because they often host actual images
                            if match not in image_urls:
                                image_urls.append(match)
                                if len(image_urls) >= num_images * 3:  # Get more candidates
                                    break
                    if len(image_urls) >= num_images * 3:
                        break
                if len(image_urls) >= num_images * 3:
                    break
        
        # Method 2: Find img tags with data attributes
        if len(image_urls) < num_images:
            img_tags = soup.find_all('img', {'data-src': True})
            for img in img_tags:
                src = img.get('data-src') or img.get('src')
                if src:
                    if src.startswith('data:image'):
                        continue
                    if src.startswith('//'):
                        src = 'https:' + src
                    if src.startswith('http') and src not in image_urls:
                        # Filter out small icons and logos
                        if 'icon' not in src.lower() and 'logo' not in src.lower():
                            image_urls.append(src)
                            if len(image_urls) >= num_images * 3:
                                break
        
        # Method 3: Fallback to regular img tags
        if len(image_urls) < num_images:
            img_tags = soup.find_all('img')
            for img in img_tags:
                src = img.get('src')
                if src and (src.startswith('http') or src.startswith('//')):
                    if src.startswith('//'):
                        src = 'https:' + src
                    # Filter out obvious small icons/logos, but allow gstatic/googleusercontent
                    if 'icon' not in src.lower() and 'logo' not in src.lower():
                        if src not in image_urls:
                            image_urls.append(src)
                            if len(image_urls) >= num_images * 3:
                                break
        
        # Return the requested number of images
        return image_urls[:num_images * 3] if image_urls else []
    
    except Exception as e:
        print(f"Error searching Google Images: {e}")
        return []

def download_image(url, filepath, header_variants=None):
    """Download an image from a URL and save it. Returns (success, actual_filepath, error_message)"""
    # Build header attempts
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    attempts = header_variants or [default_headers]

    last_err = None
    for hdrs in attempts:
        try:
            headers = default_headers.copy()
            headers.update(hdrs)
            response = requests.get(url, headers=headers, timeout=15, stream=True, allow_redirects=True)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            if 'image' not in content_type:
                last_err = f"Content-Type not image: {content_type}"
                continue
            
            extension = '.jpg'
            if 'png' in content_type:
                extension = '.png'
            elif 'gif' in content_type:
                extension = '.gif'
            elif 'webp' in content_type:
                extension = '.webp'
            elif url.lower().endswith(('.png', '.gif', '.webp', '.jpeg')):
                url_ext = Path(url).suffix.lower()
                if url_ext:
                    extension = url_ext
            
            actual_filepath = filepath
            if extension != filepath.suffix:
                actual_filepath = filepath.with_suffix(extension)
            
            with open(actual_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            if actual_filepath.exists() and actual_filepath.stat().st_size > 0:
                return (True, actual_filepath, None)
            else:
                if actual_filepath.exists():
                    actual_filepath.unlink()
                last_err = "Empty file"
        except Exception as e:
            print(f"Error downloading image from {url}: {e}")
            last_err = str(e)
            if filepath.exists():
                try:
                    filepath.unlink()
                except:
                    pass
            continue

    return (False, None, last_err)

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

@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Get all courses with their image status"""
    courses = load_courses()
    descriptions = load_descriptions()
    
    # Add image status and descriptions to each course
    for course in courses:
        # Check for images in all slots
        image_paths = find_image_paths(course['id'])
        
        # Build images object
        images = {
            'hero': None,
            'additional': []
        }
        
        # Hero image
        if image_paths['hero']:
            path, ext = image_paths['hero']
            images['hero'] = f"/api/images/{path.name}"
        
        # Additional images
        for slot in ['1', '2']:
            if image_paths[slot]:
                path, ext = image_paths[slot]
                images['additional'].append(f"/api/images/{path.name}")
        
        course['images'] = images
        
        # Backward compatibility: set hasImage and imageUrl from hero
        course['hasImage'] = images['hero'] is not None
        course['imageUrl'] = images['hero']
        
        # Add descriptions if available
        if course['id'] in descriptions:
            course['blurb'] = descriptions[course['id']]
    
    return jsonify(courses)

@app.route('/api/images/<filename>', methods=['GET'])
def get_image(filename):
    """Serve images from the images directory"""
    # Support various image extensions
    image_path = IMAGES_DIR / filename
    if not image_path.exists():
        # Try different extensions
        base_name = Path(filename).stem
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            alt_path = IMAGES_DIR / f"{base_name}{ext}"
            if alt_path.exists():
                return send_from_directory(IMAGES_DIR, alt_path.name)
        return jsonify({'error': 'Image not found'}), 404
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/api/search-images/<course_id>', methods=['GET'])
def search_images(course_id):
    """Return a list of candidate image URLs for a course without downloading"""
    limit = int(request.args.get('limit', 20))  # Default to 20 instead of 6
    courses = load_courses()
    course = next((c for c in courses if c['id'] == course_id), None)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    search_query = f"{course['name']} {course['location']} golf course"
    # Search for more images to ensure we have enough unique ones
    image_urls = search_google_images(search_query, num_images=limit * 2)  # Get more to filter duplicates
    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for url in image_urls:
        if url not in seen:
            seen.add(url)
            deduped.append(url)
        if len(deduped) >= limit:
            break

    return jsonify({'results': [{'url': u, 'thumb': u} for u in deduped]})

@app.route('/api/download-image/<course_id>', methods=['POST'])
@app.route('/api/download-image/<course_id>/<slot>', methods=['POST'])
def download_course_image(course_id, slot='hero'):
    """Download image for a specific course and slot (hero, 1, or 2), ensuring uniqueness"""
    try:
        if slot not in ['hero', '1', '2']:
            return json_error('Invalid slot. Must be hero, 1, or 2', 400)
        
        courses = load_courses()
        course = next((c for c in courses if c['id'] == course_id), None)
        
        if not course:
            return json_error('Course not found', 404)
        
        # Get existing images to check for duplicates
        image_paths = find_image_paths(course_id)
        existing_hashes = []
        for path_tuple in image_paths.values():
            if path_tuple:
                path, _ = path_tuple
                img_hash = get_image_hash(path)
                if img_hash:
                    existing_hashes.append(img_hash)
        
        # Create search query from course name and location
        search_query = f"{course['name']} {course['location']} golf course"
        
        # Search for more images to ensure we can find a unique one
        image_urls = search_google_images(search_query, num_images=15)
        
        if not image_urls:
            return json_error('No images found', 404)
        
        # Try to download a unique image
        # Start with .jpg extension, download_image will adjust if needed
        image_path = get_image_path(course_id, slot, '.jpg')
        success = False
        actual_filepath = None
        
        error_msg = None
        for url in image_urls:
            # Try with Google referer, then domain referer, then blank referer
            parsed = urllib.parse.urlparse(url)
            domain_referer = f"{parsed.scheme}://{parsed.netloc}/" if parsed.scheme and parsed.netloc else ''
            header_variants = [
                {},  # default headers include Google referer
                {'Referer': domain_referer} if domain_referer else {},
                {'Referer': ''},
            ]
            success, actual_filepath, err = download_image(url, image_path, header_variants=header_variants)
            
            if success and actual_filepath:
                # Check if this image is different from existing ones
                new_hash = get_image_hash(actual_filepath)
                if new_hash and new_hash not in existing_hashes:
                    # Unique image, we're done
                    break
                else:
                    # Duplicate image, delete it and try next
                    if actual_filepath.exists():
                        actual_filepath.unlink()
                    success = False
                    actual_filepath = None
            
            error_msg = err
            time.sleep(0.5)  # Small delay between attempts
        
        if success and actual_filepath:
            return jsonify({
                'success': True,
                'message': 'Image downloaded successfully',
                'imageUrl': f"/api/images/{actual_filepath.name}",
                'slot': slot
            })
        else:
            return json_error('Failed to download unique image', 500, error_msg or 'Could not find a unique image')
    except Exception as e:
        return json_error('Unexpected server error', 500, str(e))

@app.route('/api/download-from-url/<course_id>', methods=['POST'])
def download_from_url(course_id):
    """Download a specific URL for a course (used by picker)"""
    try:
        data = request.get_json(silent=True) or {}
        url = data.get('url')
        slot = data.get('slot', 'hero')  # Default to hero if not specified
        
        if not url:
            return json_error('Missing url', 400)
        if url.startswith('data:image'):
            return json_error('Cannot download inline data images', 400)
        if slot not in ['hero', '1', '2']:
            return json_error('Invalid slot. Must be hero, 1, or 2', 400)

        courses = load_courses()
        course = next((c for c in courses if c['id'] == course_id), None)
        if not course:
            return json_error('Course not found', 404)

        image_path = get_image_path(course_id, slot, '.jpg')
        # Try with Google referer, then domain referer, then blank referer
        parsed = urllib.parse.urlparse(url)
        domain_referer = f"{parsed.scheme}://{parsed.netloc}/" if parsed.scheme and parsed.netloc else ''
        header_variants = [
            {},  # default headers include Google referer
            {'Referer': domain_referer} if domain_referer else {},
            {'Referer': ''},
        ]
        success, actual_filepath, err = download_image(url, image_path, header_variants=header_variants)

        if success and actual_filepath:
            return jsonify({
                'success': True,
                'message': 'Image downloaded successfully',
                'imageUrl': f"/api/images/{actual_filepath.name}",
                'slot': slot
            })
        return json_error('Failed to download image', 500, err)
    except Exception as e:
        return json_error('Unexpected server error', 500, str(e))

@app.route('/api/regenerate-image/<course_id>', methods=['POST'])
@app.route('/api/regenerate-image/<course_id>/<slot>', methods=['POST'])
def regenerate_image(course_id, slot='hero'):
    """Regenerate (re-download) image for a course and specific slot"""
    if slot not in ['hero', '1', '2']:
        return json_error('Invalid slot. Must be hero, 1, or 2', 400)
    
    # Delete existing image for this slot if it exists (try all extensions)
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        image_path = get_image_path(course_id, slot, ext)
        if image_path.exists():
            image_path.unlink()
    
    # Download new image
    return download_course_image(course_id, slot)

@app.route('/api/download-all', methods=['POST'])
def download_all_images():
    """Download images for all courses that don't have images yet"""
    courses = load_courses()
    results = []
    
    for course in courses:
        # Check if image already exists with any extension
        has_image = False
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            if get_image_path(course['id'], 'hero', ext).exists():
                has_image = True
                break
        
        if not has_image:
            search_query = f"{course['name']} {course['location']} golf course"
            image_urls = search_google_images(search_query, num_images=5)
            
            success = False
            image_path = get_image_path(course['id'], 'hero', '.jpg')
            for url in image_urls:
                success, _, _ = download_image(url, image_path)
                if success:
                    break
                time.sleep(0.5)
            
            results.append({
                'courseId': course['id'],
                'courseName': course['name'],
                'success': success
            })
            
            time.sleep(1)  # Rate limiting
    
    return jsonify(results)

def get_image_hash(filepath):
    """Get a simple hash of image file for comparison"""
    try:
        import hashlib
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def images_are_different(image_paths):
    """Check if all existing images are different"""
    existing_paths = [path for path in image_paths.values() if path]
    if len(existing_paths) < 2:
        return True  # Not enough images to compare
    
    hashes = []
    for path_tuple in existing_paths:
        path, _ = path_tuple
        img_hash = get_image_hash(path)
        if img_hash:
            if img_hash in hashes:
                return False  # Duplicate found
            hashes.append(img_hash)
    
    return True  # All images are different

@app.route('/api/download-secondary-images', methods=['POST'])
def download_secondary_images():
    """Download secondary images (slots 1 and 2) for all courses that have hero images"""
    courses = load_courses()
    results = []
    
    for course in courses:
        # Check if hero image exists
        has_hero = False
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            if get_image_path(course['id'], 'hero', ext).exists():
                has_hero = True
                break
        
        if not has_hero:
            continue  # Skip courses without hero images
        
        # Check which secondary slots need images
        image_paths = find_image_paths(course['id'])
        slots_to_download = []
        
        if not image_paths['1']:
            slots_to_download.append('1')
        if not image_paths['2']:
            slots_to_download.append('2')
        
        if not slots_to_download:
            # Check if existing images are different, if not, regenerate
            if not images_are_different(image_paths):
                # Find which images are duplicates and regenerate them
                existing_paths = {k: v for k, v in image_paths.items() if v}
                hashes = {}
                duplicates = []
                
                for slot, path_tuple in existing_paths.items():
                    path, _ = path_tuple
                    img_hash = get_image_hash(path)
                    if img_hash:
                        if img_hash in hashes.values():
                            # This is a duplicate
                            duplicates.append(slot)
                        else:
                            hashes[slot] = img_hash
                
                # Regenerate duplicate images
                for dup_slot in duplicates:
                    slots_to_download.append(dup_slot)
                    # Delete the duplicate
                    path, ext = image_paths[dup_slot]
                    if path.exists():
                        path.unlink()
            
            if not slots_to_download:
                continue  # All images exist and are different
        
        # Search for more images to ensure we have enough unique ones
        search_query = f"{course['name']} {course['location']} golf course"
        image_urls = search_google_images(search_query, num_images=20)
        
        # Download images for missing slots, ensuring uniqueness
        slot_results = {}
        url_index = 0
        downloaded_hashes = []
        
        # Get hashes of existing images to avoid duplicates
        for slot, path_tuple in image_paths.items():
            if path_tuple:
                path, _ = path_tuple
                img_hash = get_image_hash(path)
                if img_hash:
                    downloaded_hashes.append(img_hash)
        
        for slot in slots_to_download:
            success = False
            image_path = get_image_path(course['id'], slot, '.jpg')
            attempts = 0
            max_attempts = min(15, len(image_urls))  # Try up to 15 URLs
            
            # Try to download from available URLs, ensuring uniqueness
            for i in range(url_index, min(url_index + max_attempts, len(image_urls))):
                url = image_urls[i]
                success, actual_filepath, _ = download_image(url, image_path)
                
                if success and actual_filepath:
                    # Check if this image is different from existing ones
                    new_hash = get_image_hash(actual_filepath)
                    if new_hash and new_hash not in downloaded_hashes:
                        downloaded_hashes.append(new_hash)
                        url_index = i + 1
                        break
                    else:
                        # Duplicate image, delete it and try next
                        if actual_filepath.exists():
                            actual_filepath.unlink()
                        success = False
                        attempts += 1
                        if attempts >= max_attempts:
                            break
                else:
                    attempts += 1
                    if attempts >= max_attempts:
                        break
                time.sleep(0.5)
            
            slot_results[slot] = success
        
        results.append({
            'courseId': course['id'],
            'courseName': course['name'],
            'slot1': slot_results.get('1', False),
            'slot2': slot_results.get('2', False)
        })
        
        time.sleep(1)  # Rate limiting
    
    return jsonify(results)

@app.route('/api/video/<filename>', methods=['GET'])
def get_video(filename):
    """Serve video files"""
    try:
        # Try to find video in root directory first
        video_path = BASE_DIR / filename
        if video_path.exists() and video_path.suffix.lower() == '.mp4':
            return send_from_directory(BASE_DIR, filename)
        
        # Try Videos directory (uppercase)
        videos_dir = BASE_DIR / 'Videos'
        if videos_dir.exists():
            video_path = videos_dir / filename
            if video_path.exists():
                return send_from_directory(videos_dir, filename)
        
        # Try videos directory (lowercase)
        videos_dir = BASE_DIR / 'videos'
        if videos_dir.exists():
            video_path = videos_dir / filename
            if video_path.exists():
                return send_from_directory(videos_dir, filename)
        
        return json_error('Video not found', 404)
    except Exception as e:
        return json_error(f"Error serving video: {e}", 500)

@app.route('/api/set-hero-image/<course_id>/<slot>', methods=['POST'])
def set_hero_image(course_id, slot):
    """Set which image slot should be the hero image"""
    try:
        if slot not in ['hero', '1', '2']:
            return json_error('Invalid slot. Must be hero, 1, or 2', 400)
        
        if slot == 'hero':
            return jsonify({'success': True, 'message': 'Hero is already the hero image'})
        
        # Find existing images
        image_paths = find_image_paths(course_id)
        
        if not image_paths[slot]:
            return json_error(f'No image found in slot {slot}', 404)
        
        # Get the image from the specified slot
        source_path, source_ext = image_paths[slot]
        
        # Check if hero image exists
        hero_path = None
        if image_paths['hero']:
            hero_path, _ = image_paths['hero']
        
        # Copy source image to hero (or move if hero doesn't exist)
        import shutil
        new_hero_path = get_image_path(course_id, 'hero', source_ext)
        
        if hero_path and hero_path.exists():
            # Swap: move hero to the source slot
            old_hero_slot_path = get_image_path(course_id, slot, hero_path.suffix)
            shutil.move(str(hero_path), str(old_hero_slot_path))
        
        # Move source to hero
        shutil.move(str(source_path), str(new_hero_path))
        
        return jsonify({
            'success': True,
            'message': f'Image from slot {slot} is now the hero image',
            'imageUrl': f"/api/images/{new_hero_path.name}"
        })
    except Exception as e:
        return json_error(f"Error setting hero image: {e}", 500)

@app.route('/api/update-course/<course_id>', methods=['POST'])
def update_course(course_id):
    """Update course data (e.g., description/blurb)"""
    try:
        data = request.get_json()
        if not data:
            return json_error('No data provided', 400)
        
        courses = load_courses()
        course = next((c for c in courses if c.get('id') == course_id), None)
        
        if not course:
            return json_error('Course not found', 404)
        
        # Update allowed fields
        if 'blurb' in data:
            course['blurb'] = data['blurb']
        if 'description' in data:
            course['description'] = data['description']
        
        # Save updated courses
        with open(COURSES_FILE, 'w', encoding='utf-8') as f:
            json.dump(courses, f, indent=2, ensure_ascii=False)
        
        return jsonify({'success': True, 'course': course})
    except Exception as e:
        return json_error(f"Error updating course: {e}", 500)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", "5001"))
    app.run(debug=True, host="0.0.0.0", port=port)

