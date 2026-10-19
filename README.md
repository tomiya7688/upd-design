# UPD Design

**UPD は、アプリケーションの仕事を UI・Process・Data の3つに分ける設計の考え方です。**

大切なのは、フォルダやクラスの名前ではなく、**それぞれが担当する仕事を混ぜないこと**です。

| 層 | 担当する仕事 |
| --- | --- |
| **UI** | 入力の受け取りと結果の表示 |
| **Process** | アプリのルールに基づく判断・計算・処理 |
| **Data** | データの取得・保存 |

## 守るべき境界

UPD の3つの層は、それぞれの仕事を越えてはいけません。特に、**UI と Data が直接やり取りする構成は認めません。**

    要求：UI → Process → Data
    結果：Data → Process → UI

これは仕事の受け渡しを表すものであり、特定のクラス構成や通信方法を指定するものではありません。

## ドキュメント

### [利用者向け](docs/users/README.md)

- [UPD の考え方](docs/users/README.md) — 何を分離するのか
- [UPD を使うメリット](docs/users/benefits.md) — 何が改善し、どこに注意するか
- [具体例で理解する UPD](docs/users/examples.md) — 検索、保存、ゲームの例

### [開発者向け](docs/developers/README.md)

- [開発者ガイド](docs/developers/README.md) — 実装時の基本方針
- [必ず守る境界](docs/developers/boundaries.md) — 禁止事項と違反例
- [処理の分け方と受け渡し](docs/developers/implementation.md) — 判断の目安と処理の流れ
- [レビューのチェックリスト](docs/developers/review-checklist.md) — 境界を確認する項目
- [境界チェックツールの利用](docs/developers/checker.md) — 検査の導入と限界

## ツール

[`tools/`](tools/README.md) で UPD の境界違反を検出するチェックツールを開発します。違反時はエラーにし、CI を失敗させます。

現在は **Python の import による層間依存**を検査する初期ツールを提供します。すべての責務違反を検出できるわけではありません。範囲と使い方は [ツールの説明](tools/README.md)を参照してください。

## ライセンス

[MIT License](LICENSE)
