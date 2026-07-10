import streamlit as st

st.title("Simple Streamlit App")
st.write("これは最小限の Streamlit アプリです。テキストを入力して表示できます。")

user_input = st.text_input("テキストを入力してください")
if st.button("表示"):
    st.success(f"入力内容: {user_input}")
