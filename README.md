# Black-Scholes オプション計算ツール

<div align="center">

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io/)

</div>

## 📋 概要

Black-Scholesモデルを使用したオプション価格計算とインプライドボラティリティ（IV）算出のWebアプリケーションです。FastAPIによるバックエンドAPIとStreamlitによるインタラクティブなフロントエンドで構成されています。

> **Note**: このプロジェクトの開発環境は [a5chin/python-uv](https://github.com/a5chin/python-uv) をベースにしています。

### 主な機能

- ✅ **オプション価格計算**: コール/プットオプションの理論価格を計算
- 📊 **インプライドボラティリティ算出**: 市場価格からIVを逆算
- 📈 **インタラクティブなグラフ表示**: 権利行使価格に対する価格/IVの変化を可視化
- ⚡ **高速計算**: NumPy/SciPyによる効率的な数値計算

## 🚀 クイックスタート

### 前提条件

- Docker Desktop（Dev Container使用時）
- または、Python 3.10以上 + [uv](https://github.com/astral-sh/uv)

### Dev Containerでの起動（推奨）

1. **リポジトリのクローン**
```bash
git clone <repository-url>
cd <repository-name>
```

2. **VS Codeで開く**
```bash
code .
```

3. **Dev Containerで再度開く**
   - `⌘+⇧+P` (macOS) または `Ctrl+Shift+P` (Windows/Linux) でコマンドパレットを開く
   - `Dev Containers: Reopen in Container` を選択

4. **依存関係のインストール**
```bash
uv sync
```

5. **バックエンドの起動**
```bash
cd src/backend
uv run uvicorn main:app --reload --port 8000
```

6. **フロントエンドの起動**（別ターミナル）
```bash
cd src/frontend
uv run streamlit run app.py
```

7. **アクセス**
   - フロントエンド: http://localhost:8501
   - バックエンドAPI: http://localhost:8000
   - API ドキュメント: http://localhost:8000/docs

## 📁 プロジェクト構成

```
.
├── .devcontainer/
│   ├── devcontainer.json       # Dev Container設定
│   └── Dockerfile              # 開発環境のDockerイメージ
├── .github/
│   └── workflows/
│       ├── docker.yml          # Dockerビルドチェック
│       ├── pyright.yml         # 型チェック
│       ├── ruff.yml            # フォーマット・リントチェック
│       └── test.yml            # pytest実行
├── docs/                       # ドキュメント（MkDocs）
│   ├── about/                  # プロジェクトについて
│   ├── configurations/         # 設定ファイル解説
│   ├── getting-started/        # 開始ガイド
│   ├── guides/                 # 各種ガイド
│   ├── img/                    # 画像リソース
│   ├── stylesheets/            # カスタムスタイル
│   ├── usecases/               # ユースケース
│   └── index.md
├── src/
│   ├── backend/
│   │   ├── main.py             # FastAPI バックエンド
│   │   └── requirements.txt    # バックエンド依存関係
│   └── frontend/
│       ├── app.py              # Streamlit フロントエンド
│       └── requirements.txt    # フロントエンド依存関係
├── tests/                      # テストコード
│   ├── conftest.py
│   └── tools/
│       ├── test__config.py
│       ├── test__logger.py
│       └── test__tracer.py
├── tools/                      # ユーティリティツール
│   ├── config/                 # 設定管理
│   ├── logger/                 # ロギング
│   └── tracer/                 # トレーシング
├── .pre-commit-config.yaml     # pre-commitフック設定
├── Dockerfile                  # 本番環境用Dockerイメージ
├── mkdocs.yml                  # MkDocs設定
├── noxfile.py                  # Noxタスク設定
├── pyproject.toml              # プロジェクト設定・依存関係
├── pyrightconfig.json          # Pyright設定
├── pytest.ini                  # pytest設定
├── renovate.json               # Renovate設定
├── ruff.toml                   # Ruff設定
├── uv.lock                     # uvロックファイル
└── README.md
```

## 🛠️ 使い方

### 1. オプション価格計算

1. サイドバーで「オプション価格計算」を選択
2. パラメータを入力：
   - **株価 (S)**: 現在の原資産価格
   - **権利行使価格 中央値 (K)**: 計算する権利行使価格の中心
   - **権利行使価格 範囲 (±)**: Kの変動幅
   - **残存期間 (年)**: オプションの満期までの期間
   - **無リスク金利 (r)**: 年率の無リスク金利
   - **配当利回り (q)**: 年率の配当利回り
   - **ボラティリティ (σ)**: 原資産のボラティリティ
   - **オプション種別**: call（コール）または put（プット）
3. グラフで権利行使価格に対するオプション価格の変化を確認

### 2. インプライドボラティリティ計算

1. サイドバーで「インプライドボラティリティ計算」を選択
2. パラメータを入力（上記と同様）
3. **市場価格**: 観測されたオプションの市場価格を入力
4. グラフで権利行使価格に対するIVの変化を確認（ボラティリティ・スマイル）

## 🔧 開発

### 依存関係の管理

```bash
# すべての依存関係をインストール（開発用含む）
uv sync

# 本番環境用のみ
uv sync --no-dev

# パッケージの追加
uv add <package-name>

# 開発用パッケージの追加
uv add --dev <package-name>
```

### コードフォーマット

```bash
# フォーマット実行
uv run ruff format .

# リント実行
uv run ruff check . --fix
```

### テスト実行

```bash
# 全テスト実行
uv run pytest

# カバレッジ付き実行
uv run pytest --cov=src --cov-report=html
```

### 型チェック

```bash
uv run pyright
```

### pre-commit

コミット前に自動的にフォーマット・リント・型チェックを実行：

```bash
# pre-commitのインストール
uv run pre-commit install

# 手動実行
uv run pre-commit run --all-files
```

### ドキュメント生成

```bash
# MkDocsサーバーの起動
uv run mkdocs serve

# ドキュメントのビルド
uv run mkdocs build
```

## 📊 APIエンドポイント

### POST /calculate_prices

オプション価格を計算します。

**リクエスト:**
```json
{
  "S_list": [100.0],
  "K_list": [80, 85, 90, 95, 100, 105, 110, 115, 120],
  "T": 1.0,
  "r": 0.05,
  "sigma": 0.2,
  "q": 0.0,
  "option_type": "call"
}
```

**レスポンス:**
```json
{
  "S_list": [100.0],
  "K_list": [80, 85, 90, 95, 100, 105, 110, 115, 120],
  "prices": [[20.32, 18.45, 16.23, 13.87, 11.45, 9.12, 7.01, 5.21, 3.78]]
}
```

### POST /calculate_ivs

インプライドボラティリティを計算します。

**リクエスト:**
```json
{
  "S_list": [100.0],
  "K_list": [80, 85, 90, 95, 100, 105, 110, 115, 120],
  "T": 1.0,
  "r": 0.05,
  "price_list": [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
  "q": 0.0,
  "option_type": "call"
}
```

**レスポンス:**
```json
{
  "S_list": [100.0],
  "K_list": [80, 85, 90, 95, 100, 105, 110, 115, 120],
  "ivs": [[0.15, 0.16, 0.18, 0.19, 0.20, 0.21, 0.23, 0.25, 0.28]]
}
```

## 🐛 トラブルシューティング

### Ruffフォーマットが動作しない

1. `⌘+⇧+P` でコマンドパレットを開く
2. `Developer: Reload Window` を実行してウィンドウをリロード

### APIに接続できない

- バックエンドが起動しているか確認: `http://localhost:8000/docs`
- ポート8000が他のプロセスで使用されていないか確認
- `src/backend` ディレクトリから実行しているか確認

### IV計算が収束しない

- 市場価格が妥当な範囲内か確認（極端に高い/低い価格はNG）
- パラメータ（S, K, T, r）が現実的な値か確認
- オプションタイプ（call/put）が正しいか確認
- レスポンスに `null` が含まれている場合、その組み合わせでは収束しませんでした

### 配列の長さエラー（All arrays must be of the same length）

- バックエンドのレスポンス構造が正しいか確認
- `S_list` の長さが1の場合、`prices[0]` で最初の行を取得する必要があります
- フロントエンドのコードを最新版に更新してください

## 📚 参考資料

- [Black-Scholesモデル](https://ja.wikipedia.org/wiki/ブラック–ショールズ方程式)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

## 📖 詳細ドキュメント

詳細なドキュメントは `docs/` ディレクトリを参照してください：

- [Getting Started](docs/getting-started/index.md) - 環境構築ガイド
- [Configurations](docs/configurations/index.md) - 各種設定の詳細
- [Guides](docs/guides/index.md) - 開発ガイド
- [Use Cases](docs/usecases/index.md) - 各種ユースケース

ドキュメントサイトをローカルで起動：
```bash
uv run mkdocs serve
```

## 📝 ライセンス

このプロジェクトは2つの部分から構成され、それぞれ異なるライセンスが適用されます：

### アプリケーションコード
- **対象**: `src/backend/`, `src/frontend/` およびアプリケーション固有のロジック
- **ライセンス**: MIT License
- **著作権**: Copyright (c) 2025 Shintaro0105
- **詳細**: [LICENSE](LICENSE)

### 開発環境設定
- **対象**: `.devcontainer/`, `.github/`, `.vscode/`, `tools/`, 各種設定ファイルなど
- **ライセンス**: MIT License
- **著作権**: Copyright (c) 2024 a5chin
- **詳細**: [LICENSE-DEVCONTAINER](LICENSE-DEVCONTAINER)
- **基になったプロジェクト**: [python-uv](https://github.com/a5chin/python-uv) by a5chin

両方のライセンスともMITライセンスですが、著作権は各部分の作成者に帰属します。

## 🤝 コントリビューション

Issue・Pull Requestを歓迎します！

コントリビューションの際は以下を確認してください：
1. `uv run ruff format .` でコードをフォーマット
2. `uv run ruff check . --fix` でリントエラーを修正
3. `uv run pytest` でテストをパス
4. `uv run pyright` で型チェックをパス

---

<div align="center">
Built with ❤️ using FastAPI, Streamlit, and uv
</div>
