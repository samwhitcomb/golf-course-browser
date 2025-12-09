# GitHub Pages Deployment Guide

## Quick Deploy

### Option 1: Deploy from dist folder (Recommended)

1. **Build the project:**
   ```bash
   npm run build
   ```

2. **Deploy the dist folder:**
   - Go to your GitHub repository
   - Navigate to Settings → Pages
   - Under "Source", select "Deploy from a branch"
   - Choose the branch (usually `main` or `master`)
   - Set the folder to `/dist`
   - Click Save

3. **Alternative: Use gh-pages branch**
   ```bash
   # Install gh-pages if needed
   npm install --save-dev gh-pages
   
   # Add to package.json scripts:
   # "deploy": "npm run build && gh-pages -d dist"
   
   # Then deploy:
   npm run deploy
   ```

### Option 2: GitHub Actions (Automatic)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build
        run: npm run build
        
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

## Important Notes

- The app uses **HashRouter**, so URLs will be:
  - `https://yourusername.github.io/repo-name/#/`
  - `https://yourusername.github.io/repo-name/#/presentation`

- All assets are static:
  - Images: `/images/...`
  - Videos: `/videos/...`
  - Data: `/courses.json`

- No backend required - everything is static!

## Troubleshooting

If you see 404 errors:
1. Make sure the repository name matches in GitHub Pages settings
2. Check that all files in `dist/` are committed
3. Verify the build completed successfully

## Testing Locally

Before deploying, test the production build:
```bash
npm run build
npm run preview
```

Then visit `http://localhost:4173` to verify everything works.

