import streamlit as st

st.title("Simple Streamlit App")
st.write("これは最小限の Streamlit アプリです。テキストを入力して表示できます。")

# 既存の表示機能
user_input = st.text_input("テキストを入力してください", key="display_input")
if st.button("表示"):
    st.success(f"入力内容: {user_input}")

# session_state に tasks を保持する
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

st.header("タスク管理（セッション単位）")
# タスク入力欄（セッションキーを使って追加後にクリアできるようにする）
task_input = st.text_input("タスクを入力してください", key="task_input")
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("追加"):
        task = task_input.strip()
        if task:
            st.session_state["tasks"].append(task)
            st.success("タスクを追加しました")
            # 入力欄をクリア
            st.session_state["task_input"] = ""
        else:
            st.error("空のタスクは追加できません")

with col2:
    if st.button("クリア（全て）"):
        st.session_state["tasks"] = []
        st.info("タスクをすべて削除しました")

st.subheader("現在のタスク")
if st.session_state["tasks"]:
    for i, t in enumerate(st.session_state["tasks"], 1):
        st.write(f"{i}. {t}")
else:
    st.info("タスクはまだありません。")
