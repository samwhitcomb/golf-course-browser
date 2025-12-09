# Local Preview Guide

## Quick Preview (Production Build)

To preview the site exactly as it will appear on GitHub Pages:

```bash
npm run build
npm run preview
```

Then visit: `http://localhost:4173/golf-course-browser/#/`

## Development Mode (No Base Path)

For faster development without the base path:

1. Temporarily change `vite.config.js`:
   ```js
   base: '/',  // Change from '/golf-course-browser/'
   ```

2. Run dev server:
   ```bash
   npm run dev
   ```

3. Visit: `http://localhost:3000/#/`

**Remember to change it back to `/golf-course-browser/` before pushing to GitHub!**

## Check Descriptions

To see which courses are missing descriptions:

```bash
python3 check_descriptions.py
```

## Update Courses JSON for Static Site

After making changes to `courses.json`, regenerate the public version:

```bash
python3 update_courses_for_static.py
```

This will update `public/courses.json` with image paths.

