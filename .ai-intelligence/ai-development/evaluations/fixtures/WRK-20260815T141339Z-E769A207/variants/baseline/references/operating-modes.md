# Operating Modes

## report-only

用途:

- 導入初期
- eval品質が未確認
- optimizer精度を測っている
- critical Skill
- model / harness更新直後

動作:

- baselineを実行
- candidateを作成
- reviewとcomparisonを行う
- promotion decisionを保存
- canonicalは変更しない

推奨期間: 最初の5〜10 optimization run。

## branch

用途:

- evalとgateが安定した
- optimizerのfalse improvementを把握した
- Git reviewで最終確認できる

動作:

- gate通過candidateだけを独立worktreeへcopy
- `claude/skill-opt-*` branchを作成
- commitを作成
- main checkoutは変更しない
- pushしない

人間の作業はbranch diffの確認とmergeだけになる。

## in-place

このPluginでは非推奨・未提供。

理由:

- baselineを失う
- session途中でSkillが再読込され、条件が変わる
- rollbackが難しい
- unrelated changesと混ざる
- false improvementが即時本番化する

## 実行頻度

毎日自動でSkillを書き換えない。

推奨:

- weekly optimization review
- material anomaly trigger
- Skill変更trigger
- model / Claude Code upgrade trigger

## Optimization budget

1回のrun:

- 1 target Skill
- 最大3 iterations
- 1 iteration 1 scoped change
- max 8 replay casesで開始
- live smoke 1回
- plateau 2回で停止

Skill数が多い場合、週ごとに対象をrotateする。
