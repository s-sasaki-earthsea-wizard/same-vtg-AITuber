# ベースイメージ
FROM python:3.13.0-slim

# 作業ディレクトリを指定
WORKDIR /app

# Install system dependencies (audio processing, video streaming, and Japanese fonts)
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    portaudio19-dev \
    ffmpeg \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# 必要なライブラリをrequirements.txtからインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
# appディレクトリの内容を/app配下にコピー
COPY app/ /app/

# Pythonパスを設定
ENV PYTHONPATH=/app/src

# Keep container running for testing and manual execution
CMD ["tail", "-f", "/dev/null"]