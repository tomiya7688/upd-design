# UPD 境界チェックツール

[English](en/README.md)

UPD の境界違反を検出したら、チェックを失敗させるためのツールです。[必ず守る境界](../docs/developers/境界.md) が規則の本文です。

## 対応言語（初期段階）

| 言語 | 拡張子 | 現時点で解析する構文 |
| --- | --- | --- |
| Python | .py | import / from / 一部の定数による動的 import（Python AST） |
| C# | .cs | 名前空間宣言と using（global / 別名も含む） |
| Rust | .rs | crate:: / super:: による明示的な参照 |
| Go | .go | go.mod に基づくローカルパッケージの import |
| Kotlin | .kt / .kts | package 宣言と import |
| C++ | .cpp / .cc / .cxx / .h / .hpp / .hh / .hxx | ダブルクォート形式のローカル #include |
| なでしこ3 | .nako3 | !「ファイル」を取り込む / !『ファイル』を取り込む |

**各言語の完全対応ではありません。** 現在は代表的な静的参照構文の検出に限ります。なでしこ1（.nako / .nako2）は未対応としてエラーにします。

## 境界の規則

| 参照元 | 許可される層 | 禁止される層 |
| --- | --- | --- |
| UI | UI、Process、Shared | Data |
| Process | Process、Data、Shared | UI |
| Data | Data、Shared | UI、Process |
| Shared（任意） | Shared | UI、Process、Data |

Shared は第4の処理層ではありません。共有部品を通して別の層の仕事へ直接アクセスしてはいけません。

## 設定

検査対象プロジェクトに upd-check.json を作成します。次の構成は例であり、フォルダ名を固定する規則ではありません。

~~~json
{
  "source_roots": ["src"],
  "layers": {
    "ui": ["src/ui"],
    "process": ["src/process"],
    "data": ["src/data"],
    "shared": ["src/shared"]
  }
}
~~~

指定したディレクトリは実在している必要があります。shared を使わない場合は省略できます。検査対象ソースは source_roots の範囲に収めてください。

## 実行

Python 3.11 以上の標準ライブラリだけで動作します。

~~~sh
python /path/to/upd-design/tools/check_layers.py --root /path/to/project --config upd-check.json
~~~

C#・Kotlin は検査対象にある名前空間や package 宣言を照合します。Go は検査対象プロジェクト内の go.mod が必要です。Rust はディレクトリを用いてモジュールの位置を推定します。C++・なでしこ3は実在するローカルファイルへの参照を照合します。

## エラーと終了コード

| 終了コード | 意味 |
| --- | --- |
| 0 | **検査できた構文の範囲で**違反を検出しなかった |
| 1 | 違反・未分類ソース・未対応拡張子・解析不能・検査対象なし |
| 2 | 設定ファイル等の不備で検査を開始できなかった |

例：

~~~text
src/ui/View.cs:1: UPD100 禁止された層間依存: ui → data (Demo.Data)
~~~

違反を解消するまで対象プロジェクトのCIを失敗にします。利用先プロジェクトでの実行をCIの必須チェックに設定してください。

## できないこと・注意点

**チェックに合格したことは、UPD のすべての規則を満たす証明ではありません。** 例えば、UI の内部に割引計算を直接書いても、import の検査だけでは分かりません。

言語ごとの主な未対応範囲は次のとおりです。

- C#：完全修飾名の直接参照、条件付きコンパイルや生成コードの意味解析。
- Rust：マクロ、グループ化した use、path 属性、複雑なモジュール構成。
- Go：go.mod のないローカル構成、ビルドタグ、生成コードや実行時の振る舞い。
- Kotlin：import を使わない完全修飾名による直接参照、実行時の呼び出し。
- C++：山括弧の include、マクロ、ビルドシステムの include path、関数の呼び出し関係。
- なでしこ3：外部プラグイン・URL・貯蔵庫の取り込み、実行時参照、取り込み以外の呼び出し。
- 共通：複数言語間の実行経路、コメントと文字列の完全な解析、アプリの責務の意味解析。source_roots に含まれないファイル、未知の拡張子は検査対象になりません。

**未対応の構文を検査済みと称さないこと。** 検査器を拡張し、各言語で正式な構文解析やビルド情報を利用するのが今後の課題です。

## テスト・CI

~~~sh
python -m unittest discover -s tools/tests -v
~~~

このリポジトリの GitHub Actions はチェックツール**自身のテスト**を実行します。利用プロジェクトの境界チェックは、そのプロジェクトのCIに実行コマンドを追加してください。

なでしこ3 の取り込み構文は[公式リポジトリ](https://github.com/kujirahand/nadesiko3)と[開発者による解説](https://qiita.com/kujirahand/items/bdbf611fc1f448e63bf9)を参考にしています。
