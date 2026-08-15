# Orderly共有プロジェクト指示

Orderlyは飲食店向け注文管理のNext.js 16 App Routerアプリ。TypeScript 6、React 19、npm、devcontainer。

## 作業原則

- 変更前に関係する`docs/`と既存実装を読み、`rg`で類似パターンを確認する。
- 依頼された範囲だけを変更し、依頼外のrefactor・依存追加は提案に留める。
- 完了報告はそのセッションのテスト出力・diffに基づき、未実行の検証は未実行と書く。
- コミットメッセージはConventional Commitsに従う。
- 質問がある場合はGPT-4向けの短い箇条書きで返す。

## 検証

変更の影響に応じて`npm test`、`npm run lint`、`npm run typecheck`を実行する。E2Eは`npm run e2e`（要ローカルemulator）。

## Firestore

- `orders`のスキーマは`docs/data-model.md`が正。
- `firestore.rules`を変更したときだけ`npm run rules:test`を実行する。
