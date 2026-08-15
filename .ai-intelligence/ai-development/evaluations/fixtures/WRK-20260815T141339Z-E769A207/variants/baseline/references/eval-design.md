# Skill Eval設計

## 目的

Evalは「Claudeがそれらしい説明をしたか」ではなく、
Skillによって実際のtask成功率が改善したかを測る。

## Eval setの構成

最低6ケースを推奨する。

1. typical success
2. known failure
3. edge condition
4. near miss
5. should-not-change / no-op
6. holdout

research Skillではさらに次を入れる。

- source不足
- source conflict
- period boundary
- duplicate
- no material update
- unsupported generalization

## Replay Eval

Replay fixtureには次を保存する。

- basis time
- prior state
- source metadata
- source family
- extracted evidence
- tool availability
- expected classification
- expected non-action

Replayではlive Webを禁止する。

目的は、同じevidenceに対してSkill versionだけを変えること。

## Live Smoke

Live Smokeは次を確認する。

- current sourceへ到達できる
- current metadataを読める
- current file pathsで動く
- permissionやconnectorが壊れていない
- output schemaが生成される

Live Smokeの結果はpromotion scoreへ直接足さない。
結果が変わる場合、Replay fixtureを追加して次回から固定評価する。

## Expectations

良いexpectation:

- `status`が`sustained`である
- `update_type`が`broadened`である
- 同じmetricの微増だけなら保存しない
- topicをtrendとして自動変換しない
- source familyを2種類以上示す
- adoption recommendationを書かない

弱いexpectation:

- 良い文章である
- 詳しく説明する
- 正しいtrendを見つける
- usefulである

## Critical failure

次はcriticalとして扱う。

- false positiveでcanonical knowledgeへ誤ったstateを保存
- topic / trend / impactの責務混同
- date boundary違反
- sourceなしの事実断定
- fixture / eval answer leakage
- credential、branch、push等の権限逸脱
- existing stateの破壊
- unknown frontmatter追加

## Holdout

candidateを作るagentへholdoutのexpected answerを見せない。
holdoutは少なくとも全体の20%を確保する。

同じtemplateの値違いだけではholdoutにならない。
因果や境界が異なるcaseを選ぶ。

## Model variance

同じcaseを複数回実行できる場合、1回の偶然を改善としない。

- critical case: 3 run推奨
- deterministic output: 1 runでも可
- subjective case: blind A/Bを複数比較

## Eval maintenance

Skillを変更するたびにevalを増やさない。

eval追加条件:

- 新しいfailure class
- 既存caseでは再現不能
- productionでmaterial incident
- model / harness変更で新しい境界が出た

同じfailureの表現違いは既存caseへ統合する。
