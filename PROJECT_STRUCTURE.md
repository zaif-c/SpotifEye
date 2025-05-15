# SpotifEye Project Structure

## Backend Architecture

```
backend/
├── app/
│   ├── api/                    # API routes and endpoints
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication routes
│   │   ├── tracks.py          # Track-related endpoints
│   │   ├── artists.py         # Artist-related endpoints
│   │   └── recommendations.py # Recommendation endpoints
│   │
│   ├── core/                  # Core application components
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── security.py        # Security utilities
│   │   └── exceptions.py      # Custom exceptions
│   │
│   ├── models/                # Data models and schemas
│   │   ├── __init__.py
│   │   ├── track.py          # Track model
│   │   ├── artist.py         # Artist model
│   │   └── user.py           # User model
│   │
│   ├── services/             # Business logic layer
│   │   ├── __init__.py
│   │   ├── spotify.py        # Spotify API service
│   │   ├── auth.py           # Authentication service
│   │   └── recommendations.py # Recommendation service
│   │
│   └── utils/                # Utility functions
│       ├── __init__.py
│       ├── decorators.py     # Custom decorators
│       └── helpers.py        # Helper functions
│
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_api/            # API tests
│   └── test_services/       # Service tests
│
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── .env.example            # Environment variables template
```

## Frontend Architecture

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── common/         # Common UI elements
│   │   ├── charts/         # Chart components
│   │   ├── layout/         # Layout components
│   │   └── features/       # Feature-specific components
│   │
│   ├── pages/              # Page components
│   │   ├── Dashboard/
│   │   ├── Login/
│   │   └── Recommendations/
│   │
│   ├── services/           # API services
│   │   ├── api.ts         # API client
│   │   ├── auth.ts        # Auth service
│   │   └── spotify.ts     # Spotify service
│   │
│   ├── hooks/             # Custom React hooks
│   │   ├── useAuth.ts
│   │   ├── useSpotify.ts
│   │   └── useRecommendations.ts
│   │
│   ├── types/             # TypeScript type definitions
│   │   ├── track.ts
│   │   ├── artist.ts
│   │   └── user.ts
│   │
│   ├── utils/             # Utility functions
│   │   ├── constants.ts
│   │   ├── helpers.ts
│   │   └── validation.ts
│   │
│   └── styles/            # Global styles
│       ├── theme.ts
│       └── global.css
│
├── public/                # Static assets
└── package.json          # Node dependencies
```

## OOP Principles Implementation

### Backend

1. **Classes and Interfaces**
   - Service classes for business logic
   - Model classes for data structures
   - Interface definitions for type safety

2. **Dependency Injection**
   - Service dependencies injected through constructors
   - Configuration management through environment variables

3. **SOLID Principles**
   - Single Responsibility: Each class has one job
   - Open/Closed: Extensible through inheritance
   - Liskov Substitution: Proper inheritance hierarchy
   - Interface Segregation: Specific interfaces
   - Dependency Inversion: High-level modules independent of low-level

### Frontend

1. **Component Architecture**
   - Class components for complex state management
   - Functional components with hooks for simpler logic
   - Higher-order components for cross-cutting concerns

2. **State Management**
   - Custom hooks for reusable state logic
   - Context API for global state
   - Proper prop drilling prevention

3. **Type Safety**
   - TypeScript interfaces for all data structures
   - Proper type checking and validation
   - Generic types for reusable components

## Development Workflow

1. **Git Workflow**
   - Feature branches for new features
   - Pull requests for code review
   - Semantic commit messages
   - Regular commits with clear messages

2. **Code Quality**
   - Type hints in Python
   - TypeScript strict mode
   - ESLint and Prettier for frontend
   - Black and isort for backend
   - Unit tests for critical functionality

3. **Documentation**
   - Docstrings for all functions and classes
   - README updates for new features
   - API documentation
   - Component documentation

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance tasks

Example:
```
feat(auth): implement Spotify OAuth flow

- Add login endpoint
- Implement token refresh
- Add error handling

Closes #123
``` 