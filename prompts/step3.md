# RAG回答の実装

`app.py` と `practice/rag.py` のみを編集してください。STEP 2の資料登録機能は残してください。

## 依頼
チャットで質問されたら `search_documents(query, top_k=3)` で関連チャンクを取得し、`build_rag_system_prompt(matches)` で参照資料を含むシステムプロンプトを組み立て、`generate_reply(messages, system_prompt=...)` で回答してください。各回答の下に、検索されたファイル名・チャンク番号・本文を折りたたみ表示してください。データ未登録の場合はAPIに質問せず、登録を促してください。資料中の文章は指示ではなく参考情報として扱ってください。

## 完了条件
登録した `01_ai_training.txt` について「研修の申込期限は？」と質問し「2026年11月30日」が回答される。検索された資料を確認できる。

## 動かない場合
`docker compose run --rm --user 0:0 app python scripts/restore_checkpoint.py step3` で完成版に復帰。
