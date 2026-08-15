# CLAUDE.md — Ledgerly

Ledgerlyは家計簿SaaSのRails 7 API + React SPA。Ruby 3.3、Node 22、pnpm。

## 必ず守ること

- どんな小さな修正でも、着手前に「背景・方針・影響範囲・テスト計画」を含む計画を出力し、ユーザーの承認を待つ。
- 変更ごとに必ず`bundle exec rspec`と`pnpm test`と`pnpm lint`と`pnpm build`をすべて実行し、結果を全文貼り付ける。
- 思考過程を必ず段階的に表示し、各ステップで何を考えたかを説明する。
- コードを書くときは、将来の拡張に備えて必ずinterfaceとfactoryを用意する。
- 1回の返答は必ず2000文字以内。超える場合は分割する。
- Claude 3.5 Sonnetでは長いファイルを一度に編集すると壊れるので、100行ずつ編集する。

## リポジトリ

- API: `api/`（Rails）、SPA: `web/`（Vite）。
- DBマイグレーションは`api/db/migrate/`。本番DBに触るコマンドは絶対に実行しない。
- 認証情報は`.env`にあり、コミットしない。
