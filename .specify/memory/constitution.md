<!--
  Sync Impact Report:
  - Version change: 0.0.0 → 1.0.0 (Initial project setup)
  - List of modified principles:
      - [PRINCIPLE_1_NAME] → I. Spec-Driven Development (SDD) Rule
      - [PRINCIPLE_2_NAME] → II. Modern Tech Stack (FastAPI/Next.js)
      - [PRINCIPLE_3_NAME] → III. JWT-Based Authentication & Security
      - [PRINCIPLE_4_NAME] → IV. User-Scoped Data Isolation
      - [PRINCIPLE_5_NAME] → V. Production-Ready Modular Code
      - [PRINCIPLE_6_NAME] → VI. Backend Test Commitment
  - Added sections:
      - Security Requirements
      - Development Workflow
  - Templates requiring updates:
      - .specify/templates/plan-template.md (✅ updated)
      - .specify/templates/spec-template.md (✅ updated)
      - .specify/templates/tasks-template.md (✅ updated)
  - Follow-up TODOs:
      - TODO(RATIFICATION_DATE): Finalize launch date.
-->

# Phase II – Todo Full-Stack Web Application Constitution

## Core Principles

### I. Spec-Driven Development (SDD) Rule
NO manual coding assumptions are permitted. Every implementation detail, API contract, and business rule MUST be derived from finalized specifications. If an requirement is missing, it must be clarified in the spec before code is written.

### II. Modern Tech Stack (FastAPI/Next.js)
The application architecture is strictly bounded by:
- **Backend**: FastAPI + SQLModel + Neon PostgreSQL.
- **Frontend**: Next.js App Router + TypeScript + Tailwind CSS.
- Abstractions must align with these framework patterns.

### III. JWT-Based Authentication & Security
Authentication MUST use Better Auth on the frontend with JWT verification on the backend. Security is non-negotiable; all API routes (except public auth entries) MUST be protected via JWT validation.

### IV. User-Scoped Data Isolation
Every data operation MUST be user-scoped. Cross-user access is a critical failure. Ownership checks must be enforced at the database/service layer for every request.

### V. Production-Ready Modular Code
Code must be modular, highly readable, and project-structured for scalability. Avoid monolithic files; prefer service-oriented patterns and clear separation of concerns between models, schemas, and logic.

### VI. Backend Test Commitment
Tests are mandatory for all backend logic. No backend feature is considered "done" without corresponding unit or integration tests that verify success and error paths.

## Security Requirements

- **Ownership Integrity**: Every SQL query filtering by ID must also filter by `user_id`.
- **Secret Management**: Never hardcode tokens or credentials; use `.env` files and environment variables exclusively.
- **Input Validation**: All external input must be validated via Pydantic/Zod schemas at the system boundary.

## Development Workflow

1. **Spec**: Define feature and acceptance criteria.
2. **Plan**: Design architecture and data models.
3. **Tasks**: Break into testable, prioritized increments.
4. **Implement**: Write code and mandatory backend tests.
5. **Review**: Ensure compliance with this constitution.

## Governance

This constitution supersedes all other informal practices. Amendments require a version bump and updates to all dependent templates. Compliance is checked during the planning phase of every feature.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2026-01-06
