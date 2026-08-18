from langchain_chroma import Chroma
import config_data as config

class VectorSearchService:
    def __init__(self, embedding):
        self.embedding = embedding
        self.chroma = Chroma(
            collection_name=config.collection_name,   # 数据库名称
            embedding_function=self.embedding,  # 向量模型
            persist_directory=config.persist_directory,  #数据库本地存储文件夹路径
        )

    def get_retriever(self):
        """返回向量检索器，方便加入chain"""
        return self.chroma.as_retriever(search_kwargs={'k': config.similarity_threshold})

if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever = VectorSearchService(DashScopeEmbeddings(model=config.embedding_model_name)).get_retriever()

    res = retriever.invoke("OWASP第4个漏洞")
    unique_ids = set()

    for document in res:
        print(res)
        unique_ids.add(document.id)
        print(f"其中唯一的 Document ID 有 {len(unique_ids)} 个")
    # 检索后
    print(f"检索返回了 {len(res)} 个 Document")




