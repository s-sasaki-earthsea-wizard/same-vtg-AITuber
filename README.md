# さめのバーチャルテックガレージ AITuber

## 概要

このプロジェクトは、[rindguitarさんのレポジトリ](https://github.com/rindguitar/AITuber1)のフォークから始まり、**YouTube配信機能に特化**したAITuberシステムです。

LLMの応答と合成音声を使用して、YouTubeライブ配信でコメントに自動応答するVTuberを実現します。

## 主な機能

- YouTube配信でのコメント取得と自動応答
- OpenAI APIを使用した自然な会話生成
- OpenAI TTSによる音声合成
- FFmpeg + RTMPによるヘッドレス配信

## 技術スタック

- **言語**: Python 3.13.0
- **実行環境**: Docker
- **LLM**: OpenAI API (GPT-4o)
- **音声合成**: OpenAI TTS
- **配信**: FFmpeg + RTMP (完全ヘッドレス)
- **配信プラットフォーム**: YouTube Live

## 必要な準備

### 1. YouTube配信設定

YouTube Studioでライブ配信を設定し、以下を取得:
- **Video ID**: 配信URL（配信ごとに変化）
- **Stream Key**: ライブ配信の設定から取得

### 2. APIキーの取得

- **OpenAI APIキー**: https://platform.openai.com/api-keys

## セットアップ方法

### 前提条件

- Docker環境が利用可能であること
- YouTube配信の設定が完了していること（Video ID、Stream Key）

### Docker Compose環境での実行（推奨）

1. リポジトリをクローン
```bash
git clone https://github.com/rindguitar/same-vtg-AITuber.git
cd same-vtg-AITuber
```

2. 環境変数の設定
```bash
make env-setup
# .envファイルを編集して必要な値を設定
```

3. 環境変数を確認
```bash
make env-check
```

4. Docker Composeでビルド・起動
```bash
make up
```

5. ログを確認
```bash
make logs
```

6. 停止
```bash
make down
```

### 便利なMakeコマンド

```bash
make help        # 利用可能なコマンドを表示
make env-setup   # .envファイルをセットアップ
make env-check   # 環境変数の設定を確認
make up          # ビルド・起動
make start       # 起動（ビルドなし）
make down        # 停止
make restart     # 再起動
make logs        # ログ表示
make shell       # コンテナ内でシェル起動
make clean       # コンテナ・イメージ・ボリュームを削除
```


### ローカル環境での実行

1. リポジトリをクローン
```bash
git clone https://github.com/rindguitar/same-vtg-AITuber.git
cd same-vtg-AITuber
```

2. パッケージのインストール
```bash
pip install -r requirements.txt
```

3. 環境変数の設定（次のセクションを参照）

4. 実行
```bash
python app/src/live/AITuberSystem.py
```

## 環境変数の設定

`.env`ファイルを作成し、以下の環境変数を設定してください:

```env
# OpenAI API
OPENAI_API_KEY="your-openai-api-key"

# YouTube配信設定
YOUTUBE_VIDEO_ID="your-youtube-video-id"

# YouTube RTMP配信設定
YOUTUBE_RTMP_URL="rtmp://a.rtmp.youtube.com/live2"
YOUTUBE_STREAM_KEY="your-stream-key"
```

## キャラクター設定のカスタマイズ

`app/docs/`ディレクトリ内のファイルを編集して、AITuberのキャラクターをカスタマイズできます:

- **Character setting**: キャラクターの基本設定（性格、口調など）
- **aituber_system_prompt.txt**: AITuberの応答システムプロンプト

## 注意事項

- YouTube配信のVideo IDとStream Keyは配信ごとに確認・更新が必要です
- 完全なヘッドレス環境で動作するため、GUIツール（OBS、VOICEVOX）は不要です
- キャラクター設定のカスタマイズは、LLMに手伝ってもらうことを推奨します

## ライセンスと参考文献

このプロジェクトは、書籍「AITuberを作ってみたらプロンプトエンジニアリングがよくわかった件」を基に開発されています。詳細な実装の意図については、同書籍を参照してください。

## 開発履歴

- **2025-10-09**: FFmpeg + RTMPストリーミング実装
  - OBSからFFmpeg + RTMPへ完全移行
  - ヘッドレス環境で完結する配信システムを実現
  - network_mode: host依存を削除
- **2025-10-09**: pytestインフラ構築
  - OpenAI API統合テストを追加
  - make test, make test-llmコマンド実装
- **2025-10-09**: OpenAI TTSへ切り替え
  - 音声合成をVOICEVOXからOpenAI TTSに変更
  - VOICEVOXのセットアップが不要になり、環境構築を簡素化
- **2025-10-08**: Makefile追加
  - Docker操作用のMakeターゲットを追加
  - `makefiles/`ディレクトリに詳細ヘルプを追加
  - 環境変数セットアップコマンドを追加
- **2025-10-08**: Docker環境構築
  - `app/`ディレクトリ構成に変更
  - `docker-compose.yml`を追加
  - Docker環境での実行に対応
- **2025-10-08**: プロジェクト初期化
  - YouTube配信機能に特化
  - Twitter投稿、はてなブログ投稿、日記生成機能を削除