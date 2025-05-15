# SpotifEye: Your Spotify Listening Dashboard

## Overview

**SpotifEye** is a full-stack web application that connects to a user's Spotify account and visualizes their listening habits using **FastAPI** (Python) and **React** (JavaScript). The app provides real-time access to top tracks, favorite artists, and detailed audio feature breakdowns such as energy, danceability, and mood — insights not available in Spotify's native app.

---

## Problem Statement

Spotify offers limited insights beyond basic playback history. Users lack control over timeframe filters and have no way to analyze track characteristics (e.g., energy, mood, tempo). Annual features like Spotify Wrapped are fun but not actionable or interactive.

**SpotifEye bridges that gap**, empowering users with:
- Custom timeframe-based stats
- Audio feature visualizations
- Real-time, interactive data from their listening history

---

## Core Features

### Backend (FastAPI)
- Spotify OAuth 2.0 authentication (access + refresh token flow)
- REST API endpoints to:
  - Fetch top tracks (`/top-tracks`)
  - Fetch top artists (`/top-artists`)
  - Retrieve audio features of tracks (`/audio-features`)
  - Get song recommendations (`/recommendations`) - Optional

### Frontend (React)
- Login with Spotify
- Display of top artists/tracks (short, medium, long term)
- Interactive bar or radar charts showing:
- Danceability, energy, valence, tempo, etc.
- Song recommendations display (Optional)

---

## Project Pipeline

#### 1. Project Initialization (1 hour)
- Set up project structure
- Initialize FastAPI backend with essential dependencies
- Create React frontend using Vite
- Set up environment variables

#### 2. Spotify Integration (2-3 hours)
- Register app in Spotify Developer Dashboard
- Implement OAuth flow
- Set up token management
- Test authentication flow

#### 3. Core Backend API (3-4 hours)
- Implement essential endpoints:
  - `/top-tracks`
  - `/top-artists`
  - `/audio-features`
- Add basic error handling
- Test endpoints with Postman

#### 4. Basic Frontend Structure (2 hours)
- Set up routing
- Create login page
- Implement basic dashboard layout
- Add Spotify authentication flow

### Day 2: Frontend and Polish (8-10 hours)

#### 1. Data Visualization (3-4 hours)
- Implement charts for audio features
- Create track/artist display components
- Add time range selector
- Style components

#### 2. Recommendations Feature (2-3 hours)
- If time permits, implement:
  - `/recommendations` endpoint
  - Recommendation display component
  - Basic recommendation logic

#### 3. Polish and Testing (2-3 hours)
- Add error handling
- Implement loading states
- Test on different devices
- Fix any bugs

#### 4. Deployment (1 hour)
- Deploy backend to Render
- Deploy frontend to Vercel
- Set up environment variables
- Test deployed version

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
