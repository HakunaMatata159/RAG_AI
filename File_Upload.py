import streamlit as st
from io import BytesIO
import PyPDF2
from Knowledge_base import KnowledgeBaseService


st.set_page_config(
    page_title="数据库更新",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': '这是一个上传pdf文件，用于更新数据库的页面'}
)

st.title("PDF-->数据库更新")

upload_file = st.file_uploader("请上传pdf文件", type=["pdf"], accept_multiple_files=False) # accept_multiple_files=False表示只接受单个文件


if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService() # 初始化服务,用session state保存上传数据库的类实例

if upload_file is not None:
    st.write("文件上传成功！")
    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size / 1024  # 将字节转换为KB
    st.write(f"文件名：{file_name}")
    st.write(f"文件类型：{file_type}")
    st.write(f"文件大小：{file_size:.2f} KB")

    # 使用PyPDF2提取文本
    pdf_bytes = upload_file.getvalue()
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))

    pdf_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text + "\n"

    # 现在 full_text 就是纯文本内容
    print(pdf_text)
    with st.spinner("正在上传数据库中..."):
        response=st.session_state["service"].upload_str(pdf_text, file_name)
        st.write(response)