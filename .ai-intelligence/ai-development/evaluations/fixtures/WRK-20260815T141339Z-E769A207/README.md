# WRK-20260815T141339Z-E769A207 (RMD-D14-001) — baseline probe

Question: does the existing `skill-optimization/optimize-skill` method (SKILL.md + references as on main) already make the optimizer record model/effort/harness/Skill-revision as one comparable configuration and run isolation/ablation experiments (Skill version, model, effort/harness) under matched conditions before touching the Skill, when a model alias, harness version and Skill text changed at once?

- Scenarios: `scenarios/target-harness-change.json` (target); `holdout-instruction-removal.json`, `adjacent-single-case-fail.json` prepared but unused because the baseline probe was decisive.
- Variant: `variants/baseline/` (copy of the Skill on main). Executor brief: `EXECUTOR.md`; runs: `runs/baseline/*.json`.

Result: 2/2 baseline trials recorded resolved model id, explicit effort, harness version/release-note items, skill-creator version, tool permissions, Skill tree digest/git SHA and eval/fixture/grader digests, and planned one-axis isolation runs (old vs new Skill; old vs new model/effort; drift check; attribution) with report-only mode after the harness/model change. No candidate was authored: RMD-D14-001 is covered by the existing asset (artifact-contracts run_config + optimization-method matched comparison + operating-modes report-only trigger + failure attribution agent).
