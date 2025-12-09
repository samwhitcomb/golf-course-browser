# Adding Course Descriptions

To add the custom course descriptions to the info button:

1. Make sure your `course description.txt` file is saved with all the descriptions
2. Run the parser script:
   ```bash
   python3 parse_descriptions.py
   ```
3. This will create `course_descriptions.json` with the descriptions mapped to course IDs
4. Restart the Flask server - the descriptions will automatically be included in the API response
5. The info button will now show the custom 2-paragraph descriptions instead of the generated ones

The parser matches course names from the descriptions file to courses in `courses.json` using smart name matching (handles variations like "Royal County Down Golf Club" vs "Royal County Down").


