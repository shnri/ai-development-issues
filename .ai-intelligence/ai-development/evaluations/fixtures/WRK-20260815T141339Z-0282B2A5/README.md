# WRK-20260815T141339Z-0282B2A5 (RMD-H01-002) — baseline probe

Question: does the existing `mitigate-model-behavior-issues` Skill (mitigation-playbook.md as on main) already plan the Fable 5 long-run mitigation — do not stop/summarize/propose a new session because of remaining context, ground progress claims in session tool results, keep durable notes independent of context — for a project directly exposed (claude-fable-5, unattended Claude Code routine)?

- Fixture project: `repos/project` (AGENTS.md without completion criteria, fingerprint file, settings.json).
- Scenarios: `scenarios/target-context-stop.json` (target); `holdout-permission-stop.json` and `adjacent-verbosity.json` prepared but unused because the baseline probe was decisive.
- Variant: `variants/mitigation-playbook.baseline.md` (= main). Executor brief: `EXECUTOR.md`; runs: `runs/baseline/*.json`.

Result: 2/2 baseline trials produced a bounded, model/surface-gated instruction covering all three mechanisms (playbook §6 autonomous completion criteria + §4 grounded claims + §5 durable resume artifact) with the Stop hook as a fallback and no global instruction. No candidate was authored: the playbook's mechanism list already yields RMD-H01-002; in production the Skill's step 3 also consults the provider's model-specific guidance (the official Fable 5 prompting page cited in the remedy).

Fixture repository files are stored as `fixture-repos.json` (path → content); materialize them into a temporary directory before rerunning trials.
