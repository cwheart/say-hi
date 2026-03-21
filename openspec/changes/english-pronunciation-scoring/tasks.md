## 1. Project Scaffolding

- [x] 1.1 Create Vue.js 3 frontend project with Vite and TypeScript (`frontend/`)
- [x] 1.2 Create Python FastAPI backend project structure (`backend/`)
- [x] 1.3 Create backend `requirements.txt` with dependencies (fastapi, uvicorn, openai-whisper, python-Levenshtein, python-multipart, python-dotenv, ffmpeg-python)
- [x] 1.4 Create `.env.example` with configurable variables (WHISPER_MODEL, CORS_ORIGINS, etc.)
- [x] 1.5 Create project root `README.md` with setup instructions, prerequisites (ffmpeg, Python 3.9+, Node.js 18+)

## 2. Backend Core Setup

- [x] 2.1 Implement FastAPI application entry point (`backend/app/main.py`) with CORS middleware and lifespan events
- [x] 2.2 Implement Whisper service (`backend/app/services/whisper_service.py`) - model loading at startup, transcription method with language="en"
- [x] 2.3 Implement audio conversion utility - ffmpeg-based WebM/OGG to WAV conversion (`backend/app/services/audio_service.py`)
- [x] 2.4 Implement health check endpoint (`/api/health`) returning model status

## 3. Pronunciation Scoring Engine

- [x] 3.1 Implement text normalization utility - lowercase, strip punctuation, trim whitespace (`backend/app/services/text_utils.py`)
- [x] 3.2 Implement word-level alignment using Levenshtein distance (`backend/app/services/scoring_service.py`)
- [x] 3.3 Implement multi-dimension scoring (accuracy, completeness, fluency) and overall score calculation
- [x] 3.4 Implement evaluation response model with word comparison array (`backend/app/models/evaluation.py`)

## 4. Backend API Routes

- [x] 4.1 Implement `/api/evaluate` POST endpoint - accept audio file + target text, return scoring result (`backend/app/routers/evaluate.py`)
- [x] 4.2 Implement `/api/practices` GET endpoint with category and difficulty filtering (`backend/app/routers/practices.py`)
- [x] 4.3 Implement `/api/practices/{id}` GET endpoint
- [x] 4.4 Create practice seed data JSON file with 30+ items across all categories and difficulty levels (`backend/app/data/practices.json`)
- [x] 4.5 Implement practice data loading service (`backend/app/services/practice_service.py`)

## 5. Frontend Core Setup

- [x] 5.1 Configure Vite proxy for backend API (`frontend/vite.config.ts`)
- [x] 5.2 Define TypeScript types for API responses - EvaluationResult, Practice, WordComparison (`frontend/src/types/`)
- [x] 5.3 Implement API client composable (`frontend/src/composables/useApi.ts`)

## 6. Frontend Audio Recording

- [x] 6.1 Implement audio recording composable with MediaRecorder API (`frontend/src/composables/useAudioRecorder.ts`) - start, stop, playback, re-record, 30s time limit
- [x] 6.2 Implement browser compatibility detection for MediaRecorder API
- [x] 6.3 Create AudioRecorder component with record/stop/play/re-record buttons and timer display (`frontend/src/components/AudioRecorder.vue`)

## 7. Frontend Practice & Evaluation Views

- [x] 7.1 Create PracticeList view - display practice items grouped by category/difficulty (`frontend/src/views/PracticeList.vue`)
- [x] 7.2 Create PracticeDetail view - show target text, audio recorder, and submit button (`frontend/src/views/PracticeDetail.vue`)
- [x] 7.3 Implement Vue Router with routes for practice list and practice detail

## 8. Frontend Feedback Display

- [x] 8.1 Create ScoreDashboard component - overall score with color-coded indicator, dimension scores, level label (`frontend/src/components/ScoreDashboard.vue`)
- [x] 8.2 Create WordComparison component - word-by-word colored comparison view (`frontend/src/components/WordComparison.vue`)
- [x] 8.3 Create EvaluationResult view integrating ScoreDashboard, WordComparison, and "Try Again" button (`frontend/src/components/EvaluationResult.vue`)
- [x] 8.4 Implement loading state with spinner during evaluation

## 9. UI Polish & Integration

- [x] 9.1 Create App layout with navigation header and responsive design
- [x] 9.2 Add global CSS styles - modern, clean design with consistent color scheme
- [x] 9.3 Add unsupported browser warning component
- [x] 9.4 End-to-end integration testing - record audio, submit, view results
