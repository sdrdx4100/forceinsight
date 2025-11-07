# ForceInsight

ForceInsight は車両の計測データを集約・分析・可視化・検索・ナレッジ化する Django ベースのプラットフォームです。Django Admin (テーマ: **django-jet-reboot**。社内文書では `django-jet-reboon` と表記される場合があります) と Django REST Framework を中心に、Plotly による対話的な可視化を管理画面とカスタムビューの両方で提供します。

## 主な機能

- **バックボーン管理**: 車両・ECU・センサー・試験コースなどのマスタ管理。
- **データセット管理**: MDF/MF4/CSV(dat) のメタデータ・チャネル情報・要約統計・プレビューを保存。
- **取込ワークフロー**: asammdf ベースのパーサと CSV(dat) スタブを備えた同期取込 (`ingestion.services.ingest_file`)。管理コマンドで疑似データを生成可能。
- **検索 API**: プロジェクト・車両・ラベル・チャネル・期間・テキストを組み合わせた絞り込みとファセット情報を返却。
- **可視化**: Plotly でダウンサンプリング済みプレビューを対話的に描画。SavedChart と Dashboard へ保存し再利用可能。
- **ナレッジ/履歴管理**: 検索や可視化操作を UsageLog として自動記録し、SavedSearch と連携。
- **エクスポート/運用**: プレビュー値の CSV エクスポートと簡易ヘルスチェックを提供。

## セットアップ手順 (venv 前提)

### 1. Python と仮想環境の準備

Python 3.12 以上を利用してください。

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. 依存パッケージのインストール

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 環境変数設定

必要に応じて `.env` を作成し、`SECRET_KEY` や `DATABASE_URL` を上書きできます。

```
DEBUG=True
SECRET_KEY=任意の値
DATABASE_URL=sqlite:///db.sqlite3
```

### 4. マイグレーションと管理ユーザー

```bash
python manage.py migrate
python manage.py createsuperuser  # 管理ユーザー作成
python manage.py loaddata fixtures/initial_data.json  # 初期マスタを投入
```

### 5. サンプルデータの取り込みと可視化確認

疑似 dat(CSV) を生成して MeasurementSet/ChannelMap を登録する管理コマンドです。

```bash
python manage.py load_sample_data --project Demo --vehicle DEMO-CAR
```

完了後は以下を実行し、管理画面・API・Plotly ビューを確認します。

```bash
python manage.py runserver
```

- http://127.0.0.1:8000/admin/ : django-jet-reboot テーマの管理画面。
- http://127.0.0.1:8000/api/schema/swagger-ui/ : OpenAPI ドキュメント。
- http://127.0.0.1:8000/visualizations/measurement/1/ : Plotly プレビュー (ID は取込結果に合わせて変更)。

### 6. REST API

`/api/` 配下に DRF の ModelViewSet を提供しています。主なエンドポイント:

- `/api/datasets/measurement-sets/`
- `/api/datasets/channel-maps/`
- `/api/search/measurement-sets/?project=Demo`
- `/api/analytics/saved-charts/`
- `/api/plotly/preview/<id>/`

### 7. 認証・権限

- カスタムユーザー `accounts.User` にロール (admin/data_steward/analyst/viewer) を付与。
- 行レベル権限は [django-guardian](https://django-guardian.readthedocs.io/) を利用可能です。PostgreSQL での運用時は以下の設定を追加し、`python manage.py migrate guardian` を実行してください。

```python
INSTALLED_APPS += ['guardian']
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
ANONYMOUS_USER_NAME = 'anonymous'
```

## 運用環境 (PostgreSQL) への移行

1. `pip install psycopg[binary]` (requirements に含まれています)。
2. `.env` で `DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DBNAME` を指定。
3. `python manage.py migrate` を再実行してスキーマを作成。
4. JSONB カラムに対しては `GIN` インデックス、全文検索には `pg_trgm` 拡張の導入を推奨します。

## Celery/Redis を用いた非同期化 (将来拡張)

現在の取込処理は同期実行ですが、以下の手順で Celery + Redis による非同期化が可能です。

1. `pip install celery[redis]` を追加。
2. `celery.py` をプロジェクト直下に配置し、`shared_task` で `ingestion.services.ingest_file` をラップ。
3. `docker run -p 6379:6379 redis:7` 等で Redis を起動。
4. `celery -A forceinsight worker -l info` を別ターミナルで実行し、Django 側から `.delay()` を呼び出すように変更。

## 代替可視化ライブラリ

Plotly を標準としていますが、Altair や Bokeh を用いた対話的可視化へ置き換えることも可能です。`analytics` アプリのビューで `fig.to_json()` を返却し、フロントで描画する構成にすると、ライブラリ切替が容易です。

## 社内 SSO 連携の雛形

- `django-allauth` や `python3-saml` を追加することで SAML/OIDC 認証が可能です。
- 社内の IdP に合わせて `LOGIN_REDIRECT_URL` や `LOGOUT_REDIRECT_URL` を設定し、`/sso/login/` などの URL を追加してください。

## テスト

```bash
pytest
```

主なテスト内容:

- 取込サービスが MeasurementSet/ChannelMap を生成すること。
- REST API/Plotly プレビュー/検索エンドポイントが正常応答すること。
- UsageLog の記録と SavedChart のモデル動作。

## ディレクトリ構成 (抜粋)

```
forceinsight/
├── accounts/            # カスタムユーザーと管理
├── analytics/           # Plotly ビュー・SavedChart/Dashboard
├── catalog/             # 車両等マスタ
├── datasets/            # MeasurementSet/Channel 定義
├── export/              # CSV エクスポート
├── ingestion/           # 取込パーサ・サービス・管理コマンド
├── knowledge/           # UsageLog/SavedSearch とユーティリティ
├── labeling/            # ラベル・アノテーション
├── ops/                 # ヘルスチェック
├── search/              # 検索 API
├── templates/           # 基本テンプレートと Plotly 埋め込み
├── fixtures/initial_data.json
└── tests/               # pytest ベースの自動テスト
```

## 参考

- Plotly: `plotly.io.to_html(fig, full_html=False, include_plotlyjs='cdn')` を利用し Django テンプレートへ埋め込み。
- asammdf: MDF/MF4 のチャネル抽出に利用。PostgreSQL 運用時は JSONB による柔軟なメタデータ格納が可能。
- 類似検索拡張: PostgreSQL + [pgvector](https://github.com/pgvector/pgvector) によりベクトル検索を導入することで、ドライバ挙動の類似度分析が可能になります。
