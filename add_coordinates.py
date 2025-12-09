import json
from pathlib import Path

# Coordinate lookup table for common golf course locations
# Format: "City, State/Country" -> (latitude, longitude)
COORDINATE_LOOKUP = {
    # US States - Major Cities
    "Pebble Beach, California": (36.5681, -121.9494),
    "Augusta, Georgia": (33.5030, -82.0199),
    "Pinehurst, North Carolina": (35.1954, -79.4695),
    "Southampton, New York": (40.8843, -72.3895),
    "Oakmont, Pennsylvania": (40.4367, -79.8303),
    "Bandon, Oregon": (43.1187, -124.4085),
    "Newcastle, Northern Ireland": (54.2180, -5.8898),
    "Fishers Island, New York": (41.2647, -72.0294),
    "Mullen, Nebraska": (41.9167, -101.0500),
    "Dornoch, Scotland": (57.8800, -4.0278),
    "Kiawah Island, South Carolina": (32.6083, -80.0806),
    "Ardmore, Pennsylvania": (40.0076, -75.2852),
    "Mamaroneck, New York": (40.9487, -73.7326),
    "Carnoustie, Scotland": (56.5000, -2.7000),
    "Farmingdale, New York": (40.7326, -73.4454),
    "Troon, Scotland": (55.5417, -4.6583),
    "Frankfort, Michigan": (44.6336, -86.2342),
    "Southport, England": (53.6474, -3.0061),
    "East Hampton, New York": (40.9634, -72.1848),
    "Hutchinson, Kansas": (38.0608, -97.9298),
    "Portrush, Northern Ireland": (55.2000, -6.6500),
    "Bernardsville, New Jersey": (40.7182, -74.5693),
    "Gullane, Scotland": (56.0333, -2.8333),
    "Kohler, Wisconsin": (43.7389, -87.7817),
    "Springfield, New Jersey": (40.7045, -74.3171),
    "Wheaton, Illinois": (41.8661, -88.1070),
    "Lytham St. Annes, England": (53.7425, -3.0069),
    "Ridgewood, New Jersey": (40.9793, -74.1165),
    "Turnberry, Scotland": (55.3167, -4.8333),
    "Los Angeles, California": (34.0522, -118.2437),
    "Garden City, New York": (40.7268, -73.6343),
    "Sandwich, England": (51.2787, 1.3385),
    "Bethesda, Maryland": (38.9847, -77.0947),
    "Pacific Palisades, California": (34.0475, -118.5265),
    "Juno Beach, Florida": (26.8798, -80.0534),
    "Hanahan, South Carolina": (32.9185, -80.0220),
    "Orlando, Florida": (28.5383, -81.3792),
    "Chaska, Minnesota": (44.7894, -93.6022),
    "San Francisco, California": (37.7749, -122.4194),
    "Scarsdale, New York": (41.0051, -73.7846),
    "Lake Bluff, Illinois": (42.2792, -87.8348),
    "Chatham, Massachusetts": (41.6812, -69.9597),
    "Erin, Wisconsin": (43.2511, -88.2901),
    "French Lick, Indiana": (38.5489, -86.6200),
    "Hilton Head, South Carolina": (32.2163, -80.7526),
    "Hot Springs, Virginia": (37.9996, -79.8317),
    "Isle of Palms, South Carolina": (32.7868, -79.7940),
    "Kamuela, Hawaii": (20.0200, -155.6694),
    "La Jolla, California": (32.8328, -117.2713),
    "La Quinta, California": (33.6634, -116.3100),
    "Lahaina, Hawaii": (20.8783, -156.6825),
    "Miami, Florida": (25.7617, -80.1918),
    "Myrtle Beach, South Carolina": (33.6891, -78.8867),
    "North Myrtle Beach, South Carolina": (33.8160, -78.6800),
    "Pawleys Island, South Carolina": (33.4352, -79.1278),
    "Ponte Vedra Beach, Florida": (30.2394, -81.3856),
    "Sanford, North Carolina": (35.4799, -79.1803),
    "Scottsdale, Arizona": (33.4942, -111.9261),
    "University Place, Washington": (47.2357, -122.5504),
    "Wailea, Hawaii": (20.6900, -156.4400),
    "Wilmington, North Carolina": (34.2257, -77.9447),
    "Williamsburg, Virginia": (37.2707, -76.7075),
    "White Sulphur Springs, West Virginia": (37.7962, -80.2976),
    "Bridgeport, West Virginia": (39.2865, -80.2562),
    "Boulder City, Nevada": (35.9786, -114.8325),
    "Bowling Green, Florida": (30.6280, -86.7144),
    "Castle Rock, Colorado": (39.3722, -104.8561),
    "Half Moon Bay, California": (37.4636, -122.4286),
    "Indian Wells, California": (33.7175, -116.3400),
    "Mesquite, Nevada": (36.8055, -114.0672),
    "North Las Vegas, Nevada": (36.1989, -115.1175),
    
    # International - Scotland
    "St. Andrews, Scotland": (56.3398, -2.7967),
    "Aberdeen, Scotland": (57.1497, -2.0943),
    
    # International - England
    "Lytham St. Annes, England": (53.7425, -3.0069),
    
    # International - Australia
    "Melbourne, Australia": (-37.8136, 144.9631),
    "Adelaide, Australia": (-34.9285, 138.6007),
    "La Perouse, Australia": (-33.9894, 151.2306),
    
    # International - New Zealand
    "Hawke's Bay, New Zealand": (-39.4928, 176.9120),
    "Mangawhai, New Zealand": (-36.1333, 174.5833),
    "Matauri Bay, New Zealand": (-35.0333, 173.9000),
    
    # International - Spain
    "Sotogrande, Spain": (36.2833, -5.2833),
    "Casares, Spain": (36.4447, -5.2739),
    
    # International - Portugal
    "Cascais, Portugal": (38.6979, -9.4215),
    "Óbidos, Portugal": (39.3611, -9.1572),
    
    # International - France
    "Paris, France": (48.8566, 2.3522),
    "Chantilly, France": (49.1944, 2.4714),
    "Mortefontaine, France": (49.1167, 2.6000),
    
    # International - Japan
    "Kobe, Japan": (34.6901, 135.1956),
    "Osaka, Japan": (34.6937, 135.5023),
    "Saitama, Japan": (35.8617, 139.6455),
    
    # International - South Korea
    "Jeju Island, South Korea": (33.4996, 126.5312),
    
    # International - China
    "Shenzhen, China": (22.5431, 114.0579),
    
    # International - Thailand
    "Pattaya, Thailand": (12.9236, 100.8825),
    "Pathum Thani, Thailand": (14.0208, 100.5253),
    
    # International - South Africa
    "George, South Africa": (-33.9581, 22.4614),
    "Kleinmond, South Africa": (-34.3333, 19.0167),
    "Mpumalanga, South Africa": (-25.5653, 30.5279),
    "Sun City, South Africa": (-25.3307, 27.0967),
    
    # International - Canada
    "Toronto, Canada": (43.6532, -79.3832),
    "Ancaster, Canada": (43.2181, -79.9828),
    "Inverness, Nova Scotia, Canada": (46.2287, -61.3086),
    
    # International - Mexico
    "Playa del Carmen, Mexico": (20.6296, -87.0731),
    
    # International - Dominican Republic
    "Punta Cana, Dominican Republic": (18.5819, -68.3686),
    "Cap Cana, Dominican Republic": (18.5667, -68.3667),
    "La Romana, Dominican Republic": (18.4273, -68.9728),
    
    # Other locations
    "Bridport, Tasmania": (-41.0000, 147.4000),
    "King Island, Tasmania": (-39.8333, 143.8333),
    "Princeville, Hawaii": (22.2167, -159.4833),
}

def get_coordinates(location):
    """Get coordinates for a location string"""
    if not location:
        return None, None
    
    # Try exact match first
    if location in COORDINATE_LOOKUP:
        return COORDINATE_LOOKUP[location]
    
    # Try partial matches for city/state patterns
    location_lower = location.lower()
    
    # Extract city name (first part before comma)
    city = location.split(',')[0].strip() if ',' in location else location
    
    # Try to find by city name in lookup
    for lookup_loc, coords in COORDINATE_LOOKUP.items():
        if city.lower() in lookup_loc.lower() or lookup_loc.lower() in city.lower():
            return coords
    
    # Approximate coordinates by region (fallback)
    if 'california' in location_lower:
        return (36.7783, -119.4179)  # Central California
    elif 'new york' in location_lower:
        return (40.7128, -74.0060)  # New York City
    elif 'florida' in location_lower:
        return (27.7663, -82.6404)  # Central Florida
    elif 'scotland' in location_lower:
        return (56.4907, -4.2026)  # Central Scotland
    elif 'england' in location_lower or 'uk' in location_lower:
        return (51.5074, -0.1278)  # London
    elif 'australia' in location_lower:
        return (-25.2744, 133.7751)  # Central Australia
    elif 'new zealand' in location_lower:
        return (-40.9006, 174.8860)  # Central New Zealand
    elif 'spain' in location_lower:
        return (40.4168, -3.7038)  # Madrid
    elif 'portugal' in location_lower:
        return (38.7223, -9.1393)  # Lisbon
    elif 'france' in location_lower:
        return (48.8566, 2.3522)  # Paris
    elif 'japan' in location_lower:
        return (35.6762, 139.6503)  # Tokyo
    elif 'south korea' in location_lower or 'korea' in location_lower:
        return (37.5665, 126.9780)  # Seoul
    elif 'china' in location_lower:
        return (39.9042, 116.4074)  # Beijing
    elif 'thailand' in location_lower:
        return (13.7563, 100.5018)  # Bangkok
    elif 'south africa' in location_lower or 'africa' in location_lower:
        return (-25.7479, 28.2293)  # Johannesburg
    elif 'canada' in location_lower:
        return (45.5017, -73.5673)  # Montreal
    elif 'mexico' in location_lower:
        return (19.4326, -99.1332)  # Mexico City
    elif 'dominican' in location_lower:
        return (18.4861, -69.9312)  # Santo Domingo
    elif 'hawaii' in location_lower:
        return (21.3099, -157.8581)  # Honolulu
    elif 'nevada' in location_lower:
        return (36.1699, -115.1398)  # Las Vegas
    elif 'arizona' in location_lower:
        return (33.4484, -112.0740)  # Phoenix
    elif 'colorado' in location_lower:
        return (39.7392, -104.9903)  # Denver
    elif 'north carolina' in location_lower:
        return (35.2271, -80.8431)  # Charlotte
    elif 'south carolina' in location_lower:
        return (33.7490, -84.3880)  # Columbia
    elif 'georgia' in location_lower:
        return (33.7490, -84.3880)  # Atlanta
    elif 'pennsylvania' in location_lower:
        return (39.9526, -75.1652)  # Philadelphia
    elif 'new jersey' in location_lower:
        return (40.7178, -74.0431)  # Newark
    elif 'massachusetts' in location_lower:
        return (42.3601, -71.0589)  # Boston
    elif 'virginia' in location_lower:
        return (37.5407, -77.4360)  # Richmond
    elif 'west virginia' in location_lower:
        return (38.3498, -81.6326)  # Charleston
    elif 'wisconsin' in location_lower:
        return (43.0731, -89.4012)  # Madison
    elif 'illinois' in location_lower:
        return (41.8781, -87.6298)  # Chicago
    elif 'minnesota' in location_lower:
        return (44.9778, -93.2650)  # Minneapolis
    elif 'kansas' in location_lower:
        return (39.0473, -95.6752)  # Topeka
    elif 'nebraska' in location_lower:
        return (40.8136, -96.7026)  # Lincoln
    elif 'indiana' in location_lower:
        return (39.7684, -86.1581)  # Indianapolis
    elif 'oregon' in location_lower:
        return (45.5152, -122.6784)  # Portland
    elif 'washington' in location_lower:
        return (47.6062, -122.3321)  # Seattle
    elif 'michigan' in location_lower:
        return (42.3314, -83.0458)  # Detroit
    elif 'maryland' in location_lower:
        return (39.2904, -76.6122)  # Baltimore
    elif 'texas' in location_lower:
        return (30.2672, -97.7431)  # Austin
    
    # Default fallback (center of US)
    return (39.8283, -98.5795)

# Load courses
courses_file = Path(__file__).parent / 'courses.json'
with open(courses_file, 'r', encoding='utf-8') as f:
    courses = json.load(f)

# Add coordinates to each course
updated_count = 0
for course in courses:
    location = course.get('location', '')
    if location and not course.get('latitude') and not course.get('longitude'):
        lat, lng = get_coordinates(location)
        if lat and lng:
            course['latitude'] = lat
            course['longitude'] = lng
            updated_count += 1

# Save updated courses
with open(courses_file, 'w', encoding='utf-8') as f:
    json.dump(courses, f, indent=2, ensure_ascii=False)

print(f"Added coordinates to {updated_count} courses")
print(f"Total courses: {len(courses)}")

# Show sample
print("\nSample coordinates:")
for course in courses[:5]:
    if course.get('latitude') and course.get('longitude'):
        print(f"  {course['name']}: ({course['latitude']}, {course['longitude']})")


