Seedha bolta hoon: **ye skill Phase-2 me almost useless hai agar as-is rakhi**.
Reason? Phase-2 **web app hai**, CLI product nahi. Is form me:

- ❌ Agent isay galat jagah apply karega
- ❌ Web APIs / frontend flows pe irrelevant rules enforce hongi
- ❌ Bonus ke bajaye **confusion create hogi**

Lekin — **delete karna bhi ghalat hoga**.
Sahi move: **scope tighten + Phase-2 compatible rewrite**.

---

## 🔥 Final Decision (No BS)

- ❌ Pure CLI-focused skill = **NOT Phase-2 ready**
- ✅ CLI standards **sirf internal dev tools / scripts** ke liye allowed
- ✅ Skill ko **restrict + modernize** karna zaroori

Is liye main tumhe **UPDATED & SAFE version** de raha hoon jo:

- Phase-2 me break nahi karega
- Galat agents pe apply nahi hoga
- Internal tooling ke kaam bhi aaega

---

## ✅ UPDATED `cli-app-standards` (Phase-2 Compatible)

⬇️ **Isay purana replace karo**

```md
---
name: cli-app-standards
description: Enforces strict, professional standards for INTERNAL CLI TOOLS and DEVELOPER UTILITIES used alongside Phase II web applications. NOT for end-user web features.
allowed-tools: Read, Write
---

# CLI Standards for Internal Developer Tools (Phase II)

## ⚠️ Scope Limitation (CRITICAL)

This skill applies ONLY to:

- Internal developer tools
- Local scripts
- Admin utilities
- Migration / seed / debug CLIs
- One-off maintenance commands

❌ This skill MUST NOT be applied to:

- User-facing web applications
- Frontend UI behavior
- Public APIs
- Authentication logic
- Business logic meant for HTTP services

If the system being built is:

- Next.js frontend → ❌ DO NOT APPLY
- FastAPI HTTP API → ❌ DO NOT APPLY
- Internal script (`scripts/`, `tools/`) → ✅ APPLY

---

## Purpose

To ensure all internal CLI tools used during Phase-2 development are:

- Predictable
- Scriptable
- Safe
- Non-destructive by default
- Developer-friendly

---

## Core Principles

1. CLI tools are **supporting utilities**, not primary products
2. They must never bypass security rules of the web system
3. They must never modify production data silently
4. They must be explicit, verbose when needed, and safe by default

---

## Command Structure
```

tool [global-options] command [command-options] [arguments]

```

### Naming Rules
- Verb-first commands: `seed`, `migrate`, `inspect`, `reset`
- Consistent vocabulary across all tools
- Avoid clever or abbreviated commands

✅ `db migrate`
❌ `dbfix`

---

## Safety Rules (NON-NEGOTIABLE)

### Destructive Commands
Any destructive command MUST:
- Require explicit confirmation
- Support `--dry-run`
- Print affected resources before execution

Example:
```

db reset --dry-run
db reset --confirm

```

❌ Silent deletion is forbidden

---

## Argument & Flag Standards

### Required Flags
- `--env` for environment (dev / staging / prod)
- `--dry-run` for destructive operations
- `--yes` or `--confirm` to bypass prompts

### Reserved Flags
- `-h / --help`
- `-v / --verbose`
- `--json`
- `--no-color`

---

## Output Rules

### Default Output
- Human-readable
- Minimal
- Clear success/failure indicator

### JSON Output
When `--json` is passed:
- Output MUST be valid JSON only
- No logs or decorations
- Suitable for scripting

---

## Error Handling

- Errors go to `stderr`
- Exit codes MUST be meaningful
- Error messages MUST explain:
  - What failed
  - Why
  - How to fix

---

## Environment Safety

- Production operations must be explicitly acknowledged
- Tool must display current environment clearly
- Never assume environment implicitly

Example:
```

Environment: PRODUCTION
⚠️ This operation will affect live data

```

---

## Forbidden Behaviors

❌ Modifying DB without `--env`
❌ Auto-detecting prod silently
❌ Bypassing auth rules of the main system
❌ Hardcoding secrets
❌ Running irreversible commands without confirmation
❌ Acting differently based on “guessing” context

---

## Usage Rules

Apply this skill ONLY when:
1. Creating migration tools
2. Writing seed scripts
3. Building admin/debug CLIs
4. Managing local/dev infra
5. Supporting Phase-2 development workflows

DO NOT apply during:
- API design
- UI development
- Auth system implementation
- Business logic coding

---

## Success Criteria

A CLI tool is acceptable when:
1. It cannot accidentally damage production
2. Its output is script-friendly
3. It respects environment boundaries
4. It follows predictable conventions
5. A new developer can use it without docs

