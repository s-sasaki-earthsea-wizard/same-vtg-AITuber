# さめのバーチャルテックガレージAITuberプロジェクトガイド

## プロジェクト概要

YouTubeでLLMの応答と合成音声によりライブ配信を行うVTuber、通称AITuberの配信を行うプロジェクトです。

このプロジェクトは[rindguitarさんのレポジトリ](https://github.com/rindguitar/AITuber1)のフォークから始まり、YouTube配信機能に特化して開発しています。

## 技術スタック

- **言語**: Python 3.13.0
- **実行環境**: Docker
- **LLM**: OpenAI API
- **音声合成**: VOICEVOX
- **配信制御**: OBS (OBS WebSocket)
- **配信プラットフォーム**: YouTube Live

## プロジェクト構成

```
.
├── src/
│   ├── api/              # OpenAI API連携
│   └── live/             # YouTube配信関連機能
│       ├── AITuberSystem.py        # メインシステム
│       ├── OBSAdapter.py           # OBS制御
│       ├── VoiceMaker.py           # 音声合成
│       ├── PlaySound.py            # 音声再生
│       ├── talker.py               # 発話制御
│       └── youtube_comment_adapter.py  # コメント取得
├── docs/
│   ├── aituber_system_prompt.txt   # システムプロンプト
│   └── Character setting           # キャラクター設定
├── Dockerfile            # Docker環境定義
├── requirements.txt      # Python依存パッケージ
└── .env.example         # 環境変数テンプレート

```

## 開発履歴

### 2025-10-08: プロジェクト初期化
- フォーク元からYouTube配信機能以外を削除
- 削除した機能:
  - Twitter投稿機能 (`src/tweet/`)
  - はてなブログ投稿機能 (`src/hatena/`)
  - 日記生成機能 (`src/diary/`)
  - ブログユーティリティ (`src/utils/`)
- Docker環境での動作を目指した構成に変更

## 言語設定

このプロジェクトでは**日本語**での応答を行ってください。コード内のコメント、ログメッセージ、エラーメッセージ、ドキュメンテーション文字列なども日本語で記述してください。

## 開発ルール

### コーディング規約

- Python: PEP 8準拠
- 関数名: snake_case
- クラス名: PascalCase
- 定数: UPPER_SNAKE_CASE
- Docstring: Google Style

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