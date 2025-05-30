# Historical Network Analysis Tool

## 概要
このプロジェクトは、歴史的な人物関係のデータを可視化・分析するためのネットワーク分析ツールです。立命館大学アート・リサーチセンター(ARC)に提供され、同センターのデジタルツールの一部として実装されています。

## 主な機能
- CSVファイルから人物関係データの読み込み
- 時期、カテゴリーによるデータフィルタリング
- 共起関係に基づくネットワークの構築
- インタラクティブな可視化インターフェース
- ノード（人物）情報のポップアップ表示
- ネットワーク統計情報の算出

## システム構成
### フロントエンド（GUI）
- Tkinterを使用したデスクトップアプリケーション
- ファイル選択、フィルター設定、実行制御の機能を提供
- 分析結果の表示機能

### バックエンド（分析エンジン）
- NetworkX: ネットワーク分析ライブラリ
- PyVis: ネットワーク可視化ライブラリ
- Pandas: データ処理ライブラリ

### 主要ファイル構成
- `arc_network.py`: メインアプリケーション
- `add_click_macro_update.py`: 可視化用HTMLファイルのカスタマイズスクリプト
- `requirements.txt`: 依存ライブラリ一覧

## 技術的特徴
1. ネットワーク分析
   - 共起関係の抽出とカウント
   - 次数分布などのネットワーク統計量の計算
   - フィルタリングによる部分ネットワークの抽出

2. データ処理
   - CSVファイルの動的な列数対応
   - 欠損値処理
   - 日付およびカテゴリーベースのフィルタリング

3. 可視化
   - インタラクティブなネットワーク表示
   - カスタムポップアップによる詳細情報表示
   - 物理シミュレーションによるレイアウト制御

## 実行環境
- Python 3.8以上
- 必要なライブラリは`requirements.txt`に記載

## 非公開情報・依存関係の扱い
- 実データおよび分析結果は非公開
- データベースアクセス情報は設定ファイルで管理
- 外部システム連携用のAPIキーは別途管理

## 今後の展開
現在、フロントエンド部分のリファクタリングが進行中です。最新版は立命館ARCのデジタルツールページにて公開予定です。

## 留意事項
- 本ツールは研究目的での使用を想定しています
- 実データの取り扱いには適切な許諾が必要です
- 機能拡張時は互換性の維持に注意が必要です

## 参考URL
- [立命館ARC デジタルツール](https://www.arc.ritsumei.ac.jp/lib/vm/DigitalTools/arc-online-tools/)
