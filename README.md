# UPD Design

**UPD は、アプリケーションの仕事を UI・Process・Data の3つに分ける設計の考え方です。**

大切なのは、フォルダやクラスの名前ではなく、**それぞれが担当する仕事を混ぜないこと**です。

| 層 | 担当する仕事 |
| --- | --- |
| **UI** | 入力の受け取りと結果の表示 |
| **Process** | アプリのルールに基づく判断・計算・処理 |
| **Data** | データの取得・保存 |

たとえば商品検索では、検索欄と一覧表示は UI、検索条件の確認は Process、商品データの取得は Data が担当します。

## 守るべき境界

UPD の3つの層は、それぞれの仕事を越えてはいけません。特に、**UI と Data が直接やり取りする構成は認めません。**

    要求：UI → Process → Data
    結果：Data → Process → UI

この図は仕事の受け渡しを表すものであり、特定のクラス構成や通信方法を指定するものではありません。すべての操作が3層を通る必要はありませんが、他の層の仕事を横取りしてはいけません。

## ドキュメント

### [利用者向け](docs/users/README.md)

UPD を理解し、採用を考える人向けです。

- [UPD の考え方](docs/users/README.md) — 何を分離するのか
- [UPD を使うメリット](docs/users/benefits.md) — 何が改善し、どこに注意するか
- [具体例で理解する UPD](docs/users/examples.md) — 検索、保存、ゲームの例

### [開発者向け](docs/developers/README.md)

UPD に沿って実装・レビューする人向けです。

- [開発者ガイド](docs/developers/README.md) — 実装時の基本方針
- [必ず守る境界](docs/developers/boundaries.md) — 禁止事項と違反例
- [処理の分け方と受け渡し](docs/developers/implementation.md) — 判断の目安と処理の流れ
- [レビューのチェックリスト](docs/developers/review-checklist.md) — 境界を確認する項目

## ライセンス

[MIT License](LICENSE)
