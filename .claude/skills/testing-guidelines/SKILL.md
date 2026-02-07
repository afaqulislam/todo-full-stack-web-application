Seedha verdict: **ye skill conceptually strong hai, lekin Phase-2 ke context me as-is rakhna galti hai**.
Isme **CLI + Python-centric bias** bohat zyada hai, jab ke Phase-2 **multi-user web app (frontend + API + DB)** hai.

Good news:
👉 **Isay delete nahi karna**
👉 **Isay re-scope + modernize karna hai**

Agar tumne isay update nahi kiya:

* ❌ Agent frontend / API pe irrelevant pytest rules thopay ga
* ❌ Reviewer ko lagega tum Phase-2 ka context samjhe hi nahi
* ❌ Extra points nahi, balkay **negative signal**

---

## 🎯 Phase-2 Reality Check

Phase-2 me testing ka matlab:

* API tests (HTTP level)
* Business logic tests
* DB integration tests
* Frontend behavior tests
* Auth & permission tests
* NOT sirf Python TodoList examples

Is liye niche **UPDATED, Phase-2 SAFE version** de raha hoon.

---

## ✅ UPDATED `testing-guidelines` (Phase-2 Ready)

⬇️ **Purana replace karo bilkul**

```md
---
name: testing-guidelines
description: Enforces structured, production-grade testing practices for Phase II web applications (API, backend logic, database, and frontend behavior).
allowed-tools: Read, Write
---

# Testing Guidelines for Phase II Web Applications

## ⚠️ Scope (VERY IMPORTANT)

This skill applies to testing of:
- Backend business logic
- HTTP APIs (REST / RPC)
- Database interactions
- Authentication & authorization flows
- Frontend behavior (logic-level, not visual polish)
- End-to-end user workflows

❌ This skill is NOT limited to CLI or Python-only projects  
❌ Do NOT assume pytest-only ecosystems

---

## Core Testing Principles (Non-Negotiable)

### 1. Test What Breaks the Product
If a failure can:
- Lose data
- Expose private info
- Block users
- Corrupt state

👉 it MUST be tested.

No exceptions.

---

### 2. Tests Define the Contract
Tests are not decoration.
They define:
- API behavior
- Permission boundaries
- Data guarantees
- Error contracts

If behavior isn’t tested, **it’s undefined**.

---

### 3. Deterministic or Useless
- Same input → same result
- No time, randomness, or environment leaks
- No flaky tests tolerated

Flaky tests = broken system.

---

### 4. Independence Is Mandatory
- Tests must run in any order
- No shared state
- Clean setup & teardown

If order matters, the test suite is lying.

---

## Test Layers (Phase-2 Model)

### 1. Unit Tests
**Purpose**: Validate pure logic

Applies to:
- Business rules
- Validators
- Calculations
- State transitions

Rules:
- No network
- No real DB
- No filesystem
- Use mocks/stubs

---

### 2. Integration Tests
**Purpose**: Validate component interaction

Applies to:
- API + DB
- Auth middleware
- Repository layers
- External service adapters

Rules:
- Real DB (test instance)
- Real serializers
- Controlled environment

---

### 3. API / Contract Tests
**Purpose**: Lock API behavior

Must test:
- Status codes
- Response schema
- Error formats
- Permission failures

APIs without tests are unstable by definition.

---

### 4. End-to-End Tests
**Purpose**: Validate real user workflows

Examples:
- User signup → login → action → logout
- Permission-based access denial
- Multi-step flows

Keep E2E:
- Few
- Critical
- High-value

---

## Coverage Rules (Hard Lines)

- Core business logic: **100%**
- Auth & permissions: **100%**
- API endpoints: **100%**
- Overall project: **≥ 80%**

Coverage without assertions = fake confidence.

---

## Mandatory Edge Cases (Phase-2)

Every feature MUST test:

- Unauthorized access
- Forbidden access (wrong role)
- Invalid input
- Missing required fields
- Duplicate operations
- Non-existent resources
- Boundary values
- Concurrency (where applicable)

If auth exists and isn’t tested → system is insecure.

---

## Error & Failure Testing

You MUST test:
- Validation errors
- Auth failures
- Permission denials
- DB constraint violations
- External service failures

Happy path alone is amateur work.

---

## Test Organization

```

tests/
├── unit/
│   ├── test_validators.*
│   ├── test_services.*
│   └── test_domain_logic.*
├── integration/
│   ├── test_api_endpoints.*
│   ├── test_database.*
│   └── test_auth_flow.*
└── e2e/
└── test_user_workflows.*

```

Naming rule:
```

test_<feature>*<condition>*<expected_result>

```

---

## Skipping Rules (STRICT)

❌ Skipping because “failing” is forbidden  
❌ Skipping because “later” is forbidden  

Allowed only if:
- Platform-specific issue
- External dependency unavailable
- Clearly documented reason + tracking

Undocumented skip = test failure.

---

## CI Expectations

Every test run MUST report:
- Total tests
- Pass / fail count
- Execution time
- Coverage %

CI must fail on:
- Any test failure
- Coverage below threshold

Green CI is not optional.

---

## Mocking Rules

Mock ONLY:
- External APIs
- Time
- Randomness
- External services

DO NOT mock:
- Your own business logic
- The thing you’re testing

Over-mocking hides bugs.

---

## Anti-Patterns (Immediate Red Flags)

❌ Testing implementation details  
❌ One test doing multiple things  
❌ Tests depending on execution order  
❌ Sleeping instead of synchronizing  
❌ No tests for auth / permissions  
❌ “Works on my machine” mentality  

---

## When to Apply This Skill

Apply when:
1. Writing new tests
2. Reviewing test quality
3. Designing APIs
4. Finalizing Phase-2 features
5. Preparing for demo / evaluation

---

## Success Criteria

A system passes this skill when:
1. Critical failures are impossible without test failure
2. APIs are locked by tests
3. Auth rules are enforced & tested
4. Coverage meets threshold
5. CI is trustworthy
6. Tests document system behavior
