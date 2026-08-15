# Mitigation playbook

These are candidate mechanisms, not universal fixes. Always match the issue's model, surface, condition, and provider guidance, then validate locally.

## 1. Excessive verbosity / over-explanation

Potential mechanisms:

- short model-specific instruction that leads with outcome/TLDR and drops details that do not affect the next action;
- lower effort for routine tasks if provider guidance says higher effort over-deliberates;
- separate user-facing final summary from internal/tool-call narration in the harness;
- remove older prompts that force exhaustive reasoning/explanation.

Avoid:

- universal hard word/token caps without regression eval;
- terse shorthand that hurts readability;
- forcing the model to reveal internal reasoning.

Evaluate:

- output tokens/words;
- task completeness;
- correctness;
- whether the user gets the requested answer early;
- coding/analysis quality on harder cases.

## 2. Overplanning / unnecessary second-guessing

Potential mechanisms:

- explicit stop condition: act when enough information is available;
- ask only for genuinely missing user-only input;
- instruct the agent not to re-litigate decisions already established;
- use lower effort for simple, reversible tasks where supported.

Evaluate:

- unnecessary questions before action;
- time/tool calls to first useful action;
- correctness after acting sooner.

## 3. Scope creep / unsolicited refactor

Potential mechanisms:

- model-specific "smallest change" instruction;
- explicit boundaries around files/feature scope;
- diff-based eval that penalizes unrelated edits;
- lower effort for routine fixes when high effort causes over-engineering.

Evaluate:

- files/lines changed outside target scope;
- functional tests;
- whether required edge cases were still handled.

## 4. Unsupported progress claims / hallucinated completion

Potential mechanisms:

- require progress claims to be grounded in tool results from the current run;
- expose structured tool/eval status to the agent;
- separate "attempted" from "verified" in completion criteria.

Evaluate:

- every completion/progress claim maps to an observable tool/test result;
- no claim of passing when tests failed/skipped.

## 5. Context loss / repetition

Potential mechanisms depend heavily on layer:

- fix session/resume/context-pruning logic;
- preserve required prior tool results and decisions;
- use a project memory/lesson file for durable facts not already represented in code/history;
- change compaction/caching behavior only when the harness is the actual cause.

Evaluate:

- retention of previously established requirements;
- repeated questions/actions;
- long-session continuation after idle/resume.

Do not fix a harness context bug by adding repeated prompt reminders everywhere.

## 6. Early stopping / unnecessary permission requests

Potential mechanisms:

- explicit autonomous completion criteria for reversible actions;
- distinguish destructive/irreversible actions from normal continuation;
- ensure the agent has a way to continue long-running work without treating every checkpoint as user approval.

Evaluate:

- whether the agent stops with statements of intent instead of performing the next tool action;
- number of unnecessary permission questions;
- safety around genuinely destructive operations.

## 7. Tool-use failures

Potential mechanisms:

- improve tool descriptions and parameter schemas;
- update provider-recommended tool versions;
- add explicit tool-trigger conditions only when the model fails to infer them;
- preserve tool results/context correctly;
- route to a model better suited to the tool workload when repeated evals fail.

Evaluate:

- tool selection accuracy;
- valid arguments;
- completion after tool results;
- no unnecessary tool calls.

## 8. Refusal / safety false positives

Potential mechanisms:

- follow provider-supported prompt framing, fallback, or routing for benign workloads;
- distinguish model refusal from application filter or policy layer;
- update to a provider-fixed version when available.

Do not attempt to bypass legitimate safety controls. The goal is reliability for allowed workloads, not circumvention.

## 9. Effort / latency / token-use behavior

Potential mechanisms:

- task-based effort routing;
- model-specific effort defaults;
- lower effort for routine work, higher effort for capability-sensitive cases;
- progress UX or asynchronous harness for legitimately long turns.

Evaluate the Pareto tradeoff:

- quality/correctness;
- latency;
- output/reasoning token cost where observable;
- user-perceived responsiveness.

## 10. Model upgrade or stronger-model regression

Newer models can make old scaffolding harmful.

Potential mechanisms:

- remove obsolete defensive instructions;
- simplify over-prescriptive skills/prompts;
- gate legacy behavior workarounds to old models;
- rerun regression evals before deleting a workaround.

Prefer evidence-based subtraction over continuously appending prompt rules.
