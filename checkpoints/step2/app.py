import streamlit as st
from practice import settings
from practice.llm import generate_reply
from practice.rag import document_count, index_document, search_documents

st.set_page_config(page_title="RAGチャットボット ハンズオン", page_icon="📚")
st.title("資料登録と検索（STEP 2）")
st.caption(f"Provider: {settings.PROVIDER} / Model: {settings.active_model()}")

with st.sidebar:
    st.header("資料を登録")
    uploaded = st.file_uploader("TXTファイルを選択", type=["txt"])
    if st.button("登録する", disabled=uploaded is None):
        try:
            content = uploaded.getvalue().decode("utf-8-sig")
            count = index_document(uploaded.name, content)
            st.success(f"{count}チャンクを登録しました")
        except (UnicodeDecodeError, ValueError) as exc:
            st.error(f"ファイルを確認してください: {exc}")
        except Exception as exc:
            st.error(f"登録に失敗: {type(exc).__name__}: {exc}")
    st.metric("保存済みチャンク", document_count())
    st.subheader("検索を試す")
    search_query = st.text_input("検索キーワード", "研修の申込期限")
    if st.button("類似検索"):
        try:
            matches = search_documents(search_query)
            if not matches:
                st.info("検索結果なし。先に資料を登録してください。")
            for hit in matches:
                st.caption(f"{hit['source']} / チャンク{hit['chunk']}")
                st.write(hit["text"])
        except Exception as exc:
            st.error(f"検索に失敗: {type(exc).__name__}: {exc}")

if "messages" not in st.session_state:
    st.session_state.messages = []
st.info("このSTEPではチャットはまだRAGに接続していません。STEP 3で接続します。")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
prompt = st.chat_input("通常チャットへの質問")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    try:
        reply = generate_reply(st.session_state.messages)
    except Exception as exc:
        st.error(f"APIエラー: {type(exc).__name__}: {exc}")
        st.session_state.messages.pop()
    else:
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
