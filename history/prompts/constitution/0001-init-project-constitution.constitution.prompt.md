---
id: 1
title: Initialize project constitution
stage: constitution
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: default
command: sp.constitution
labels: [constitution, project-init, security, architecture]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
tests:
  - N/A
---

## Prompt

Project: Phase II – Todo Full-Stack Web Application

You are building a spec-driven, production-grade full-stack web application using GitHub Spec-Kit Plus and Claude Code.

Strict Rules:
1. NO manual coding assumptions — everything must be derived from specs.
2. Follow Spec-Kit structure strictly.
3. Backend: FastAPI + SQLModel + Neon PostgreSQL only.
4. Frontend: Next.js App Router + TypeScript + Tailwind only.
5. Authentication MUST use Better Auth on frontend with JWT verification on backend.
6. All API routes MUST be protected via JWT.
7. Every task operation MUST be user-scoped (no cross-user access).
8. Code must be modular, readable, and production-ready.
9. Security is NOT optional — enforce ownership checks everywhere.
10. Tests are mandatory for backend logic.

Failure Conditions:
- Any endpoint allowing cross-user access is a critical failure.
- Any missing JWT validation is a critical failure.
- Any undocumented behavior is unacceptable.

Optimization Goals:
- Clean architecture
- Clear se

## Response snapshot

I have initialized the project constitution at `.specify/memory/constitution.md` based on your strict rules and optimization goals. The constitution defines core principles including SDD mandate, the FastAPI/Next.js tech stack, JWT security requirements, and user-scoped data isolation. I also updated the `plan-template.md` to include a Constitution Check gate aligned with these new principles.

## Outcome

- ✅ Impact: Established ground truth for project architecture and security.
- 🧪 Tests: N/A
- 📁 Files: Updated constitution.md and plan-template.md.
- 🔁 Next prompts: /sp.specify for the first feature.
- 🧠 Reflection: The user provided clear constraints which simplified the derivation of principles.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
