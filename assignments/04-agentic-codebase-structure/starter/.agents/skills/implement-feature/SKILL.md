---
name: implement-feature
description: Implement a Link Shortener feature using a test-first workflow, following repository guidance and verifying API behavior.
---

# Implement Feature — Link Shortener

## Purpose

Use this skill when implementing a feature from `docs/TASKS.md`.

Follow the repository's existing architecture and make the smallest change that satisfies the selected task.

## Workflow

### 1. Read the task and guidance
- Read `docs/TASKS.md` to understand the selected feature.
- Read the root `AGENTS.md`.
- Read `tests/AGENTS.md` before creating or editing tests.

### 2. Inspect the application
- Read `main.py` and the existing `test_main.py`.
- Identify the affected endpoints, data models, and database operations.
- Run the existing tests before making changes.

### 3. State the expected behavior
Before editing, summarize:
- The feature's expected behavior.
- The files that need modification.
- The success and failure cases.
- Any compatibility or implementation risks.

### 4. Write a failing behavioral test
- Add tests inside `tests/`.
- Use FastAPI's `TestClient`.
- Test observable HTTP behavior rather than internal functions.
- Run the new tests and confirm they fail for the expected reason.

### 5. Implement the smallest change
- Modify only the files necessary for the feature.
- Preserve existing endpoints and response formats.
- Avoid unrelated refactoring and unnecessary dependencies.

### 6. Verify the implementation
Run:

```bash
python -m pytest
```

Confirm that both the original tests and the new tests pass.

### 7. Summarize and review
Report:
- What changed and why.
- Which tests were added.
- The final test results.
- Any remaining risks or limitations.

Do not claim completion if tests fail.
