# Artifact contracts

Generated optimization artifacts live outside the canonical Skill.

## Workspace

```text
<workspace>/
├── workspace.json
├── baseline/
│   └── skill/
├── candidates/
│   └── iteration-001/
│       ├── skill/
│       └── variant.json
└── runs/
    └── ... official skill-creator artifacts ...
```

`variant.json` is candidate metadata and must remain a sibling of `skill/`.

## Failure attribution

```json
{
  "schema_version": 1,
  "root_cause": "skill",
  "confidence": "high",
  "candidate_change_justified": true,
  "summary": "The Skill does not distinguish current status from update type.",
  "evidence": ["runs/baseline/eval-7/grading.json"]
}
```

Allowed causes are `skill`, `eval`, `fixture`, and `environment`. Set
`candidate_change_justified` to `true` only for a supported `skill` cause.

## Independent review

```json
{
  "schema_version": 1,
  "decision": "approve",
  "blocking_findings": [],
  "overfit_signals": [],
  "responsibility_drift": [],
  "contradictions": []
}
```

Allowed decisions are `approve` and `reject`. Any blocking finding rejects the
candidate even if `decision` was written incorrectly.

## Normalized comparison

Normalize the official `skill-creator` benchmark without discarding its raw
files:

```json
{
  "schema_version": 1,
  "eval_ids": ["1", "2"],
  "run_config": {
    "model": "fable",
    "effort": "high",
    "repetitions": 1,
    "grader": "same-assertions-v1"
  },
  "baseline": {
    "pass_rate": 0.5,
    "score": 5.0,
    "total_tokens": 10000,
    "duration_ms": 20000,
    "cases": {
      "1": {"passed": true, "score": 3.0},
      "2": {"passed": false, "score": 2.0}
    }
  },
  "candidate": {
    "pass_rate": 1.0,
    "score": 7.0,
    "total_tokens": 10500,
    "duration_ms": 21000,
    "cases": {
      "1": {"passed": true, "score": 3.0},
      "2": {"passed": true, "score": 4.0}
    }
  }
}
```

`eval_ids` and both `cases` key sets must be identical. `run_config` describes
the shared configuration, not variant-specific labels.

## Promotion decision

`promotion-gate.py` writes:

```json
{
  "schema_version": 1,
  "promote": true,
  "reasons": [],
  "regressions": [],
  "improvements": ["2"],
  "deltas": {
    "pass_rate": 0.5,
    "score": 2.0,
    "total_tokens": 500,
    "duration_ms": 1000
  }
}
```

Raw benchmark, attribution, review, and decision files are evidence. Do not place
them in the promoted Skill directory.
