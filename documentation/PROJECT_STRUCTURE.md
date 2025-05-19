# SpotifEye Project Structure

```
spotifeye/
├── backend/                    # FastAPI backend
│   ├── app/                   # Application package
│   │   ├── api/              # API endpoints
│   │   │   ├── auth.py       # Authentication endpoints
│   │   │   └── spotify.py    # Spotify API endpoints
│   │   ├── core/             # Core functionality
│   │   │   ├── __init__.py
│   │   │   └── config.py     # Configuration management
│   │   ├── services/         # Business logic
│   │   │   └── spotify.py    # Spotify service
│   │   ├── __init__.py
│   │   └── main.py           # Main application logic
│   ├── tests/                # Test suite
│   │   ├── conftest.py       # Test configuration
│   │   ├── requirements-test.txt  # Test dependencies
│   │   ├── test_api.py       # API endpoint tests
│   │   ├── test_config.py    # Configuration tests
│   │   ├── test_spotify.py   # Spotify service tests
│   │   └── test_spotipy_installation.py  # Spotipy setup tests
│   ├── .env                  # Backend environment variables
│   ├── .env.example          # Example environment variables
│   ├── main.py               # Application entry point
│   ├── pyproject.toml        # Python project configuration
│   └── pytest.ini            # Pytest configuration
│
├── documentation/            # Project documentation
│   ├── PIPELINE.md          # Development pipeline
│   └── PROJECT_STRUCTURE.md # This file
│
├── frontend/                  # React frontend
│   ├── public/              # Public assets
│   │   ├── logo.png        # Application logo
│   │   └── vite.svg        # Vite logo
│   ├── src/                  # Source code
│   │   ├── assets/          # Static assets
│   │   │   └── react.svg    # React logo
│   │   ├── components/       # React components
│   │   │   ├── Header.tsx
│   │   │   ├── LoadingScreen.tsx
│   │   │   ├── TopArtists.tsx
│   │   │   ├── TopTracks.tsx
│   │   │   └── UserProfile.tsx
│   │   ├── hooks/           # Custom React hooks
│   │   │   └── useAuth.ts
│   │   ├── pages/           # Page components
│   │   │   └── Callback.tsx # OAuth callback page
│   │   ├── services/        # API services
│   │   │   └── api.ts
│   │   ├── App.tsx          # Main application component
│   │   ├── index.css        # Global styles
│   │   ├── main.tsx         # Application entry point
│   │   └── vite-env.d.ts    # Vite type definitions
│   ├── .gitignore          # Frontend-specific git ignore rules
│   ├── eslint.config.js     # ESLint configuration
│   ├── index.html           # HTML entry point
│   ├── package.json         # NPM package configuration
│   ├── package-lock.json    # NPM package lock file
│   ├── tsconfig.app.json    # App-specific TypeScript config
│   ├── tsconfig.json        # TypeScript configuration
│   ├── tsconfig.node.json   # Node-specific TypeScript config
│   └── vite.config.ts       # Vite configuration
│
├── .gitignore               # Project-wide git ignore rules
├── environment.yml          # Conda environment configuration
├── LICENSE                  # MIT License
└── README.md               # Project overview and setup instructions
```