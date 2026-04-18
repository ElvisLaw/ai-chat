---
name: integrated-ai-dev-workflow
description: Unified workflow combining Superpowers + OpenSpec + Everything-Claude-Code
version: 1.0.0
---

# Integrated AI Development Workflow

Combines Superpowers (methodology), OpenSpec (specification), and Everything-Claude-Code (execution).

## Workflow Stages

### Stage 1: Ideation → Superpowers
**Command:** `Superpowers:brainstorming`

When to use:
- New feature request arrives
- Unclear if feature is worth building
- Need to evaluate trade-offs before committing

Output: Clear decision to proceed or not, with rationale

---

### Stage 2: Specification → OpenSpec
**Command:** `/opsx:propose "feature-name"`

When to use:
- Decision made to proceed with implementation
- Need to document what/why/how before writing code

Creates:
```
openspec/changes/[feature-name]/
├── proposal.md    # Why we're doing this
├── specs/         # Requirements and scenarios
├── design.md      # Technical approach
└── tasks.md       # Implementation checklist
```

---

### Stage 3: Implementation → ECC
**Commands:**
- `ECC:feature-dev` — Main implementation
- `ECC:code-review` — Quality check
- `ECC:security-review` — Security audit

When to use:
- Spec is defined and approved
- Ready to write code

---

### Stage 4: Completion → OpenSpec
**Command:** `/opsx:archive`

When to use:
- All tasks completed
- Code reviewed and merged
- Ready to clean up

---

## Decision Tree

```
New idea arrives
    │
    ▼
Superpowers:brainstorming
    │
    ├── "Don't do it" → Stop
    │
    └── "Do it" → /opsx:propose "feature"
                      │
                      ▼
                 Define specs in OpenSpec
                      │
                      ▼
                 ECC:feature-dev
                      │
                      ├── Issues? → Fix and loop
                      │
                      └── Done → /opsx:archive
```

## Quick Reference

| Stage | Tool | Command | Output |
|-------|------|---------|--------|
| Think | Superpowers | `brainstorming` | Decision |
| Specify | OpenSpec | `/opsx:propose` | Spec files |
| Build | ECC | `feature-dev` | Code |
| Complete | OpenSpec | `/opsx:archive` | Archived spec |

## Key Principles

1. **Superpowers first** — Never start coding without thinking
2. **OpenSpec before code** — Agree on what to build
3. **ECC for execution** — Use specialized agents for speed
4. **Archive when done** — Keep workspace clean

## Tips

- Use `Superpowers:writing-plans` after `brainstorming` to细化步骤
- Use `ECC:code-review` after any non-trivial implementation
- Run `/opsx:verify` before archiving to确认所有任务完成
