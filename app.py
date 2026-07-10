import streamlit as st
import json
import os

# ファイルパス
TODOS_FILE = "todos.json"

def load_todos():
    """todos.json からタスクを読み込む"""
    if os.path.exists(TODOS_FILE):
        try:
            with open(TODOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_todos(todos):
    """タスクを todos.json に保存"""
    with open(TODOS_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

def get_next_id(todos):
    """次のタスクIDを取得"""
    if not todos:
        return 1
    return max(task["id"] for task in todos) + 1

st.title("Simple Streamlit App")
st.write("これは最小限の Streamlit アプリです。テキストを入力して表示できます。")

# 既存の表示機能
user_input = st.text_input("テキストを入力してください", key="display_input")
if st.button("表示"):
    st.success(f"入力内容: {user_input}")

# セッションに tasks を初期化
if "tasks" not in st.session_state:
    st.session_state["tasks"] = load_todos()

st.header("タスク管理")

# タスク入力欄
task_input = st.text_input("タスクを入力してください", key="task_input")
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("追加"):
        task = task_input.strip()
        if task:
            new_task = {
                "id": get_next_id(st.session_state["tasks"]),
                "title": task,
                "done": False
            }
            st.session_state["tasks"].append(new_task)
            save_todos(st.session_state["tasks"])
            st.success("タスクを追加しました")
            st.session_state["task_input"] = ""
            st.rerun()
        else:
            st.error("空のタスクは追加できません")

with col2:
    if st.button("クリア（全て）"):
        st.session_state["tasks"] = []
        save_todos(st.session_state["tasks"])
        st.info("タスクをすべて削除しました")
        st.rerun()

# タスク表示フィルター
st.subheader("タスク一覧")
tab1, tab2, tab3 = st.tabs(["すべて", "未完了", "完了"])

with tab1:
    display_tasks = st.session_state["tasks"]
    label = "すべてのタスク"

with tab2:
    display_tasks = [t for t in st.session_state["tasks"] if not t["done"]]
    label = "未完了のタスク"

with tab3:
    display_tasks = [t for t in st.session_state["tasks"] if t["done"]]
    label = "完了したタスク"

if display_tasks:
    for task in display_tasks:
        col_check, col_title, col_delete = st.columns([0.5, 4, 0.5])
        
        # チェックボックス
        with col_check:
            new_status = st.checkbox(
                "完了",
                value=task["done"],
                key=f"checkbox_{task['id']}"
            )
            if new_status != task["done"]:
                task["done"] = new_status
                save_todos(st.session_state["tasks"])
                st.rerun()
        
        # タスク名（完了時は打ち消し線）
        with col_title:
            if task["done"]:
                st.write(f"~~{task['title']}~~")
            else:
                st.write(task["title"])
        
        # 削除ボタン
        with col_delete:
            if st.button("🗑️", key=f"delete_{task['id']}"):
                st.session_state["tasks"] = [
                    t for t in st.session_state["tasks"]
                    if t["id"] != task["id"]
                ]
                save_todos(st.session_state["tasks"])
                st.rerun()
else:
    st.info("タスクはまだありません。")
