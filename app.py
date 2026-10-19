"""STEP 0: 参加者向け雛形。STEP 1からAIにコードを書いてもらいます。"""
import streamlit as st

st.set_page_config(page_title="RAGチャットボット ハンズオン", page_icon="📚")
st.title("RAGチャットボット ハンズオン")
st.info("STEP 0 完了。次は prompts/step1.md をAIコーディングツールに渡してください。")
st.chat_input("STEP 1で会話機能を実装します", disabled=True)
