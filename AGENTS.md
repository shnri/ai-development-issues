# ai-development-issues 共有指示

このRepositoryは`ai-development-improvement` Pluginの中央Authority（`catalog.role=authority`）であり、AI開発問題のLiving Catalog・Evidence・Research・Remedy・改善記録の正本である。PublicなRepositoryである。

## 役割の境界

- Plugin／Skill本体は`vendor/shared-agent-plugins`（git submodule、確定SHA）にあり、ここでは編集しない。共有資産の変更は`target-registry.json`の`shared-agent-plugins` targetを通じ、`shared-agent-plugins`側のrelease policyとR0–R3 Risk gateに従ってPRで行う。
- Consumer固有のfindings／experiments／adoptions、Agent Trace、内部情報、Credential、非公開URLは置かない。`README.md`のpublic境界表と`scripts/check_public_boundary.py`が正本である。
- Consumer projectへCatalogをコピーしない。ConsumerはAuthorityをread-onlyで参照する。

## `maintain` の実行手順

「`ai-development-improvement` の `maintain` を実行してください。」と指示されたら次を行う。

1. `git submodule update --init --recursive` でPlugin実体を用意し、`.claude/skills/ai-development-improvement/SKILL.md`と`references/mode-maintain.md`、`references/automation-model.md`を読む。
2. `python3 scripts/check_authority.py` が通ることを確認する（通らなければ先に原因を報告し、stateを壊す操作はしない）。
3. Skillの`maintain` modeをこのRepositoryをauthorityとして実行する（`maintenance_plan.py . --write`から開始）。棚卸し → 新規問題探索 → 必要なresearch → `action_queue.py --apply`による改善候補化 → Work Itemの実装・独立評価 → promotion → 必要に応じて`shared-agent-plugins`へのrelease／propagation → Catalog更新まで、`automation-policy.json`の範囲で進める。
4. 共有targetは`ensure_target_repo.py . shared-agent-plugins --apply`で`.ai-intelligence/ai-development/workspaces/`へcloneし、`prepare_target.py`でclean baseを確認してから使う。releaseは`release_git.py`の`pull-request` strategyのみ。`main`への直接pushや保護回避はしない。
5. `complete_maintenance_run.py`で実行記録を閉じ、`python3 scripts/check_authority.py`を再実行する。
6. validation通過後、`safe_commit_state.py . --apply`でAuthority state（`.ai-intelligence/ai-development/**`のみ）を`main`へcommit・pushする。state以外の差分が混ざる場合はcommitせず報告する。
7. 変更なしの実行も正常である。blockedやdecision-requiredは、不足しているtarget・権限・baseline・validation・人間の判断を具体的に報告する。

## 検証

state、script、文書のいずれを変更した場合も`python3 scripts/check_authority.py`を実行する。public境界の違反は修正せずに公開しない。
