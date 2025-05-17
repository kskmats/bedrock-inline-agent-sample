FROM python:3.12-slim

WORKDIR /app

# requirements.txtのコピーとパッケージのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードのコピー
COPY src .

# pythonコマンドをENTRYPOINTに設定し、実行時に引数を渡せるようにする
ENTRYPOINT ["python"]
# デフォルト引数（指定がない場合にはmain.pyを実行）
CMD ["main.py"]