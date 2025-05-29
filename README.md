月次売上ダッシュボード

この Streamlit アプリは、架空の売上データを用いてカテゴリ別・月別の売上分析を行うインタラクティブなダッシュボードです。

## 機能一覧
カテゴリ別売上推移（折れ線グラフ）
月次売上（棒グラフ）
売上構成比（円グラフ）
売上と利益の相関（散布図）
売上のばらつき（箱ひげ図）
売上と利益の比較（サブプロット）
カテゴリ別売上の時系列アニメーション
売上と利益率の2軸グラフ
全体俯瞰のヒートマップ

## ファイル構成
monthly_sales_dashboard/
├── app.py               # Streamlitアプリ本体
├── sample_sales_data.csv # 架空の売上データ
├── requirements.txt      # 依存パッケージ一覧
└── README.md             # 本ドキュメント

## 実行方法
pip install -r requirements.txt
streamlit run app.py
