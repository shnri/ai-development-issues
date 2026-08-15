# Promotion policy

## Default mode

Use `report-only` until repeated runs show that attribution and review decisions
generalize. Five to ten successful human-reviewed optimization runs are a useful
operational checkpoint, not a statistical guarantee.

## Required gate conditions

Promote only when all conditions hold:

- the primary root cause is `skill` with a justified candidate change;
- the independent reviewer approves with no blocking findings;
- baseline and candidate use identical eval IDs and shared run configuration;
- candidate pass rate is not lower;
- no previously passing case fails and no case score decreases;
- at least one case improves and the aggregate score delta meets the configured
  threshold;
- the candidate contains one logical change and no candidate-only metadata;
- target repository tests and Skill validation pass.

Token or duration increases do not fail the gate by default because quality may
justify cost. Report both deltas. A target owner may add explicit budgets before
the run, but must not invent them after seeing a candidate.

## Report-only

Do not edit the canonical Skill. Return artifact paths, reviewer findings,
comparison deltas, and the gate decision.

## Branch

Require a clean Git repository and a new branch name. Create a separate worktree,
copy only the candidate `skill/` tree to the target Skill path, and leave the
worktree uncommitted for inspection. Do not delete an existing worktree, reuse an
existing branch, commit, push, merge, publish, or update a consumer submodule.

## Automatic rejection

Reject when evidence is missing, malformed, unmatched, or ambiguous. Also reject
eval leakage, fixture-specific rules, responsibility expansion, safety weakening,
multiple logical changes, hidden regressions, or a non-Skill root cause.
