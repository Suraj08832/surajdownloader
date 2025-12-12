# YouTube Music API

## Overview
A comprehensive REST API for YouTube Music, similar to JioSaavn API. Provides endpoints for searching, fetching songs, albums, artists, playlists, lyrics, and more.

## API Endpoints

### Search
- `GET /api/search?q=<query>&limit=<num>` - Search all content types
- `GET /api/search/songs?q=<query>&limit=<num>` - Search songs
- `GET /api/search/albums?q=<query>&limit=<num>` - Search albums
- `GET /api/search/artists?q=<query>&limit=<num>` - Search artists
- `GET /api/search/playlists?q=<query>&limit=<num>` - Search playlists
- `GET /api/search/videos?q=<query>&limit=<num>` - Search videos

### Songs
- `GET /api/songs/<id>` - Get song details with download URLs
- `GET /api/songs/<id>/download` - Get download URLs only
- `GET /api/songs/<id>/lyrics` - Get song lyrics

### Albums
- `GET /api/albums/<id>` - Get album with all tracks

### Artists
- `GET /api/artists/<id>` - Get artist info, top songs, albums, singles, videos

### Playlists
- `GET /api/playlists/<id>` - Get playlist with all tracks

### Watch/Radio
- `GET /api/watch/<videoId>` - Get related songs/radio playlist

## Response Format
All responses follow this structure:
```json
{
  "success": true,
  "data": { ... }
}
```

## Project Structure
- `main.py` - Flask REST API server
- `ytmusicapi/` - YouTube Music API library source

## Running the Project
Run `python main.py` to start the Flask API server on port 5000.

## Vercel Deployment
This project is configured for Vercel deployment:

1. Push to GitHub
2. Import project in Vercel
3. Deploy automatically

**Files for Vercel:**
- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function entry point
- `requirements.txt` - Python dependencies

## Dependencies
- Python 3.10+
- Flask
- ytmusicapi
- requests
