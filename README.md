# PocketSmart AI

A complete FastAPI + Jinja2 + SQLite + Gemini budget recommendation assistant based on the supplied project document.

## What is included
- Home Interior, Party and Jewelry planners
- Registration, login, logout and JWT cookie authentication
- Recommendation history
- Optional jewelry outfit image upload
- Gemini multimodal integration when `GEMINI_API_KEY` is configured
- Deterministic fallback catalog when Gemini is unavailable
- Responsive frontend
- Health endpoint and automated smoke tests

## Important implementation note
The source document names Gemini 1.5 Flash Pro and several third-party shopping/service APIs. Those model/API details are not treated as live integrations. The app uses a configurable current Gemini model and a built-in catalog with outbound search/platform links. It does not scrape or claim live inventory, prices, ratings, or availability.

## VS Code setup
1. Install Python 3.11+.
2. Open this folder in VS Code.
3. Create a terminal and run:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`.
6. Optional AI: put your Gemini API key in `GEMINI_API_KEY`. The app works without it using fallback recommendations.
7. Start: `uvicorn app.main:app --reload`
8. Open http://127.0.0.1:8000

## Test
Run `pytest -q`.
Open http://127.0.0.1:8000/docs for the interactive API documentation.

## API
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/session-info`
- `POST /api/generate-home`
- `POST /api/generate-party`
- `POST /api/generate-jewelry`
- `GET /api/history`
- `GET /health`

## Gemini
The code uses the official `google-genai` SDK and the configurable `GEMINI_MODEL`, defaulting to `gemini-3.8-flash`. Jewelry image input is passed as a multimodal request. If Gemini fails or no key is configured, fallback recommendations are returned instead of crashing the application.
