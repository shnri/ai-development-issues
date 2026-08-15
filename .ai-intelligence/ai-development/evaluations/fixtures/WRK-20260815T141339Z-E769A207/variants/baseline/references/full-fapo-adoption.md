# Full FAPOを採用する場合

## このPluginを先に推奨する理由

このPluginの対象は、Claude Codeが実際に読み込むAgent Skillである。
評価もClaude Codeのfresh subagentと公式`skill-creator`で行うため、
Skill discovery、CLAUDE.md、tool permission、subagent contextなどの実行条件が本番に近い。

FAPO本体の標準構成は、dataset、scorer、LangGraph chain、provider経由のtask modelを持つ。
これはmulti-step LLM pipeline全体を最適化するときに強い。一方、Claude Code subscriptionだけで
実際のSkill executorを評価したい場合、標準のprovider task modelとはharnessが異なる。

したがって最初は次の構成にする。

```text
Claude Code / Fable optimizer
        ↓
Anthropic skill-creator
        ↓
実際のClaude Code fresh subagentでSkill実行
        ↓
Replay Eval / blind A-B / gate
```

## Full FAPOへ移る条件

次のいずれかが生じたら、FAPO本体へ移行する価値が高い。

- Skillだけでなくretrieval、routing、複数LLM stepも改善対象になった
- intermediate step outputへfailureを帰属したい
- prompt、Skill、parameter、chain topologyを同じloopで最適化したい
- 数十〜数千caseをAPI modelで反復評価したい
- 複数optimization projectをtenant単位で隔離したい
- LangGraph stateとして実行trajectoryを厳密に保存したい

## 移行方法

1. FAPOを別repositoryまたはsubmoduleで導入する。
2. 1 Skillを1 tenantへ対応させる。
3. Replay fixtureをFAPO dataset JSONLへ変換する。
4. Skillの期待結果をscorerへ変換する。
5. Claude Code Skillの実行忠実度が必要なら、FAPOのtask model呼び出しを実際のClaude Code executionへつなぐadapterを作る。
6. 同じbaseline Skillを、このPluginとFAPO adapterの両方で実行し、出力差を確認する。
7. harness差が許容できる場合だけFAPO scoreをpromotionの主判定へ使う。

## Adapterの責務

```text
candidate SKILL.md
      ↓
Claude Code execution adapter
      ↓
actual Skill loading + tools + permissions
      ↓
output / transcript / token / duration
      ↓
FAPO ChainState / scorer
```

adapterは少なくとも次を固定する。

- Claude modelとeffort
- CLAUDE.md
- available tools
- permission mode
- attached fixture
- working directory
- Skill version
- run timeout
- output schema

## 課金上の違い

このPluginはClaude Code subscriptionの利用枠内で動かせる。
Full FAPOの標準task modelはprovider API経由なので、task model側のAPI料金が別途発生し得る。
Claude Codeをtask executorとして使うcustom adapterならAPI task modelを避けられるが、
subagent実行によるClaude Code利用枠は消費する。
