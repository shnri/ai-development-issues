---
name: optimize-skill
description: 既存のClaude Code Agent Skillを、隔離eval、失敗原因分析、1変更variant、独立review、blind A/B、promotion gateで改善する。Skill自体の品質改善を明示的に依頼されたときだけ使用する。
argument-hint: <skill-path> [goal=...] [max_iterations=N] [promotion_mode=report-only|branch]
disable-model-invocation: true
context: fork
agent: skill-optimizer
background: false
---

`$ARGUMENTS`で指定されたAgent Skillを改善する。

- repository rootの`CLAUDE.md`を守る
- `${CLAUDE_PLUGIN_ROOT}/skill-optimization.config.json`を既定値として読む
- nested subagentを標準で利用できるClaude Code v2.1.219以降を使う
- canonical Skillを直接編集しない
- Anthropic公式`skill-creator`をeval engineとして使う
- `skill-optimizer`を独立したoptimization orchestratorとする
- failure attributionとvariant reviewをoptimizerから別subagentへ委譲する
- 1iterationにつき1つのscoped changeだけ作る
- old/candidateを同一条件で比較する
- gateを通らないcandidateを反映しない
- `report-only`では変更案と証拠だけを残す
- `branch`では合格候補を独立worktree branchへ反映する
- pushとmergeは行わない

実行前に次を読む。

- [operational-guardrails.md](references/operational-guardrails.md)
- [optimization-method.md](references/optimization-method.md)
- [eval-design.md](references/eval-design.md)
- [artifact-contracts.md](references/artifact-contracts.md)
- [promotion-policy.md](references/promotion-policy.md)
- [operating-modes.md](references/operating-modes.md)

FAPO本体への移行を検討するときは[fapo-mapping.md](references/fapo-mapping.md)と
[full-fapo-adoption.md](references/full-fapo-adoption.md)を読む。外部Routineから起動するときは
[routine-operations.md](references/routine-operations.md)も読む。
