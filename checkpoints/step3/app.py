import streamlit as st
from practice import settings
from practice.llm import generate_reply
from practice.rag import document_count, index_document, search_documents, build_rag_system_prompt

st.set_page_config(page_title="RAGチャットボット ハンズオン", page_icon="📚")
st.title("RAGチャット（STEP 3）")
st.caption(f"Provider: {settings.PROVIDER} / Model: {settings.active_model()}")

with st.sidebar:
    st.header("資料を登録")
    uploaded = st.file_uploader("UTF-8のTXTファイル", type=["txt"])
    if st.button("登録する", disabled=uploaded is None):
        try:
            content = uploaded.getvalue().decode("utf-8-sig")
            count = index_document(uploaded.name, content)
            st.success(f"{count}チャンクを登録しました")
        except Exception as exc:
            st.error(f"登録に失敗: {type(exc).__name__}: {exc}")
    st.metric("保存済みチャンク", document_count())

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
    if message["role"] == "assistant" and message.get("sources"):
        with st.expander("検索された資料"):
            for item in message["sources"]:
                st.caption(f"{item['source']} / チャンク{item['chunk']}")
                st.write(item["text"])

prompt = st.chat_input("登録資料について質問")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    try:
        matches = search_documents(prompt, top_k=3)
        if not matches:
            st.warning("先にTXTファイルを登録してください。")
        else:
            context = build_rag_system_prompt(matches)
            # 関連資料は質問ごとに検索し、現在のターンのsystem promptに含める
            prior = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages[-6:]
            ]
            reply = generate_reply(
                [*prior, {"role": "user", "content": prompt}],
                system_prompt=context,
            )
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": reply, "sources": matches})
            with st.chat_message("assistant"):
                st.write(reply)
            with st.expander("検索された資料"):
                for item in matches:
                    st.caption(f"{item['source']} / チャンク{item['chunk']}")
                    st.write(item["text"])
    except Exception as exc:
        st.error(f"質問の処理に失敗: {type(exc).__name__}: {exc}")
