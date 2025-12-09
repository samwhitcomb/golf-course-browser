# Golf Course Image Scraper

A web application that scrapes Google Images to download relevant images for golf courses and provides a UI to view and regenerate images.

## Features

- Automatically searches Google Images for each golf course
- Downloads and stores images locally
- Beautiful UI to view all courses and their images
- Regenerate images for any course if the current image is incorrect
- Batch download for all courses without images

## Setup

### Backend (Python)

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend (React)

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. Start both the backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. View all courses - those with images will display them
4. Click "Download Image" for courses without images
5. Click "Regenerate Image" to get a new image for any course
6. Use "Download All" to batch download images for all courses without images

## Image Storage

Images are saved in the `images/` directory with filenames matching the course ID (e.g., `pebble-beach.jpg`).

## Notes

- The Google Images scraping uses a simple web scraping approach. For production use, consider using a more robust solution like SerpAPI or Google Custom Search API.
- Rate limiting is implemented to avoid overwhelming Google's servers.
- Images are cached locally - regenerating will replace the existing image.

