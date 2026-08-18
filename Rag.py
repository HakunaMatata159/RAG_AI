from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from Vector_search import VectorSearchService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from File_History_Store import get_history

# 打印生成的提示词
def print_prompt(prompt):
    print("--"*20)
    print(prompt.to_string())
    print("--"*20)
    return prompt

# 将向量数据库返回的数据转换为字符串，为拼接到提示词模板中
def format_document(docs: list[Document]):
    if not docs:
        return "无相关参考资料"

    formatted_str = ""
    for doc in docs:
        formatted_str += f"文档片段: {doc.page_content}\n文档元数据: {doc.metadata}\n\n"

    return formatted_str

def dict2str(data:dict) -> str:
    """将字典转换为字符串"""
    return data["input"]

def dict4history(data:dict) -> dict:
    """将字典转换为字符串"""
    new_data = {}
    new_data["input"] = data["input"]["input"]
    new_data["context"] = data["context"]
    new_data["history"] = data["input"]["history"]
    return new_data


class RagService():
    # 组链所用的组件
    def __init__(self):
        self.vector_service = VectorSearchService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )        # 配置向量库

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
            ("system","并且我提供历史对话记录，如下："),
            MessagesPlaceholder("history"),
            ("user", "请回答用户提问: {input}")
        ])       #  提示词模板

        self.chat_model = ChatTongyi(model=config.chat_model_name,
                                     streaming=True) #Chat模型掉用

        self.chain = self.__get_chain__() # 调用链

    def __get_chain__(self):
        """获取最终的执行链"""
        retriever = self.vector_service.get_retriever() # 获取向量库检索器

        chain = ({"input": RunnablePassthrough(),"context": RunnableLambda(dict2str) | retriever | format_document} | RunnableLambda(dict4history) | self.prompt_template | print_prompt | self.chat_model | StrOutputParser())

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain

if __name__ == "__main__":
    # 固定格式，使用RunnableWithMessageHistory必须传入以下包含session—id的配置文件
    session_config = {
        "configurable":{
            "session_id": "test"
        }
    }

    rag_service = RagService().chain.invoke({"input": "软件供应链问题有哪些"},session_config)
    print(rag_service)