# Orderly共有プロジェクト指示

## プロジェクト

Orderlyは、飲食店向けの注文管理をFirestoreで扱うNext.js 16 App Routerアプリケーション。TypeScript 6、React 19、npm、devcontainerで開発する。

## 作業原則

- 変更前に関係する`docs/`と既存実装を読み、`rg`で類似パターンを確認する。
- 依頼された範囲だけを変更する。依頼外のrefactor、抽象化の追加、依存の追加、互換shimは行わず、必要なら提案として報告する。
- ユーザーの既存変更を保持する。
- 完了・進捗の報告は、そのセッションで実行したテスト出力・diff・コマンド結果に基づいて行い、未実行の検証は未実行と明記する。
- 生成したコードには必ず日本語コメントを付ける。
- 質問がある場合はGPT-4向けの短い箇条書きで返す。

## 検証

変更の影響に応じて`npm test`、`npm run lint`、`npm run typecheck`を実行する。E2Eは`npm run e2e`（Playwright、要ローカルemulator）。

## Firestore

- `orders`コレクションのスキーマは`docs/data-model.md`が正。
- セキュリティルールは`firestore.rules`を変更するときだけ`npm run rules:test`を実行する。
