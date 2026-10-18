# 元の設計との差分と検討事項

この文書は、`upd-commander-base-design` のどの考え方を引き継ぎ、Commander を前提にしたどの条件を外すかを記録します。元のリポジトリを変更するための手順書ではありません。

## 依頼で指定されたこと

新しいリポジトリを `tomiya7688/upd-design` とし、元の「Upd Commander base design」から「Commander base」を除いた設計として文書を作成します。説明は分かりやすい日本語で書きます。

本初版では「Commander base を除く」を、**Commander 中心の構成を必須にせず、UI・Process・Data の責務分離を設計の中心にすること**として解釈しています。単に製品名から単語を消すだけの変更にはしていません。

## 引き継ぐ考え方

| 内容 | UPD Design での扱い |
| --- | --- |
| UI / Process / Data の3層に仕事を分ける。 | 引き継ぎます。 |
| UI は入力と表示、Process は判断と計算、Data は取得と保存を担当する。 | 引き継ぎます。 |
| UI と Data が直接やり取りしない。 | 要求、結果、コード上の参照で守ります。 |
| Process が表示方法や保存先の操作を担当しない。 | 引き継ぎます。 |
| Data が画面操作や業務上の判断を担当しない。 | 引き継ぎます。 |
| Common / Shared は層に属さない共有領域であり、4つ目の処理層ではない。 | 引き継ぎます。 |
| 担当する仕事を小さく保つ。 | 推奨する考え方として残します。特定の分割方法は必須にしません。 |

## 外す前提と、本初版での整理方針

| 元の設計の前提 | 本初版での扱い |
| --- | --- |
| 各層を Commander・必要な Messenger・Processing で構成する。 | この役割の組み合わせを必須にしません。 |
| Commander が呼び出しを担当し、実処理を持たない。 | Commander の配置を必須にしないため、全実装に一律には適用しません。 |
| 層を越える要求と結果は Messenger を通す。 | Messenger は任意とし、層の境界そのものを守る方針に置き換えます。 |
| 別層の Processing を直接呼べない。 | UI → Process、Process → Data では、公開された窓口を直接呼ぶ構成も選べるものとして整理します。内部実装の自由な操作は認めません。 |
| Commander 固有の通信規則やチェッカー判定がある。 | そのまま移植せず、新しい設計に必要かを個別に検討します。 |

**Messenger を任意にすることと、公開された窓口の直接呼び出しを認めることは、依頼で個別に確定された仕様ではありません。** Commander を前提にしない設計として、本初版で採った整理方針です。これらは確認が必要な設計判断として残します。

Commander や Messenger を使うこと自体は禁止しません。任意の実装方法として採用しても、UPD の3層の責務と境界は守ります。

## 今回は移植しないもの

元のリポジトリのコード、チェッカー、開発補助ツール、CI 設定、第三者コンポーネントはコピーしていません。元の仕様書一式を、そのまま新仕様とみなすこともしません。

Commander に依存しない補助機能が元のリポジトリにあっても、この初版に含まれるとは限りません。今回の成果物は、設計の核を説明する日本語文書です。

## まだ決めていないこと

Messenger の任意化と窓口の呼び出し方の最終確認に加え、複数アプリケーションへの適用、機能が大きい場合の分割、非同期処理、トランザクション、チェッカーの対象規則と互換性は、今後の検討事項です。

文書を追加するときは、元の仕様から引き継ぐ内容と、新しく決める内容を分けて記録します。特に、元のチェッカーが出す判定を、そのまま UPD Design の違反とみなしてはいけません。

## 参照した元資料

参照元は [tomiya7688/upd-commander-base-design](https://github.com/tomiya7688/upd-commander-base-design) です。初版の整理では、`main` のコミット `12aeedf675102d27fb2107427aff274dc78662d6` を参照しました。

| 元資料 | 参照した内容 |
| --- | --- |
| [README](https://github.com/tomiya7688/upd-commander-base-design/blob/12aeedf675102d27fb2107427aff274dc78662d6/README.md) | 設計の目的と基本原則。 |
| [Architecture](https://github.com/tomiya7688/upd-commander-base-design/blob/12aeedf675102d27fb2107427aff274dc78662d6/docs/architecture.md) | 3層と役割を別の軸として捉える考え方。 |
| [Layer Specification](https://github.com/tomiya7688/upd-commander-base-design/blob/12aeedf675102d27fb2107427aff274dc78662d6/specification/layer-spec.md) | 各層の責務と、要求・結果の境界。 |
| [Dependency Rules](https://github.com/tomiya7688/upd-commander-base-design/blob/12aeedf675102d27fb2107427aff274dc78662d6/specification/dependency-rules.md) | コード上の参照と層間の依存。 |
| [Common / Shared Specification](https://github.com/tomiya7688/upd-commander-base-design/blob/12aeedf675102d27fb2107427aff274dc78662d6/specification/common-shared-spec.md) | 共有領域の範囲と禁止事項。 |
| [日本語ドキュメント執筆ガイド](https://github.com/tomiya7688/upd-commander-base-design/blob/12aeedf675102d27fb2107427aff274dc78662d6/docs/japanese-writing-guide.md) | 説明の順序、用語、規則の強さの書き分け。 |

元の著作権表示と MIT ライセンスは [LICENSE](../LICENSE) に保持しています。
