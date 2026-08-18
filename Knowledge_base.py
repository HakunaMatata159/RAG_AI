import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str:str):
     """
     检查传入的md5字符串是否已经处理过
     :param md5_str:
     :return:False（未处理过）  True（已处理过）
     """
     # 先检查md5文件是否存在
     if not os.path.exists(config.md5_path):
         open(config.md5_path,'w',encoding='utf-8') #因为是写入模式所以没有文件时则创建
         return False
     else:
         for line in open(config.md5_path,'r',encoding='utf-8').readlines():
             line = line.strip()
             if line == md5_str:
                 return True

         return False

def save_md5(md5_str:str):
    """
    将传入的md5字符串保存到文件中
    :param md5_str:
    :return:
    """
    with open(config.md5_path,'a',encoding='utf-8') as f:
        f.write(md5_str+'\n')


def get_string_md5(input_str: str, encoding='utf-8'):
    """
    将传入的字符串转换为md5字符串
    """

    # 将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)

    # 创建md5对象
    md5_obj = hashlib.md5()  # 得到md5对象
    md5_obj.update(str_bytes)  # 更新内容（传入即将要转换的字节数组）
    md5_hex = md5_obj.hexdigest()  # 得到md5的十六进制字符串

    return md5_hex

class KnowledgeBaseService:
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)  #保证数据库本地存储文件夹存在

        self.chroma = Chroma(
            collection_name=config.collection_name,   # 数据库名称
            embedding_function=DashScopeEmbeddings(model=config.embedding_model_name),  # 向量模型
            persist_directory=config.persist_directory,  #数据库本地存储文件夹路径
        )  #Chroma向量库对象

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,      # 每个文本块的最大长度
            chunk_overlap=config.chunk_overlap,   # 每个文本块之间的重叠长度
            separators=config.separators,        # 自然段落划分的依据符号
            length_function=len,                #python的len函数做长度依据
        ) #文本分割器对象

    def upload_str(self,data:str,filename):
        """
        将传入的字符串进行向量化，上传到向量数据库
        :param data:
        :param filename:
        :return:
        """
        # 先转为md5
        md5_hex = get_string_md5(data)

        # 检查md5是否已经处理过
        if check_md5(md5_hex):
            return f"{filename} 已处理过"

        # 根据文本长度决定是否进行分割
        if len(data) > config.max_split_char:
             knowledge_chunks:list[str] = self.spliter.split_text(data)
        else:
             knowledge_chunks = [data] # 如果文本长度小于最大分割字符数，则保持与分割后的数据类型一致

        # 将文本块上传到向量数据库
        metadata = {
            "source": filename,
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.chroma.add_texts(knowledge_chunks,
                              metadatas=[metadata for _ in knowledge_chunks], # 每个文本块都对应一个元数据，数量对齐
                              ) #将文本块和元数据上传到向量数据库
        save_md5(md5_hex) #保存md5字符串到文件中
        return f"{filename} 上传成功"

if __name__ == '__main__':
    service = KnowledgeBaseService()
    service.upload_str("你好，我是张三，我来自中国。","test")
    print(service.upload_str("你好，我是李四，我来自中国。","test"))
