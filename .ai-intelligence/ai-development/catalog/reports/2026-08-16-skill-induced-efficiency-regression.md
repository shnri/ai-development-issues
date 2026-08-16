---
kind: established-development-problem
problem_id: PROBLEM-skill-induced-efficiency-regression
status: established
as_of: 2026-08-16T09:15:33Z
timezone: Etc/UTC
first_observed_at: 2026-03-16
first_established_at: 2026-08-12
last_material_update_at: 2026-08-16
next_review_at: 2026-11-16
areas: [engineering]
related_problem_ids: [P-20260816-66F0FD78, D04, G22, K11]
authority_record: .ai-intelligence/ai-development/catalog/catalog.json#P-20260816-66F0FD78
---

# Skill-induced efficiency regression

## 現在の結論

関連するAgent Skillでも、成果品質や成功率の改善が小さいままToken、所要時間、Tool Callを大きく増やす場合がある。この効率回帰はSkill本文をContextへ追加する直接費用だけでは説明できず、Skillが検証や実装Recipeを必須工程として解釈させることでも生じる。複数の比較研究と実運用寄りのbenchmarkで反復観測されているため問題の存在は確立しているが、発生率と損益分岐点はSkill、Task、Model、Harnessに依存する。

## 問題の定義

- **問題主張**: Agent Skillが実行経路へ介入すると、Task品質の限界改善に見合わないToken・時間・Tool Callの増加を誘発する場合がある。
- **状態**: established
- **問題としての確度**: medium
- **対象**: Software engineering Agentへ推論時にロードされる手順型Skill
- **成立条件**: Skillあり／なし、または対象Skill／意味的に近いSkillを同一Task条件で比較でき、成果とResource使用量の双方を観測できること
- **対象外**: 無関係なSkillの誤発火だけによる失敗、静的なSkill本文長だけで説明できるContext増加、Resource指標を観測しないこと自体、予算上限がないこと自体

## なぜ起きるか

直接確認されている原因は、Skillのchecklistや構築Recipeが状況に応じた選択肢ではなく必須工程として実行され、過剰な検証や重い実装pipelineへ展開されることである。Skill本文の追加による入力Token増加も寄与するが、差分分析では本文長だけでは効率回帰を説明できない。Model、Harness、Skillの適合度がどの程度この挙動を増減させるかは、まだ一般化できていない。

## 観測されている影響

- 同じTask成功率でもToken、時間、Tool Call、金額が増え、Skill導入の費用対効果が悪化する。
- 検証や実装工程の増加により、Agentのiteration時間とCI上の回帰検出時間が長くなる。
- 成果品質だけを評価する運用では、Skillが引き起こした効率回帰が見逃される。

## 成熟度の判定

2026年3月の49 Skillsを対象にしたpaired benchmarkで、改善なしと大幅なToken増加の組合せが確認された。2026年8月の別研究は2つのbenchmarkへ差分帰属を適用し、182件のSkill-induced efficiency regressionを分類して、過剰検証と重い実装pipelineを主要因として確認した。4月のvendor benchmarkも異なるTask構成で大幅なToken・Turn増加を報告している。研究dataset間の依存や2026年時点のModel偏りは残るが、時間的反復、比較条件、原因分類が揃っているため存在を`established`、一般化の確度を`medium`とする。

## Evidence timeline

| 観測日・期間 | 根拠の種類 | 観測内容 | 支持する主張 | 独立性・限界 |
| --- | --- | --- | --- | --- |
| 2026-03-16 | primary research / paired benchmark | 49 Skills中39件はpass-rate改善なし。pass rate不変のままToken overheadが最大451%増加 | Skill導入が成果改善なしのResource回帰を生み得る | 公開Software engineering Skills中心。Model・Task分布に依存 |
| 2026-04-21 | vendor field benchmark | 880 evalsで、特定構成は+2ppに対してcost最大約3倍、入力Token 82%増、Turn 40%増 | 実運用寄りの設定でも費用対効果の不均衡が起きる | Vendor作成benchmarkであり、全構成の平均liftは正だった |
| 2026-08-12 | primary research / differential attribution | 307件のSkill-induced failure中182件が効率回帰。過剰検証67件、重い実装pipeline 30件 | prompt長以外のSkill誘発手順が効率回帰を生む | SkillsBenchとSWE-Skills-Benchを用いるため、前研究とdatasetの一部関係がある |

## 反証・代替説明

- SWE-Skills-Benchでは7つの専門Skillが意味のある改善を示しており、Skill全般が無効という問題ではない。
- Tesslのbenchmarkでは全88構成で平均adherenceが改善したため、Resource増加が常に不利益になるとは限らない。
- Task難度、Model、Harness、cache、価格体系の差が、Skill自体の効果と混在する可能性がある。

## 未解決部分

- 品質改善とToken・時間・Tool Call増加を交換可能にする一般的な採否閾値はない。
- Skillのどの記述形式が過剰手順を誘発するかを、実行前に安定して予測できるかは未確立である。
- Software engineering以外のAgent Skillへ同じ発生率を一般化できるかは不明である。

## 再確認条件

- **定期確認**: 2026-11-16。異なるModel・Harness・Task領域での独立再現を確認する。
- **イベントtrigger**: Agent Skill runtimeの大幅変更、主要Model世代更新、差分Skill evalの大規模benchmark公開

## 変更履歴

- 2026-08-16: paired benchmark、差分帰属研究、field benchmarkを統合して新規登録。

## 根拠

- [SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering?](https://arxiv.org/abs/2603.15401) — arXiv、2026-03-16。49 Skillsのwith/without比較とToken overhead。
- [Anthropic, OpenAI, or Cursor model for your agent skills?](https://tessl.io/blog/anthropic-openai-or-cursor-model-for-your-agent-skills-7-learnings-from-running-880-evals-including-opus-47/) — Tessl、2026-04-21。880 evalsのfield benchmark。
- [Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents](https://arxiv.org/abs/2608.11888) — arXiv、2026-08-12。Skill誘発失敗と効率回帰の差分帰属。
