# FAPOとの対応

このPluginはFAPO本体のcopyではない。Claude Code Agent Skillを対象に、
FAPOの最適化methodをClaude native機能へ対応させた構成である。

| FAPO stage | このPlugin |
|---|---|
| Evaluate | Anthropic公式`skill-creator`のisolated run / grading / benchmark |
| Attribute | `agents/skill-failure-attribution.md` |
| Propose | `agents/skill-optimizer.md`が作る1変更variant |
| Review | `agents/skill-variant-reviewer.md` |
| Compare | `skill-creator`のold-skill comparison / blind A/B |
| Iterate | `/skill-optimization:optimize-skill` |
| Variant history | `.skill-optimization/<skill>/variants/`と`history.json` |
| Promotion | `promotion_gate.py` |
| Safe apply | `promote_to_worktree.py` |

## 共通する原則

- optimizerとtask executorを分ける
- final scoreだけでなくfailure locationを見る
- smallest useful changeを優先する
- candidateをin-placeで上書きしない
- independent reviewerを通す
- validation結果で比較する
- plateauまたはsuccess criteriaで止める

## 異なる点

FAPO本体:

- LangGraph pipeline
- provider経由のtask model
- retrieval / prompt / skill / parameter / topologyを最適化
- tenant workspace
- reusable evaluation engine

このPlugin:

- Claude Code Skillだけを対象
- actual Claude Code subagent harnessで評価
- official`skill-creator`をeval engineとして再利用
- prompt / Skill以外のchain topologyは変更しない
- subscription loginで動作し、API integrationを必須にしない

## FAPO本体へ移る判断

次のどれかに該当したらfull FAPOを検討する。

- Skill以外の複数LLM nodeを持つ
- retrieval stepのfailure attributionが必要
- model parameterもoptimization対象
- chain topologyを変更したい
- API経由で大量datasetを反復評価したい
- 複数tenantを同じengineで管理したい
