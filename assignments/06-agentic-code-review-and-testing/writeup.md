# Week 6 — AI Code Review & Testing: Habit Tracker

## 1. Project Overview

For this assignment, I extended the provided FastAPI and SQLite Habit Tracker using Google Antigravity as my coding agent and CodeRabbit as my AI pull request reviewer.

I implemented two features on independent Git branches, added automated tests, manually reviewed the generated changes, and submitted separate pull requests to the instructor's repository.

### Pull Requests

**Feature 1 — Validation**

- Branch: `week6-validation`
- PR: https://github.com/scottyUX/Software-engineering-in-the-age-of-ai/pull/248
- Implemented validation for empty or whitespace-only habit names and malformed check-in dates.
- Added automated tests for valid and invalid inputs, including Unicode date edge cases.
- Final verification: 52 tests passed.

**Feature 2 — Streak**

- Branch: `week6-streak`
- PR: https://github.com/scottyUX/Software-engineering-in-the-age-of-ai/pull/249
- Implemented `GET /habits/{habit_id}/streak` to count consecutive check-in days ending today.
- Added deterministic tests for gaps, duplicate check-ins, unknown habits, date boundaries, mixed date representations, and malformed stored dates.
- Final verification: 16 tests passed.

Both PRs include the problem, implementation approach, testing evidence, trade-offs, and AI reviewer feedback.

## 2. Deterministic Guardrails

I used three complementary tools to check the implementation independently of the coding agent.

### Pytest — Functional Correctness

From the Week 6 assignment directory:

```bash
../03-anatomy-of-coding-agents/gemini-cli-dissection/.venv/Scripts/python.exe -m pytest -q starter/
```

Pytest checks whether the application's behavior matches the expected results, including HTTP responses, database isolation, input validation, and streak calculations.

I also demonstrated that pytest detects an intentionally failing test. The failing test caused pytest to report `1 failed, 3 passed`. After removing the demonstration test, the baseline suite returned to `3 passed`.

Final feature test results:

- Validation: 52 passed.
- Streak: 16 passed.

A Starlette/httpx dependency deprecation warning appeared during testing, but it did not cause test failures.

### Black — Consistent Formatting

```bash
../03-anatomy-of-coding-agents/gemini-cli-dissection/.venv/Scripts/python.exe -m black --check starter/main.py starter/test_main.py
```

Black checks whether the Python files follow consistent formatting conventions. It helps prevent unnecessary formatting differences in code reviews.

Final result: both files passed the formatting check.

### Ruff — Static Linting

```bash
../03-anatomy-of-coding-agents/gemini-cli-dissection/.venv/Scripts/python.exe -m ruff check starter/main.py starter/test_main.py
```

Ruff identifies potential code-quality issues such as unused imports and violations of enabled lint rules.

Final result: all checks passed.

These guardrails are deterministic and reproducible, whereas an LLM-based review may identify different issues depending on context.

## 3. Human Review vs. CodeRabbit — Validation

**PR #248:** https://github.com/scottyUX/Software-engineering-in-the-age-of-ai/pull/248

### Findings from My Manual Review

I inspected the AI-generated implementation and tests before committing.

I identified several weaknesses:

1. **Test database isolation:** Tests initially depended on the persistent SQLite database. I requested an isolated temporary database for each test.
2. **Persistence verification:** Tests needed to confirm that rejected inputs were not stored.
3. **Input coverage:** I requested additional tests for missing, null, and non-string payload values.
4. **Exception handling:** I identified an opportunity to improve exception chaining using `raise ... from None`.

These improvements were applied before submitting the pull request.

### Findings from CodeRabbit

CodeRabbit identified additional issues:

1. **Dependency compatibility:** The implementation used Pydantic's `field_validator`, which requires Pydantic 2. The dependency requirements were updated accordingly, including a compatible FastAPI version.
2. **Unicode date matching:** The regular expression used `\d`, which matches Unicode digits beyond ASCII `0–9`. The expression was changed to `[0-9]`, and Unicode regression tests were added.

### Comparison

My manual review was particularly effective at identifying weaknesses in test reliability, database side effects, and input coverage.

CodeRabbit contributed an additional perspective by identifying dependency compatibility and a subtle regular-expression issue.

The Unicode concern overlapped with an edge case considered during human review, but CodeRabbit's concrete feedback helped turn it into an explicit correction and regression tests.

**Conclusion:** Human review and CodeRabbit were complementary. Neither review alone covered every important issue.

## 4. Human Review vs. CodeRabbit — Streak

**PR #249:** https://github.com/scottyUX/Software-engineering-in-the-age-of-ai/pull/249

### Findings from My Manual Review

I reviewed the streak calculation and test suite line by line.

I identified three improvements:

1. **Date underflow:** Subtracting one day from `date.min` could raise `OverflowError`. I requested a boundary check and regression test.
2. **HTTP response assertions:** Some tests created check-ins without verifying the response status. I requested explicit assertions.
3. **Habit isolation:** I requested a test proving that check-ins belonging to one habit do not affect another habit's streak.

I also noted that loading every distinct check-in date into memory is a reasonable simplicity trade-off for a small application but could become inefficient for a much larger history.

The three requested improvements were implemented before the PR was opened.

### Finding from CodeRabbit

CodeRabbit identified a date-representation inconsistency.

The check-in endpoint stored date strings without normalization, while the streak endpoint compared stored values directly against canonical `YYYY-MM-DD` strings.

As a result, a compact ISO date such as `20260925` could represent a valid check-in but would not count toward the streak.

To correct this:

- Valid stored dates were parsed with `date.fromisoformat()`.
- Dates were normalized to canonical `YYYY-MM-DD` strings.
- Malformed stored values were safely ignored.
- Three regression tests were added for compact dates, mixed representations, and malformed dates.

After the correction, all 16 Streak tests passed, and Black and Ruff also passed.

### Comparison

My manual review focused on boundary conditions, test quality, and separation between habits.

CodeRabbit found a representation mismatch that the initial human review had not identified.

The issue was significant because the existing check-in endpoint could accept a date that the streak endpoint would subsequently fail to recognize.

**Conclusion:** CodeRabbit was especially useful for identifying an overlooked interaction between existing API behavior and the new feature. Human review remained essential for assessing the suggested fix and verifying it with tests.

## 5. What I Learned

This assignment showed me that automated tests, formatting checks, and linting provide a reliable first layer of protection, but they cannot guarantee that every requirement or edge case has been considered. Manual review helped me evaluate the agent's implementation critically, particularly its test design, database isolation, and boundary conditions. CodeRabbit added value by identifying compatibility and data-representation problems that were not fully covered by my initial review. I am comfortable using AI review as an additional source of feedback, but I would not trust its suggestions without understanding the reasoning, checking their relevance, and independently verifying the resulting changes.

## 6. Final Submission

**GitHub repository:** https://github.com/Kaan-Cal/AI-Augmented-Software-Engineering

**Validation PR:** https://github.com/scottyUX/Software-engineering-in-the-age-of-ai/pull/248

**Streak PR:** https://github.com/scottyUX/Software-engineering-in-the-age-of-ai/pull/249

**AI coding agent:** Google Antigravity

**AI pull request reviewer:** CodeRabbit

Both required features were implemented on separate branches, reviewed manually and with CodeRabbit, and verified using Pytest, Black, and Ruff.