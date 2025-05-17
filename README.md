# Bedrock Inline Agentサンプル

これはAWS Bedrock Inline Agentを実行するPythonプログラムのサンプルである。

## ファイル構成

- `Dockerfile`: Pythonアプリケーションを実行するためのDockerイメージ定義
- `main.py`: サンプルPythonプログラム（コマンドライン引数対応）
- `requirements.txt`: 依存パッケージの一覧
- `src/.env.example`: 環境変数設定のテンプレートファイル

## 前提

### アクセスキー/シークレットアクセスキー設定

`.env.example`ファイルをコピーして`.env`ファイルを作成し、AWSアクセスキー/シークレットアクセスキーを登録する。(us-east-1以外のリージョンを使う場合はリージョンも指定する)

```bash
cp src/.env.example src/.env
```

その後、`.env`ファイルを編集する。

## 使用方法

### Dockerイメージのビルド

以下のコマンドでDockerイメージをビルドする:

```bash
docker build -t python-sample .
```

### コンテナの実行

ビルドしたイメージからコンテナを実行する:

```bash
docker run python-sample
```

引数として実行するファイルを渡す場合:

```bash
docker run python-sample python call_sample_agent.py
```

## カスタマイズ

自分のPythonプログラムを実行したい場合は、以下の手順に従う:

1. `main.py`を自分のプログラムファイルに置き換えるか編集する
2. 必要に応じて`Dockerfile`を編集する（例：依存パッケージのインストール）
3. 再度Dockerイメージをビルドして実行する

## 依存パッケージの追加方法

外部パッケージが必要な場合は、`requirements.txt`ファイルに追加する:

```
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```