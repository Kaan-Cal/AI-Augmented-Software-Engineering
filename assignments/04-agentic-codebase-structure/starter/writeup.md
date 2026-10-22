# Week 4 — Agent-Ready Link Shortener: Writeup

## 1. Repository-Wide Agent Instructions

I created `AGENTS.md` in the Link Shortener's `starter/` directory to provide consistent guidance for coding agents. It describes the FastAPI and SQLite application, important files, setup commands, testing procedures, and product boundaries. I included a seven-step development process emphasizing understanding requirements, writing behavioral tests, implementing minimal changes, and verifying results. These instructions apply repository-wide because they establish general expectations for every feature, regardless of which files an agent modifies.

## 2. Scoped Instructions

I created `tests/AGENTS.md` to provide additional guidance specifically for files inside the `tests/` directory. It requires testing through FastAPI's public API using `TestClient`, checking successful and unsuccessful requests, and maintaining test independence. This guidance is scoped because testing conventions do not need to govern every application file. The original `test_main.py` remains outside this scope, while the new `tests/test_alias.py` follows these instructions.

## 3. Reusable Agent Workflow

I implemented a reusable skill at `.agents/skills/implement-feature/SKILL.md`. Its seven steps are reading task requirements and instructions, inspecting application code, stating expected behavior, writing failing tests, implementing the smallest change, running tests, and summarizing results. This workflow promotes test-first development and can be reused for future Link Shortener features.

## 4. Agent Discovery and Invocation

I used Gemini CLI version 0.64.0. Initially, the skill was not discovered because its Markdown file contained an invisible blank line before the YAML frontmatter. After removing that line, `gemini skills list` identified `implement-feature` as enabled. I then explicitly instructed Gemini to use the skill during implementation. This demonstrated the importance of correct skill formatting and verifying discovery rather than assuming an instruction file is automatically recognized.

## 5. Planning, Implementation, and Review

I selected Task 1, Custom Alias. During the planning stage, Gemini inspected the existing API and proposed an optional alias field, HTTP 409 responses for duplicate aliases, and behavioral tests without editing files. The plan also identified reserved routes and collisions with automatically generated codes.

During implementation, Gemini modified `main.py` and created `tests/test_alias.py`. The final suite reported eight passing tests, including the three original tests. In a separate read-only review, Gemini returned `ACCEPT`, finding no critical or major issues. It identified unrestricted alias characters as a minor limitation, but no revision was required.

## 6. Lessons Learned

This assignment showed me that agent-ready repositories require more than working code. Clear global instructions establish consistent expectations, scoped instructions provide relevant local guidance, and reusable skills make development processes repeatable. Separating planning, implementation, and review also improves traceability and encourages more critical evaluation. Finally, troubleshooting skill discovery taught me to validate configuration and tool behavior before relying on automation.