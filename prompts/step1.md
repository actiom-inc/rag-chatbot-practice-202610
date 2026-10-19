# 通常のLLMチャット

このリポジトリを確認して `app.py` のみを編集してください。ほかの既存ファイルは変更しないでください。

## 依頼
Streamlitでシンプルなチャット画面を作ってください。ユーザーの質問を `practice.llm.generate_reply(messages)` に渡し、回答を表示してください。会話履歴は `st.session_state` に保持し、過去のやり取りも表示してください。利用中のプロバイダーとモデル名は `practice.settings` から取得してください。APIエラー時にはブラウザ上にメッセージを表示してください。APIキーの値を表示したり、コードへ書き込んだりしないでください。

## 完了条件
`docker compose up -d` で起動し、質問への回答が表示され、2回以上やり取りできること。

## 動かない場合
`docker compose run --rm --user 0:0 app python scripts/restore_checkpoint.py step1` で完成版に復帰できます。作業ファイルは退避されます。
