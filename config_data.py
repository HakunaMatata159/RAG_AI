
md5_path="./md5.text"

#Chroma
collection_name = "base1"
persist_directory = "./chroma_db"

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", "。", "！", "？", "，", "；", " ", "、", "…"]
max_split_char = 1000

# retriever
similarity_threshold = 10

# Model
embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3-max"

# session_conig
session_config = {
        "configurable":{
            "session_id": "user001"
        }
    }