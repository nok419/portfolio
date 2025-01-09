# 青空文庫による物語表現の数理分析

## プロジェクト概要
本プロジェクトは青空文庫の小説テキストを用いて、日本語の物語表現における単語の意味的関係性を数理的に分析するものです。Word2Vecを使用して単語の分散表現を学習し、物語表現における単語の意味的な類似性や関係性を定量的に把握することを目指しています。

## システム構成
- データ収集: 青空文庫スクレイピングモジュール
- テキスト前処理: 正規化・形態素解析
- 分析: Word2Vecによる分散表現学習

### 主要コンポーネント
1. スクレイピングモジュール（AozoraCorpus.py）
   - 青空文庫からのテキスト収集
   - 作家別テキストの整理保存

2. テキスト処理モジュール（main.py）
   - MeCabによる形態素解析
   - 品詞別フィルタリング
   - テキスト正規化

## 必要環境
```txt
Python 3.6以上
MeCab
neologdn
glob
```

## インストール方法
```bash
# 必要ライブラリのインストール
pip install mecab-python3
pip install neologdn

# MeCabの辞書のインストール
# Windows: https://taku910.github.io/mecab/#download
# Linux/Mac: apt-get install mecab-ipadic-utf8
```

## 使用方法

### 1. データ収集
```python
# 青空文庫からのテキスト収集
python AozoraCorpus.py
# または
from AozoraCorpus import AozoraCorpus
corpus = AozoraCorpus()
corpus.fit(url="https://www.aozora.gr.jp/index_pages/person_a.html")
corpus.run()
```

### 2. テキスト処理
```python
python main.py
```

### 出力ファイル
- doshi.log: 抽出された動詞
- keyoshi.log: 抽出された形容詞
- meishi.log: 抽出された名詞
- as.log: 分かち書きテキスト

## 処理フロー
1. テキストファイルの読み込み
2. neologdnによる正規化
3. MeCabによる形態素解析
4. 品詞フィルタリング
   - 名詞（一般、形容動詞語幹）
   - 動詞（自立）
   - 形容詞
5. 結果の保存

## 注意事項
- 青空文庫のサーバに負荷をかけないよう、適切なアクセス間隔を設定してください
- アクセス制限が発生した場合は、一定時間待機後に再試行してください
- 収集したテキストデータの利用は研究目的に限定してください

## データの取り扱い
- 青空文庫のテキストは著作権の切れた作品のみを使用
- 解析結果の公開時は出典を明記
- 商用利用は不可

## 技術的詳細
### 形態素解析の設定
- 7文字未満の単語のみを対象
- 特定の品詞と活用のみを抽出
- wakati形式での出力

### ファイル保存形式
```
[ファイル名]
抽出された単語列
```

## 将来の展望
- 時代別の言葉の使われ方の分析
- 作家ごとの文体特徴の抽出
- 物語構造の数理的分析

## トラブルシューティング
1. MeCabのインストールエラー
   - 適切な辞書パスの設定確認
   - 文字コードの確認（UTF-8推奨）

2. スクレイピングの失敗
   - ネットワーク接続の確認
   - 適切なアクセス間隔の設定
   - 一時ファイルの確認

## 参考文献
1. 青空文庫: https://www.aozora.gr.jp/
2. MeCab: https://taku910.github.io/mecab/
3. Word2Vec: Mikolov et al. (2013)

## 開発年
2022年

## ライセンス
研究目的での利用に限り許可