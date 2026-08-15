# AI Development Issues

AI支援開発で反復観測される問題（AI Development Problems）の**Living Catalog・Evidence・Research・一般化された改善策**を管理する、`ai-development-improvement` Pluginの**中央Authority Repository**です。

## 目的

- AI開発問題を「一度調べて終わり」の報告書ではなく、継続的に棚卸し・再検証されるLiving Catalogとして維持する。
- 問題ごとの根拠（Evidence）、対策調査（Research）、再利用可能な改善策（Remedy）、Lifecycle／Historyをproject横断で1か所に集約する。
- 改善の実装・評価・promotion・releaseの記録（Work Item／Implementation／Evaluation／Promotion／Release／Propagation）を保持し、閉ループ改善の正本にする。

## `shared-agent-plugins` との違い

| Repository | 役割 | 内容 |
| --- | --- | --- |
| [`shared-agent-plugins`](https://github.com/shnri/shared-agent-plugins) | **仕組み** | AI開発問題を発見・調査・改善するPlugin／Skill／script／schema／eval（`ai-development-improvement` を含む共有実行資産） |
| `ai-development-issues`（このRepository） | **知識の正本** | 問題Catalog、Evidence、Research、Remedy、Lifecycle／History、Quick Win、公開可能なEval結果、改善のrelease／propagation記録 |
| 各Project（例: TechLog） | **Project固有state** | findings／experiments／adoptions、project固有のfingerprintと例外 |

Pluginは方法（method）を持ち、このRepositoryは状態（state）を持ちます。Plugin本体はここでは編集せず、`vendor/shared-agent-plugins` submoduleで確定SHAを参照します。

## Authority / Consumer

```text
ai-development-issues (role: authority)
  └─ .ai-intelligence/ai-development/catalog/catalog.json  ← 唯一の可変Catalog
        ▲ read-only参照（submodule等のfilesystem path）
各Project (role: consumer)
  └─ .ai-intelligence/ai-development/project-profile.json
        catalog.authority_paths: ["vendor/ai-development-issues/.ai-intelligence/ai-development/catalog/catalog.json"]
        knowledge_sources:       ["vendor/ai-development-issues/.ai-intelligence/ai-development/remedies"]
```

- Authorityだけが`catalog.json`・`remedies/`・catalog events／reviews／snapshotsを変更する。
- ConsumerはAuthorityをread-onlyで参照し、Catalogを複製・Forkしない。Consumer側の`maintenance_plan.py`等の可変操作は`PermissionError: Catalog authority is external/read-only`で拒否される。
- Consumer固有のfindings／experiments／adoptionsはConsumer側の`.ai-intelligence/ai-development/`に置く。

## Living Catalogとは

`catalog/catalog.json`はrevision付きの問題一覧で、各問題は`active`／`mitigated`／`inactive`／`obsolete`／`superseded`／`unverified`のlifecycle状態、`source_refs`、`research_status`、再開trigger、次回棚卸し期日を持ちます。変更は`catalog/events/`（変更履歴）、`catalog/reviews/`（棚卸し判定）、`catalog/snapshots/`（revisionごとのsnapshot）、`catalog/candidates/`（発見候補）に残り、`check_catalog_integrity.py`で構造整合性を検証できます。

## `maintain` による継続更新

このRepositoryは定期Routineから`ai-development-improvement`の`maintain` modeで更新されます。

```text
棚卸し（inventory） → 新規問題探索（discover） → 必要なresearch → 改善候補化（work item）
→ 実装・独立評価（optimize/evaluate） → promotion → shared-agent-plugins等へのrelease（PR）
→ Consumer propagation event → Catalog更新 → validation → commit・push
```

- Routine prompt: `routines/maintain.prompt.md`
- 手順: `AGENTS.md`（`CLAUDE.md`から参照）
- 検証: `python3 scripts/check_authority.py`（catalog integrity、record schema、public boundary、maintain plan dry-run）
- Authority stateのcommit／pushは`automation-policy.json`の`release.authority_state_strategy=direct`に従い、validation通過後にのみ`safe_commit_state.py`が`main`へ行う。
- 共有Skill／Pluginへの変更は`target-registry.json`の`shared-agent-plugins` target（`git-clone`→`.ai-intelligence/ai-development/workspaces/`、release strategy `pull-request`、validation `npm run check`）を通し、`shared-agent-plugins`側のrelease policyとR0–R3 Risk gateを守る。

## Public Repositoryへ保存してよい情報／いけない情報

このRepositoryは**Public**です。`scripts/check_public_boundary.py`が機械的に検査し、違反があるとvalidationが失敗します。

| 保存してよい | 保存しない |
| --- | --- |
| AI開発問題Catalog | Private Repositoryのコード |
| 公開情報に基づくEvidence／Research | Project固有のAgent Trace／transcript |
| 一般化された改善策（Remedy） | Project固有の内部情報（絶対path、内部文書の内容、`<project>_notes`等） |
| 問題のLifecycle／History | Credential／Secret／Token |
| Quick Win | 非公開URL（localhost、private IP、`*.internal`等） |
| 公開可能なEval結果 | 顧客・利用者データ |
|  | 未公開の脆弱性情報 |
|  | 各Project固有のfindings／experiments／adoptions |

Consumerの観測に由来する記録は、`origin`／`source_refs`にproject名を残す程度のprovenanceに留め、内容はConsumer側に置きます。

## Layout

```text
.ai-intelligence/ai-development/
├── project-profile.json      # role: authority
├── automation-policy.json    # closed-loop、authority stateはmainへdirect commit/push
├── target-registry.json      # current-project(authority) / shared-agent-plugins(git-clone, pull-request)
├── catalog/                  # catalog.json, sources, candidates, reviews, events, snapshots, reports
├── remedies/                 # 再利用可能な改善策
├── work-items/ implementations/ evaluations/ promotions/ releases/ propagation/ capabilities/
├── runs/                     # maintenance run記録
└── workspaces/               # target checkout（gitignore、commit対象外）
scripts/check_authority.py            # 一括validation
scripts/check_public_boundary.py      # public境界検査
routines/maintain.prompt.md           # Routine用prompt
vendor/shared-agent-plugins           # Plugin実体（submodule、確定SHA）
.claude/skills/, .agents/skills/      # Skill探索用link → submodule内実体
```

## Setup

```bash
git clone --recurse-submodules https://github.com/shnri/ai-development-issues.git
cd ai-development-issues
python3 scripts/check_authority.py
```

`vendor/shared-agent-plugins`はprivate repositoryのため、閲覧権限がない環境ではsubmoduleを初期化できません。その場合もCatalog等のstate自体は読めます。

## 由来

2026-08-15に`shared-agent-plugins`の`.ai-intelligence/ai-development/`からGit履歴ごと移行しました（419 file、per-file sha256一致を確認）。移行後、Consumer固有のnote fieldと絶対pathだけをpublic境界に合わせて除去しています。
