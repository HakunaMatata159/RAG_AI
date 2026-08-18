import os
import json
from typing import Sequence

from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory

def get_history(session_id: str):
    return FileChatMessageHistory(session_id, "./history")

class FileChatMessageHistory(BaseChatMessageHistory):
    """将聊天消息历史持久化存储到本地JSON文件的实现类"""

    def __init__(self, session_id: str, storage_path: str):
        """
        初始化消息历史管理器

        Args:
            session_id: 会话唯一标识符
            storage_path: 存储所有会话文件的文件夹路径
        """
        self.session_id = session_id
        self.storage_path = storage_path
        # 完整文件路径 = 存储文件夹 + 会话ID（作为文件名）
        self.file_path = os.path.join(self.storage_path, self.session_id)

        # 确保存储文件夹存在（如果不存在则自动创建）
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    @property
    def messages(self) -> list[BaseMessage]:
        """
        从本地文件读取并返回当前会话的所有消息

        Returns:
            list[BaseMessage]: BaseMessage对象列表（包含HumanMessage、AIMessage等）
            如果文件不存在，返回空列表
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                # 从JSON文件读取数据，得到：list[dict]
                messages_data = json.load(f)
            # 将字典列表转换为BaseMessage对象列表
            return messages_from_dict(messages_data)
        except FileNotFoundError:
            # 文件不存在时返回空列表（新会话）
            return []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        """
        添加新消息到历史记录中，并持久化到本地文件

        Args:
            messages: BaseMessage对象序列（如列表、元组），可以是单条或多条消息
        """
        # 1. 获取已有的所有消息
        all_messages = list(self.messages)  # 现有消息列表

        # 2. 合并新消息
        all_messages.extend(messages)  # 将新消息追加到末尾

        # 3. 将所有BaseMessage对象转换为字典（便于JSON序列化）
        # 使用列表推导式：对每条消息调用 message_to_dict()
        new_messages = [message_to_dict(message) for message in all_messages]

        # 4. 将字典列表以JSON格式写入文件（覆盖写入）
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    def clear(self) -> None:
        """
        清空当前会话的所有消息历史
        """
        # 写入空列表，即清空文件内容
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

if __name__ == "__main__":
    # 使用示例
    # 1. 创建历史管理器（会话ID为 "user_001"）
    history = FileChatMessageHistory(
        session_id="user_001",
        storage_path="./chat_data"
    )

    # 2. 添加消息（模拟对话）
    from langchain_core.messages import HumanMessage, AIMessage

    history.add_messages([
        HumanMessage(content="你好，我叫小明"),
        AIMessage(content="你好小明！有什么可以帮你的？"),
        HumanMessage(content="请问1+1等于几？")
    ])

    # 3. 读取所有消息
    all_msgs = history.messages
    for msg in all_msgs:
        print(f"{msg.type}: {msg.content}")

    # 输出:
    # human: 你好，我叫小明
    # ai: 你好小明！有什么可以帮你的？
    # human: 请问1+1等于几？

    # 4. 清空历史
    history.clear()
    print(history.messages)  # 输出: []