# SpotifEye: Your Spotify Listening Dashboard

### [***Click this link***](https://spotifeye-chi.vercel.app/) to access the app!
<img width="1470" alt="Screenshot 2025-05-29 at 4 42 28 PM" src="https://github.com/user-attachments/assets/d5780115-01a4-45e8-836d-2ee4e34656e3" />

***Note:*** Deployed website tracks the deployment branch of this repository

## Overview

**SpotifEye** is a full-stack web application that connects to a user's Spotify account and visualizes their listening habits using **FastAPI** (Python) and **React** (TypeScript). The app provides access to top tracks and favorite artists with customizable time ranges, offering insights into your music preferences.

---

## Problem Statement

Spotify offers limited insights beyond basic playback history. Users lack control over timeframe filters and have no way to analyze their listening patterns in detail. Annual features like Spotify Wrapped are fun but not interactive or customizable.

**SpotifEye bridges that gap**, empowering users with:
- Custom timeframe-based stats (4 weeks, 6 months, all time)
- Real-time access to top tracks and artists
- Clean, modern interface for viewing your music preferences

---

## Core Features

### Backend (FastAPI)
- Spotify OAuth 2.0 authentication with secure token management
- REST API endpoints:
  - Fetch top tracks (`/top-tracks`)
  - Fetch top artists (`/top-artists`)
  - Get user profile (`/me`)

### Frontend (React + TypeScript)
- Modern, responsive UI using Mantine
- Secure login with Spotify
- Display of top artists/tracks with three time ranges:
  - Short term (4 weeks)
  - Medium term (6 months)
  - Long term (all time)
- Clean card-based layout for tracks and artists
- Secure session management

---

## Future Scope

### Planned Features
- Audio feature visualizations (danceability, energy, valence, tempo)
- Song recommendations based on listening history
- More detailed artist statistics
- Playlist analysis
- Custom date range selection
- Export functionality for statistics

---

## Tech Stack

| Layer       | Tech                  |
|-------------|------------------------|
| Backend     | FastAPI, Python 3.11   |
| Frontend    | React, TypeScript, Vite|
| UI Library  | Mantine               |
| Auth        | Spotify OAuth 2.0      |
| API Client  | Axios                 |
| Environment | Conda                 |

---

## Getting Started

### Prerequisites
- Python 3.11
- Node.js 18+
- Conda
- Spotify Developer Account

### Backend Setup
1. Clone the repository
2. Create and activate Conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate spotifeye
   ```
3. Set up environment variables in `backend/.env`:
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8000/callback
   SECRET_KEY=your_secret_key
   ```
4. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```

## Documentation

Additional documentation is available in the `documentation/` directory:
- `PIPELINE.md`: Development pipeline and process documentation
- `PROJECT_STRUCTURE.md`: Detailed overview of the project's directory structure and component organization

---

## License

MIT License
