# Routine運用

Claude Code RoutinesまたはDesktop scheduled taskでは、
毎回すべてのSkillを改善しない。

## Weekly routine

1. 直近7日で変更されたSkillを列挙する
2. 直近7日の実行異常を収集する
3. material anomalyがあるSkillを最大1件選ぶ
4. `/skill-optimization:optimize-skill`を`report-only`で実行する
5. promotion候補と証拠をrepositoryへ保存する
6. gate合格時だけbranch modeの候補にする

## Immediate trigger

次の場合に週次を待たない。

- critical false positive
- critical false negative
- state破壊
- security boundary違反
- date / source attribution違反
- model updateで既知evalが複数fail

## Routine prompt

consumer repositoryが所有する週次Routineを使用する。元スターターの完全な例は
共有repositoryの`docs/examples/weekly-skill-optimization.md`に保存している。

## 注意

`/skill-optimization:optimize-skill`は人間が明示実行するため
`disable-model-invocation: true`である。

Routineではnamespaced commandを明示的に実行する。
入口Skillの`context: fork`により`skill-optimizer`がworkflowを統括する。
