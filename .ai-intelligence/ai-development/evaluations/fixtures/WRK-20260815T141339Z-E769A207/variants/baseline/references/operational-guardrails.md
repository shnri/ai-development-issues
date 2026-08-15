# Claude Skill Optimization Operations

## Purpose

Operate Agent Skill improvement as an eval-driven optimization process.

## Non-negotiable rules

- Treat the canonical Skill as read-only until the promotion gate passes.
- Create every candidate as a separate variant.
- Make one scoped conceptual change per iteration.
- Run old and candidate versions against the same evals and execution harness.
- Use fresh subagent contexts for evaluation.
- Delegate failure attribution and variant review to separate agents.
- Do not accept an optimizer's self-review as the only evidence.
- Do not use live Web variation as the primary promotion score.
- Do not encode eval IDs, fixture paths, expected answers, or test-only branches into a Skill.
- Do not change the Skill when the root cause is an eval, fixture, environment, tool, or model-variance problem.
- Do not edit the default branch directly.
- Do not push or merge automatically.
- Preserve the Skill's name and primary purpose.
- Prefer the smallest useful edit.
- Record evidence paths for every promotion decision.

## Evaluation layers

1. Deterministic validation
2. Replay eval
3. Failure attribution
4. Independent variant review
5. Blind A/B
6. Holdout comparison
7. Live smoke test
8. Promotion gate

## Claude model allocation

Use Fable for optimizer, root-cause attribution, and independent review.
Keep executor model and harness identical between baseline and candidate.

## Official skill-creator

Use the installed Anthropic `skill-creator` as the eval engine.
Do not recreate its isolated run, grading, benchmark, or blind comparison logic.

If `skill-creator` is unavailable, stop with a precondition failure and provide:

```text
/plugin marketplace add anthropics/claude-plugins-official
/plugin install skill-creator@claude-plugins-official
/reload-plugins
```

## Nested CLI prohibition

Do not launch `claude -p` from inside an active Claude Code session.
Use subagents and the official skill-creator instead.
