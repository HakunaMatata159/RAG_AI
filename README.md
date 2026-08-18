
一个基于 **RAG（检索增强生成）** 技术的智能文档对话系统。上传任意PDF文档用以更新AI知识库内容，在网页可像与人对话一样，向AI提问任何内容，相关问题的回答会结合新知识和AI模型原有的知识，给出更全面的内容。内置 **LangChain + Chroma + Streamlit**，开箱即用。

> 💡 项目预置了 **2025 OWASP TOP 10** 网络安全报告作为示例知识库（chroma_db中），但**不限于此**——任何领域的PDF文档均可自由上传、索引和问答。


## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 📄 **PDF自由上传** | 支持上传PDF文档，系统自动解析(文本）并建立索引 |
| 💬 **智能对话式问答** | 基于文档内容与AI模型自身训练数据进行自然语言问答，专业性更高，像聊天一样简单 |
| 🔍 **RAG精准检索** | 先检索相关片段，再生成答案，**告别AI幻觉** |
| 🧠 **多轮对话记忆** | 记住历史对话上下文，支持连续追问 |
| 🌐 **Web交互界面** | 基于Streamlit构建，无需代码，打开浏览器即可使用 |


## 🏗️ 技术架构

| 组件 | 技术选型 |
|------|----------|
| 大语言模型 | 通义千问 |
| RAG 框架 | LangChain |
| 向量数据库 | Chroma（本地持久化） |
| 文档解析 | PyPDF2 / LangChain Document Loaders |
| Web 界面 | Streamlit |
| 开发语言 | Python 3.10+ |


## 🚀 快速启动

### 1. 克隆仓库
git clone https://github.com/HakunaMatata159/RAG_AI.git
cd RAG_Program

### 2、请确保系统环境变量配置中，配置了：
DASHSCOPE_API_KEY = 你的通义千问api key

### 3、启动应用（请确保在存放代码文件目录打开终端）
streamlit run web_chat.py

### 4、上传pdf文件（请确保在存放代码文件目录打开终端）
streamlit run File_Upload.py

### 5、自定义配置
详细配置见config_data.py
