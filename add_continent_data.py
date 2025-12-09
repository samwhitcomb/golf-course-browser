import json
from pathlib import Path

# Load courses
courses_file = Path(__file__).parent / 'courses.json'
with open(courses_file, 'r', encoding='utf-8') as f:
    courses = json.load(f)

# Continent mapping based on location
def get_continent(location):
    location_lower = location.lower()
    
    # North America
    if any(x in location_lower for x in ['united states', 'usa', 'california', 'new york', 'florida', 'texas', 'nevada', 'arizona', 'oregon', 'washington', 'north carolina', 'georgia', 'pennsylvania', 'new jersey', 'illinois', 'colorado', 'south carolina', 'hawaii', 'wisconsin', 'minnesota', 'michigan', 'massachusetts', 'vermont', 'kansas', 'missouri', 'louisiana', 'mississippi', 'alabama', 'tennessee', 'kentucky', 'virginia', 'maryland', 'delaware', 'connecticut', 'rhode island', 'new hampshire', 'maine', 'utah', 'idaho', 'montana', 'wyoming', 'north dakota', 'south dakota', 'nebraska', 'iowa', 'oklahoma', 'arkansas', 'west virginia', 'ohio', 'indiana']):
        return 'North America'
    
    # Canada
    if any(x in location_lower for x in ['canada', 'ontario', 'quebec', 'british columbia', 'alberta', 'manitoba', 'saskatchewan', 'nova scotia', 'new brunswick', 'newfoundland', 'prince edward island', 'yukon', 'northwest territories', 'nunavut']):
        return 'North America'
    
    # Europe
    if any(x in location_lower for x in ['scotland', 'england', 'ireland', 'northern ireland', 'wales', 'uk', 'united kingdom', 'spain', 'france', 'italy', 'germany', 'portugal', 'sweden', 'norway', 'denmark', 'netherlands', 'belgium', 'switzerland', 'austria', 'greece', 'poland', 'czech', 'hungary', 'romania', 'bulgaria', 'croatia', 'serbia', 'slovenia', 'slovakia', 'finland', 'iceland', 'estonia', 'latvia', 'lithuania', 'luxembourg', 'malta', 'cyprus']):
        return 'Europe'
    
    # Asia
    if any(x in location_lower for x in ['china', 'japan', 'south korea', 'north korea', 'india', 'thailand', 'singapore', 'malaysia', 'indonesia', 'philippines', 'vietnam', 'cambodia', 'myanmar', 'laos', 'bangladesh', 'sri lanka', 'pakistan', 'afghanistan', 'nepal', 'bhutan', 'maldives', 'mongolia', 'taiwan', 'hong kong', 'macau']):
        return 'Asia'
    
    # Oceania
    if any(x in location_lower for x in ['australia', 'new zealand', 'fiji', 'papua new guinea', 'samoa', 'tonga', 'vanuatu', 'solomon islands', 'new caledonia', 'french polynesia', 'cook islands']):
        return 'Oceania'
    
    # South America
    if any(x in location_lower for x in ['brazil', 'argentina', 'chile', 'colombia', 'peru', 'venezuela', 'ecuador', 'bolivia', 'paraguay', 'uruguay', 'guyana', 'suriname', 'french guiana']):
        return 'South America'
    
    # Africa
    if any(x in location_lower for x in ['south africa', 'kenya', 'egypt', 'morocco', 'tunisia', 'zimbabwe', 'botswana', 'namibia', 'mozambique', 'madagascar', 'mauritius', 'seychelles', 'ghana', 'nigeria', 'senegal', 'ivory coast', 'cameroon', 'uganda', 'tanzania', 'ethiopia', 'algeria', 'libya', 'sudan', 'angola', 'zambia', 'malawi', 'rwanda', 'burundi']):
        return 'Africa'
    
    # Middle East
    if any(x in location_lower for x in ['uae', 'united arab emirates', 'dubai', 'abu dhabi', 'saudi arabia', 'qatar', 'bahrain', 'kuwait', 'oman', 'jordan', 'lebanon', 'israel', 'turkey', 'iran', 'iraq', 'syria', 'yemen']):
        return 'Middle East'
    
    # Central America / Caribbean
    if any(x in location_lower for x in ['mexico', 'dominican republic', 'puerto rico', 'jamaica', 'bahamas', 'barbados', 'trinidad', 'cuba', 'costa rica', 'panama', 'belize', 'guatemala', 'honduras', 'nicaragua', 'el salvador', 'haiti', 'cayman islands', 'bermuda', 'aruba', 'curaçao', 'bonaire']):
        return 'North America'  # Grouping with North America
    
    return 'Unknown'

# Add continent to each course
for course in courses:
    if not course.get('continent'):
        continent = get_continent(course.get('location', ''))
        course['continent'] = continent

# Save updated courses
with open(courses_file, 'w', encoding='utf-8') as f:
    json.dump(courses, f, indent=2, ensure_ascii=False)

# Print summary
from collections import Counter
continent_counts = Counter(c.get('continent') for c in courses)
print(f"Added continent data to {len(courses)} courses")
print(f"\nContinent distribution:")
for continent, count in sorted(continent_counts.items()):
    print(f"  {continent}: {count} courses")


