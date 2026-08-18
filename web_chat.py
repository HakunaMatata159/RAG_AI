import time
from Rag import RagService
import streamlit as st
import config_data as config

st.set_page_config(
    page_title="ChatNow",
    page_icon="😃",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': '一个基于RAG架构的聊天AI'}
)

# 标题
st.title("ChatNow")
st.divider()  # 分隔符

# 初始化消息历史
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "你好，有什么可以帮助你？"}]

# 初始化 RAG 服务
if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

# 显示所有历史消息
for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入框
prompt = st.chat_input()

if prompt:
    # 显示用户消息
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    # AI 响应
    response_list = []
    with st.spinner("AI思考中..."):
        # 调用 RAG 服务
        response_stream = st.session_state["rag"].chain.stream(
            {"input": prompt},config.session_config
        )
        def capture_response(generator,cache_list):
            for chunk in generator:
                response_list.append(chunk)
                yield chunk


        # 显示 AI 响应
        st.chat_message("assistant").write_stream(capture_response(response_stream, response_list))
        st.session_state["message"].append({"role": "assistant", "content":"".join(response_list)})