# STEP 2 — TXT登録とベクトル検索（目安15分）

`app.py` と `practice/rag.py` のみを編集し、既存のチャット機能を残してください。共通部品 `practice.embeddings` および `practice.settings` は変更しないでください。

## 依頼
StreamlitのサイドバーにUTF-8のTXTファイルをアップロード・登録するUIを追加してください。 `practice.rag` に次の関数を実装してください。

- `split_text(text, chunk_size=250, overlap=40)`: 文字単位で分割
- `index_document(filename, text)`: チャンクをEmbeddingし、Chromaのローカル永続DBへupsert。IDを内容とファイル名から安定的に作る
- `document_count()`: 保存済みチャンク数
- `search_documents(query, top_k=3)`: 質問Embeddingで上位3件を類似検索し、本文・ファイル名・チャンク番号を返す

Chromaには `chromadb.PersistentClient(path=str(settings.CHROMA_PATH))` を利用してください。 `practice.embeddings.embed_passages` / `embed_queries` を呼び、コレクションはcosine距離にしてください。登録結果の件数と、検索結果の本文を画面に表示できるようにしてください。 `build_rag_system_prompt` はSTEP 3まで未実装で問題ありません。

## 完了条件
`samples/01_ai_training.txt` を登録するとチャンク件数が増える。検索窓で「申込期限」を検索すると関連文章が表示される。アプリ再起動後もチャンク件数が維持される。

## 動かない場合
`docker compose run --rm --user 0:0 app python scripts/restore_checkpoint.py step2` で完成版に復帰。
