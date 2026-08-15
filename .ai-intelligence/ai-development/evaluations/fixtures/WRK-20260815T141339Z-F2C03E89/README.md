# WRK-20260815T141339Z-F2C03E89 (RMD-F18-001) — baseline probe

Question: does the existing `maintain-agent-instructions` audit (audit-criteria as on the pending 0.1.1 branch) already lead the auditor to propose a staged verification gate (lint/typecheck/build/E2E, not only `npm test`) and grounded completion reporting for a Next.js/TS repository whose AGENTS.md says "run `npm test`, PASS = done"?

- Fixture repos: `repos/target-nextjs` (target), `repos/holdout-python` (holdout, unused because the baseline probe was decisive), `repos/adjacent-nextjs-with-gate` (adjacent, unused).
- Variants: `variants/audit-criteria.main.md` (main), `variants/audit-criteria.baseline-0.1.1.md` (pending release branch).
- Executor brief: `EXECUTOR.md`; runs: `runs/baseline/*.json`.

Result: 2/2 baseline trials proposed the staged verification gate (更新 of the `npm test` rule, driven by 陳腐化シグナル「能力前提が古い」+ package.json/playwright evidence) and grounded reporting (欠落シグナル bullet 2 from 0.1.1). No candidate was authored: RMD-F18-001 is covered by the existing asset (main criteria) plus the pending 0.1.1 release; adding a third 欠落シグナル bullet would duplicate behaviour the baseline already shows.

Fixture repository files are stored as `fixture-repos.json` (path → content); materialize them into a temporary directory before rerunning trials.
