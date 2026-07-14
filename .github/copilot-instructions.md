# Copilot Instructions (Router)

## Path-scoped Instructions

アプリケーション固有のルールは `.github/instructions/` で定義。

要点:

- このファイルに具体的な実装指示や細かい制約を書かないでください。あくまで各フォルダのルールファイルへ誘導する役目のみ持ちます。
- `.github/instructions/` が存在する場合は、必ずそちらを優先して参照してください。フォルダ単位の指示がプロジェクトルールになります。

参照先（必ず確認する）:

- `.github/instructions/backend.instructions.md` - バックエンド（FastAPI）用の詳細ルール
- `.github/instructions/frontend.instructions.md` - フロントエンド（Next.js）用の詳細ルール
- `README.md` - プロジェクト全体の概要とセットアップ手順

運用ルール（簡潔）:

1. 変更を行う前に、該当の `.instructions.md` を読み、そこに従ってください。
2. `.instructions.md` に矛盾がある場合、まずそのサブフォルダの責任者に確認の上で調整してください。
