# さめのバーチャルテックガレージAITuberプロジェクトガイド

## プロジェクト概要

YouTubeでLLMの応答と合成音声によりライブ配信を行うVTuber、通称AITuberの配信を行うプロジェクトです。

このプロジェクトは[rindguitarさんのレポジトリ](https://github.com/rindguitar/AITuber1)のフォークから始まり、YouTube配信機能に特化して開発しています。

## 技術スタック

- **言語**: Python 3.13.0
- **実行環境**: Docker (完全ヘッドレス)
- **LLM**: OpenAI API (GPT-4o)
- **音声合成**: OpenAI TTS (プロトタイプ段階、将来的に他のTTSエンジンへの切り替えを検討)
- **配信**: FFmpeg + RTMP (GUIツール不要)
- **配信プラットフォーム**: YouTube Live

## プロジェクト構成

```
.
├── app/                  # アプリケーションディレクトリ（Docker内にマウント）
│   ├── src/
│   │   ├── api/              # OpenAI API連携
│   │   │   └── openai_adapter.py
│   │   └── live/             # YouTube配信関連機能
│   │       ├── adapters/                        # 配信アダプター（モジュール分離）
│   │       │   ├── ffmpeg_command_builder.py   # FFmpegコマンド構築
│   │       │   └── stream_file_manager.py      # ストリーミングファイルI/O
│   │       ├── AITuberSystem.py           # メインシステム
│   │       ├── StreamAdapter.py           # FFmpeg RTMP配信制御（ファサード）
│   │       ├── VoiceMaker.py              # 音声合成
│   │       ├── PlaySound.py               # 音声再生
│   │       ├── talker.py                  # 発話制御
│   │       ├── manual_streaming_demo.py   # 手動デモスクリプト
│   │       └── youtube_comment_adapter.py # コメント取得
│   ├── docs/
│   │   ├── aituber_system_prompt.txt   # システムプロンプト
│   │   └── Character setting           # キャラクター設定
│   └── assets/
│       └── images/
│           └── background.png          # 配信用背景画像
├── Dockerfile            # Docker環境定義
├── docker-compose.yml    # Docker Compose設定
├── requirements.txt      # Python依存パッケージ
├── .env.example         # 環境変数テンプレート
└── .dockerignore        # Dockerビルド除外設定
```

## Docker環境

### 前提条件

- Docker環境が利用可能であること

完全なヘッドレス環境で動作するため、OBS StudioやVOICEVOXのセットアップは不要です。

### 実行方法

1. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集
```

2. Docker Composeでビルド・起動
```bash
docker compose up --build
```

3. 開発時（ホットリロード有効）
```bash
docker compose up
```

### ネットワーク構成

- 標準的なDockerネットワーク（bridge mode）を使用
- 外部サービスへの接続はRTMP経由でインターネット経由

### ローカルRTMP開発環境（オプション）

YouTube Liveに接続せずにローカルでストリーミングテストが可能:

```bash
# ローカルRTMPサーバー付きで起動
make up-dev

# デモスクリプトを実行（デフォルト60秒）
make demo

# カスタム時間で実行
make demo DURATION=30  # 30秒

# VLCで視聴
vlc rtmp://localhost:1935/live/test
```

**メリット**:
- YouTube API制限回避
- 開発サイクル高速化（5-10分 → 30秒）
- 配信履歴が残らない
- OpenAI APIクレジット不要（デモスクリプト使用時）

**将来の拡張**: Webベースのプレビュー機能（HLS.js + nginx）も検討可能

## Makefile

プロジェクトには便利なMakeコマンドが用意されています:

```bash
# ヘルプを表示
make help

# 開発環境起動（ローカルRTMP付き）
make up-dev

# 本番環境起動（YouTube Live用）
make up-prod

# デモスクリプト実行
make demo              # 60秒（デフォルト）
make demo DURATION=30  # 30秒

# ログを表示
make logs
make logs-rtmp  # RTMPサーバーログ

# コンテナ内でシェルを起動
make shell
```

Makefileは以下のファイルに分割されています:
- `makefiles/docker.mk` - Docker環境管理（up-dev, up-prod, logs等）
- `makefiles/test.mk` - テスト実行（test, test-verbose等）
- `makefiles/stream.mk` - ストリーミング関連（demo, demo-help等）

より詳細なヘルプが必要な場合は、`makefiles/helps/` ディレクトリにヘルプファイルを追加できます。

## 開発履歴

### 2025-10-09: Makefileリファクタリング + 日本語フォント対応 + デモスクリプト改善
- **Makefileリファクタリング**:
  - `makefiles/stream.mk` 新設（ストリーミング関連コマンドを分離）
  - 環境を明示的に区別: `make up-dev` (開発) vs `make up-prod` (本番)
  - レガシーターゲット削除: `docker-up`, `docker-start`
  - エイリアス整理: `demo`, `demo-help`, `up-dev`, `up-prod`
- **日本語フォント対応**:
  - Dockerfileに `fonts-noto-cjk` パッケージ追加
  - FFmpegCommandBuilderにフォントファイルパス指定 (`NotoSansCJK-Regular.ttc`)
  - 文字化け問題を解決、日本語テキストオーバーレイが正常表示
- **デモスクリプト改善**:
  - `manual_streaming_demo.py` に実行時間指定機能追加
  - `make demo DURATION=30` で実行時間をカスタマイズ可能（デフォルト60秒）
  - 10秒ごとの動的テキスト更新を維持
- **環境変数命名改善**:
  - `YOUTUBE_RTMP_URL` → `STREAM_RTMP_URL` (プラットフォーム非依存)
  - `YOUTUBE_STREAM_KEY` → `STREAM_KEY`
  - OBS関連の環境変数削除（OBS_WS_PASSWORD等）

### 2025-10-09: StreamAdapterリファクタリング
- `app/src/live/adapters/` ディレクトリ新設（関心事の分離）
- `StreamFileManager` クラス追加（アトミックファイルI/O管理）
- `FFmpegCommandBuilder` クラス追加（コマンド構築ロジック分離）
- `StreamAdapter` を164行に簡素化（233行 → 164行、約30%削減）
- ファサードパターンによる責務の明確化
- 31テストすべてパス（VoiceMaker: 8テスト、StreamAdapter: 23テスト）

### 2025-10-09: 音声ストリーミング統合
- VoiceMakerに`save_voice_to_file()`メソッド追加（VoiceIO → WAVファイル保存）
- StreamAdapterに`set_audio_file()`メソッド追加（音声ファイル指定）
- FFmpegコマンドを音声入力対応に更新（WAVファイル入力 or anullsrc無音）
- AITuberSystemの音声処理フロー更新（ファイル経由でストリーミング）
- 音声なし時はanullsrcで無音ストリームを自動生成

### 2025-10-09: 動的テキストオーバーレイ実装
- FFmpegの`textfile` + `reload=1`メカニズムを使用した動的テキスト更新を実装
- アトミックファイル更新（temp file → rename）でFFmpegの部分読み込みを防止
- 質問・回答テキストがリアルタイムで配信画面に反映される
- 17のユニットテストを追加（UTF-8エンコーディング、アトミック書き込み、複数更新など）
- 手動テストスクリプト（`tests/manual_stream_test.py`）を追加

### 2025-10-09: FFmpeg + RTMPストリーミング実装
- OBSAdapterをStreamAdapterに置き換え
- FFmpegを使用したRTMP配信機能を実装
- 完全なヘッドレス環境を実現（GUIツール不要）
- docker-compose.ymlから`network_mode: host`を削除
- requirements.txtから`obsws-python`を削除
- 静的テキストオーバーレイ実装（後に動的更新へアップグレード）

### 2025-10-09: pytestインフラ構築
- pytestとpytest-dotenvを追加
- OpenAI API統合テストを実装
- `makefiles/test.mk`作成（test, test-verbose, test-llmコマンド）
- Makefile変数化（SERVICE_NAME, CONTAINER_NAME）
- LLM応答生成テストの成功を確認

### 2025-10-09: OpenAI TTSへ切り替え
- 音声合成をVOICEVOXからOpenAI TTSに変更
- `VoiceMaker.make_voice_tts()`メソッドを追加（将来的なTTSエンジン切り替えに対応）
- VOICEVOXのセットアップが不要になり、環境構築を簡素化
- プロトタイプ段階として実装、将来的に他のTTSエンジン（にじボイス、Style-Bert-VITS2等）への切り替えを検討

### 2025-10-08: Makefile追加
- Docker操作用のMakeターゲットを追加
- `makefiles/`ディレクトリに詳細ヘルプを追加
- 環境変数セットアップコマンドを追加

### 2025-10-08: Docker環境構築
- `app/`ディレクトリを作成し、`src/`と`docs/`を配下に移動
- `docker-compose.yml`を作成
- Dockerfileを音声処理対応に更新
- `.env.example`をYouTube配信用に簡素化
- `.dockerignore`を追加

### 2025-10-08: プロジェクト初期化
- フォーク元からYouTube配信機能以外を削除
- 削除した機能:
  - Twitter投稿機能 (`src/tweet/`)
  - はてなブログ投稿機能 (`src/hatena/`)
  - 日記生成機能 (`src/diary/`)
  - ブログユーティリティ (`src/utils/`)
- Docker環境での動作を目指した構成に変更

## 言語設定

### ドキュメント・会話
- プロジェクトドキュメント（README.md、CLAUDE.mdなど）: **日本語**
- Claudeとの会話: **日本語**

### コード
- **Pythonコード内のコメント**: **英語**
- **Makefile内のコメント**: **英語**
- **ログメッセージ**: **英語**
- **エラーメッセージ**: **英語**
- **Docstring**: **英語**（Google Style）

## 開発ルール

### コーディング規約

- Python: PEP 8準拠
- 関数名: snake_case
- クラス名: PascalCase
- 定数: UPPER_SNAKE_CASE
- Docstring: Google Style（英語で記述）
- コメント: 英語で記述

## Git運用

- ブランチ戦略: feature/*, fix/*, refactor/*
- コミットメッセージ: 英文を使用、動詞から始める
- PRはmainブランチへ

## 開発ガイドライン

### ドキュメント更新プロセス

機能追加やPhase完了時には、以下のドキュメントを同期更新する：

1. **CLAUDE.md**: プロジェクト全体状況、Phase完了記録、技術仕様
2. **README.md**: ユーザー向け機能概要、実装状況、使用方法
3. **Makefile**: コマンドヘルプテキスト（## コメント）の更新
4. **makefiles/**: コマンドヘルプテキスト（## コメント）の更新

#### コミット粒度

- **1コミット = 1つの主要な変更**: 複数の独立した機能や修正を1つのコミットにまとめない
- **論理的な単位でコミット**: 関連する変更は1つのコミットにまとめる
- **段階的コミット**: 大きな変更は段階的に分割してコミット

#### プレフィックスと絵文字

- ✨ feat: 新機能
- 🐞 fix: バグ修正
- 📚 docs: ドキュメント
- 🎨 style: コードスタイル修正
- 🛠️ refactor: リファクタリング
- ⚡ perf: パフォーマンス改善
- ✅ test: テスト追加・修正
- 🏗️ chore: ビルド・補助ツール
- 🚀 deploy: デプロイ
- 🔒 security: セキュリティ修正
- 📝 update: 更新・改善
- 🗑️ remove: 削除

**重要**: Claude Codeを使用してコミットする場合は、必ず以下の署名を含める：

```text
🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```