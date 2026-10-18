import streamlit as st
from practice import settings
from practice.llm import generate_reply

st.set_page_config(page_title="RAGチャットボット ハンズオン", page_icon="📚")
st.title("AIチャット（STEP 1）")
st.caption(f"Provider: {settings.PROVIDER} / Model: {settings.active_model()}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("質問を入力してください")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    try:
        reply = generate_reply(st.session_state.messages)
    except Exception as exc:
        st.error(f"回答の取得に失敗しました（API設定やネット接続を確認してください）: {type(exc).__name__}: {exc}")
        st.session_state.messages.pop()
    else:
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
