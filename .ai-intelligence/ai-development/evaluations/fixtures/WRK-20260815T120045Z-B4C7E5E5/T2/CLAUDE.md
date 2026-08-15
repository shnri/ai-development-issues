# Claude Code向け指示

Orderlyは飲食店向け注文管理のNext.js 16 App Routerアプリ。TypeScript 6、React 19、npm。

## ルール

- 変更前に関係する`docs/`と既存実装を読み、`rg`で類似パターンを確認する。
- 依頼された範囲だけを変更する。
- コミットメッセージはConventional Commitsに従う。
- 変更後は必ず`npm test`と`npm run lint`と`npm run typecheck`と`npm run build`をすべて実行する。
- コードを書く前に必ず計画をmarkdownで提示し、承認を待つ。

## Firestore

- `orders`のスキーマは`src/types/order.ts`が正。
- `firestore.rules`を変更したときは`npm run rules:test`を実行する。
