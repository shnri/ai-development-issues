# Optimization method

## Roles and information boundaries

The `skill-optimizer` fork is the controller. Keep these roles in fresh contexts:

1. The official `skill-creator` executes and grades fixed evals.
2. `skill-failure-attribution` sees raw failures and classifies the earliest
   supported cause. It does not see a proposed fix.
3. `skill-optimizer` orchestrates the loop, receives an accepted Skill
   attribution, and authors one change. It does not grade or approve itself.
4. `skill-variant-reviewer` sees the baseline, candidate diff, responsibility,
   eval prompts, and fixtures. It does not receive the author's defense.

This separation reduces confirmation bias without pretending the fixed eval set
proves universal quality.

The optimizer has the `Agent` tool and starts the attribution and reviewer
agents as depth-2 nested subagents. Current Claude Code releases support this
without a project setting. The main session does not absorb the optimization
controller role.

## Iteration sequence

### 1. Freeze the baseline

Create a byte-for-byte snapshot before editing. Record a tree digest and keep
evals with the target Skill. Evals are part of the target's correctness contract,
not part of the optimizer Plugin.

### 2. Establish a valid failure

Use the official `skill-creator` harness. For an existing Skill, compare against
the old Skill snapshot rather than a no-Skill baseline when measuring an
improvement. Capture raw output, assertion grading, token count, and duration for
every run. A missing tool or denied permission is evidence about the environment,
not automatically about the Skill.

### 3. Attribute upstream

Trace the visible failure through grader, fixture, environment, and Skill. Choose
the earliest cause that explains downstream symptoms. If the cause is not the
Skill, fix or report that layer outside this loop and rerun the unchanged
baseline before proposing a Skill change.

### 4. Create one variant

State one hypothesis in the form: "Changing X should improve Y under condition Z
without worsening W." Make one logical change. Multiple files may change only
when they are inseparable parts of that hypothesis. A variant that edits the
Skill description and rewrites its workflow for unrelated failures is two
changes and must be split.

### 5. Review before comparison

Reject a candidate before expensive runs when it contains:

- eval IDs, fixture names, expected phrases, or case-specific branches;
- responsibility or output ownership that the baseline did not have;
- contradictions with repository instructions or the Skill's own references;
- broader permissions, weaker validation, or suppressed errors;
- unrelated cleanup or more than one logical hypothesis.

### 6. Compare under matched conditions

Launch baseline and candidate for the same eval set in the same turn. Keep model,
effort, repetitions, fixtures, assertions, graders, and tool permissions equal.
Randomized ordering or blind labels are preferred when the harness supports them.
Normalize results only after raw artifacts are saved.

### 7. Gate and iterate

Promote only an independently approved candidate with no case regression and at
least one material quality improvement. A failed candidate becomes new evidence;
return to attribution. Do not repair several suspected causes at once.

## Stopping rules

Stop when any condition holds:

- the root cause is outside the Skill;
- the fixed eval or environment cannot produce a valid comparison;
- the iteration budget is exhausted;
- no candidate improves quality without regression;
- reviewer findings require a responsibility or safety change;
- a candidate passes and the configured promotion action completes.
