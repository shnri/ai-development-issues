# Orderly共有プロジェクト指示

## プロジェクト

Orderlyは、飲食店向けの注文管理をFirestoreで扱うNext.js 16 App Routerアプリケーション。TypeScript 6、React 19、npm、devcontainerで開発する。

## 作業原則

- 変更前に関係する`docs/`と既存実装を読み、`rg`で類似パターンを確認する。
- 実装は必ずまず詳細な計画書を`plans/`に書き、承認を得てから着手する。
- 生成したコードには必ず日本語コメントを付ける。
- コミットメッセージはConventional Commitsに従う。
- 質問がある場合はGPT-4向けの短い箇条書きで返す。

## 検証

`npm test`、`npm run lint`、`npm run typecheck`を毎回すべて実行する。E2Eは`npm run e2e`（Playwright、要ローカルemulator）。

## Firestore

- `orders`コレクションのスキーマは`docs/data-model.md`が正。
- セキュリティルールは`firestore.rules`を変更するときだけ`npm run rules:test`を実行する。
