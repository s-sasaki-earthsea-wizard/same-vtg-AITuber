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
│   │       ├── AITuberSystem.py        # メインシステム
│   │       ├── StreamAdapter.py        # FFmpeg RTMP配信制御
│   │       ├── VoiceMaker.py           # 音声合成
│   │       ├── PlaySound.py            # 音声再生
│   │       ├── talker.py               # 発話制御
│   │       └── youtube_comment_adapter.py  # コメント取得
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

## Makefile

プロジェクトには便利なMakeコマンドが用意されています:

```bash
# ヘルプを表示
make help

# 環境変数をセットアップ
make env-setup

# Docker Composeで起動
make up

# ログを表示
make logs

# コンテナ内でシェルを起動
make shell
```

より詳細なヘルプが必要な場合は、`makefiles/helps/` ディレクトリにヘルプファイルを追加できます。

## 開発履歴

### 2025-10-09: FFmpeg + RTMPストリーミング実装
- OBSAdapterをStreamAdapterに置き換え
- FFmpegを使用したRTMP配信機能を実装
- 完全なヘッドレス環境を実現（GUIツール不要）
- docker-compose.ymlから`network_mode: host`を削除
- requirements.txtから`obsws-python`を削除

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