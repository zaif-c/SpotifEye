# SpotifEye: Your Spotify Listening Dashboard

## Overview

**SpotifEye** is a full-stack web application that connects to a user's Spotify account and visualizes their listening habits using **FastAPI** (Python) and **React** (JavaScript). The app provides real-time access to top tracks, favorite artists, and detailed audio feature breakdowns such as energy, danceability, and mood — insights not available in Spotify’s native app.

---

## Problem Statement

Spotify offers limited insights beyond basic playback history. Users lack control over timeframe filters and have no way to analyze track characteristics (e.g., energy, mood, tempo). Annual features like Spotify Wrapped are fun but not actionable or interactive.

**SpotifEye bridges that gap**, empowering users with:
- Custom timeframe-based stats
- Audio feature visualizations
- Real-time, interactive data from their listening history

---

## MVP Features

### Backend (FastAPI)
- Spotify OAuth 2.0 authentication (access + refresh token flow)
- REST API endpoints to:
  - Fetch top tracks (`/top-tracks`)
  - Fetch top artists (`/top-artists`)
  - Retrieve audio features of tracks (`/audio-features`)

### Frontend (React)
- Login with Spotify
- Display of top artists/tracks (short, medium, long term)
- Interactive bar or radar charts showing:
  - Danceability, energy, valence, tempo, etc.

---

## Project Pipeline

Below is the full development pipeline for **SpotifEye**, organized into logical stages from setup to deployment. This outlines both the MVP flow and leaves room for iterative feature additions.

---

### 1. Project Setup

#### Backend (FastAPI)
- Initialize a virtual environment
- Install core dependencies: `fastapi`, `uvicorn`, `requests`, `python-dotenv`, `httpx`, `pydantic`
- Create `.env` file for environment variables:
  - `SPOTIFY_CLIENT_ID`
  - `SPOTIFY_CLIENT_SECRET`
  - `REDIRECT_URI`
- Scaffold FastAPI project structure (`main.py`, `auth.py`, `spotify.py`, etc.)

#### Frontend (React)
- Create app using `Vite` or `create-react-app`
- Install dependencies: `axios`, `react-router-dom`, `chart.js` or `recharts`
- Setup base components and routing

---

### 2. Spotify OAuth Integration

- Register app in [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- Implement authorization code flow:
  - `/login` → Redirect to Spotify login
  - `/callback` → Exchange auth code for access + refresh token
  - `/refresh_token` → Regenerate token as needed
- Store tokens in memory (or secure session) for demo purposes

---

### 3. Backend API Endpoints

- `/top-tracks?time_range=short_term|medium_term|long_term`
- `/top-artists?time_range=...`
- `/audio-features?track_ids=id1,id2,...`

Each route:
- Sends authorized requests to Spotify’s Web API
- Parses and returns relevant data (JSON-serializable)

---

### 4. Data Processing (Server-Side)

- Extract core metrics:
  - Artist/track names
  - Popularity scores
  - Album images
- Fetch and normalize audio features:
  - `valence`, `danceability`, `energy`, `tempo`, `speechiness`, etc.

---

### 5. Frontend Integration

- **Login Page**: Link to `/login` to start Spotify auth
- **Dashboard Page**:
  - Display top tracks and artists (cards or lists)
  - Add time range selector (e.g., buttons/tabs)
- **Charts**:
  - Radar or bar chart for audio features
  - Optional: per-track or aggregated view

---

### 6. Testing

- Manual testing of each backend route with Postman
- Frontend integration testing with fake/mock API responses
- Test time range handling, API limits, and edge cases

---

### 7. Deployment

- **Frontend**: Vercel or Netlify
- **Backend**: Render, Fly.io, or Railway
- Set up environment variables securely on each platform
- CORS configuration to allow frontend → backend API calls

---

### Deliverables

- [x] Spotify OAuth login (with refresh)
- [x] API integration for top tracks, artists, audio features
- [x] React frontend with list + chart visualizations
- [x] Responsive, minimal UI
- [x] Deployment-ready structure

---

## Future Scope

- **Smart Recommendations**: Suggest new music based on top tracks
- **Custom Tags**: Let users label songs (e.g., "study", "party") and filter
- **AI Vibe Summary**: Use LLM to summarize the user’s vibe from track stats
- **Friend Compare**: Compare musical compatibility between users
- **Persistent Storage**: Save stats over time with PostgreSQL
- **Responsive Design**: Full support for mobile and tablet viewports

---

## Tech Stack

| Layer       | Tech                  |
|-------------|------------------------|
| Backend     | FastAPI, Python, httpx |
| Frontend    | React, Vite, Axios     |
| Visualization | Recharts / Chart.js  |
| Auth        | Spotify OAuth 2.0      |
| Deployment  | Vercel + Render        |

---

## License

MIT License
