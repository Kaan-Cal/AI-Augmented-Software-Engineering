
# Agent Guide — Link Shortener

## Project Overview
This repository contains a small URL-shortening REST API built with FastAPI, Pydantic, and SQLite.

Users can create shortened links with `POST /shorten` and visit them through `GET /{code}`, which returns an HTTP 307 redirect.

Keep the service small, understandable, and easy to test.

## Important Files
- `main.py` — API endpoints, URL validation, Base62 encoding, and SQLite access.
- `test_main.py` — existing API behavior tests.
- `docs/TASKS.md` — available feature requirements.
- `requirements.txt` — Python dependencies.
- `README.md` — setup and usage instructions.
- `AGENTS.md` — repository-wide agent guidance.
- `tests/AGENTS.md` — scoped guidance for tests.
- `.agents/skills/implement-feature/SKILL.md` — reusable feature workflow.

## Setup and Commands
Install dependencies:
`python -m pip install -r requirements.txt`

Run tests:
`python -m pytest`

Start the application:
`python -m uvicorn main:app --reload`

Interactive API documentation:
`http://localhost:8000/docs`

## Product Boundaries
- Keep the application focused on URL shortening and related link management.
- Use the existing FastAPI and SQLite architecture.
- Do not introduce authentication, analytics services, or external databases unless explicitly required.
- Preserve existing endpoint behavior and HTTP status codes.
- Prefer small changes over unnecessary abstractions.

## Change Workflow
1. Understand the selected task and inspect relevant files.
2. Run the existing tests before editing.
3. Plan the expected behavior and affected files.
4. Add a failing behavioral test.
5. Implement the smallest working change.
6. Run all tests and review the final diff.
7. Summarize the changes, results, and remaining risks.

## Testing Expectations
- Test through the public API using FastAPI's `TestClient`.
- Include successful requests and failure or edge cases.
- Keep tests independent of execution order.
- Follow `tests/AGENTS.md` when working on tests in `tests/`.
