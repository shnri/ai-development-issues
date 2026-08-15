# CLAUDE.md — Ledgerly

Ledgerlyは家計簿SaaSのRails 7 API + React SPA。Ruby 3.3、Node 22、pnpm。

## ルール

- 変更前に関連specを`docs/specs/`で確認する。
- テストは変更したファイルに関連するspecだけを実行し、PR前に全体を1回実行する。
- コードを保存するたびに必ず`pnpm prettier --write`を実行する。
- 本番DBに触るコマンドは絶対に実行しない。認証情報は`.env`にあり、コミットしない。
- API変更時は`docs/api.md`を更新する。
