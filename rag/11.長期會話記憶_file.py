import os,json
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import message_to_dict, messages_from_dict,BaseMessage

# message_to_dict:將消息對象轉換為字典格式，方便存儲和傳輸。
# message_from_dict:將字典格式的消息轉換回消息對象，以便在對話中使用。
# AIMessage、HumanMessage、SystemMessage:分別代表AI、用戶和系統的消息類型，用於構建對話歷史，都是BaseMessage的子類。

class FileChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, session_id, storage_path):
        self.session_id = session_id #會話ID，用於區分不同的對話會話，確保每個會話的歷史記錄獨立存儲。
        self.storage_path = storage_path  #文件路徑，用於存儲和讀取對話歷史的文件位置。

        self.file_path = os.path.join(self.storage_path, f"{self.session_id}.json") #構建完整的文件路徑，將會話ID作為文件名的一部分，確保每個會話的歷史記錄存儲在不同的文件中。

        os.makedirs(self.storage_path, exist_ok=True) #確保存儲路徑存在，如果不存在則創建。

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence[BaseMessage]表示一個包含BaseMessage對象的序列，這些消息將被添加到對話歷史中。

        all_messages = list(self.messages) # Existing messages
        all_messages.extend(messages)  # Add new messages

        # 將所有消息轉換為字典格式，以便存儲到文件中。
        # 類物件寫入文件 -> 一堆二進制數據，無法直接存儲和讀取，因此需要將其轉換為字典格式。
        # 為了方便，可以將BaseMessage消息轉為字典(借助json模塊已json字串寫入文件)
        # 官方提供的message_to_dict函數可以將BaseMessage對象轉換為字典格式，這樣就可以方便地存儲和傳輸消息了。

        # 傳統寫法
        # new_messages =[]

        # for message in all_messages:
        #     new_messages.append(message_to_dict(message))

        #列表推導式寫法
        new_messages = [message_to_dict(message) for message in all_messages]

        #將數據寫入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)


    @property #@property裝飾器將方法轉換為屬性，使得可以像訪問屬性一樣訪問方法，這樣在使用時就不需要加括號了。
    def messages(self) -> Sequence[BaseMessage]:
        if not os.path.exists(self.file_path):
            return []  # 如果文件不存在，返回空列表

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)

                # 將字典格式的消息轉換回BaseMessage對象，以便在對話中使用。
                # 官方提供的dict_to_message函數可以將字典格式的消息轉換回BaseMessage對象，這樣就可以在對話中使用了。

                messages = messages_from_dict(messages_data)
                return messages
        except (json.JSONDecodeError, FileNotFoundError):
            return []  # 如果文件內容無法解析為JSON，返回空列表
        
    def clear(self) -> None:
        if os.path.exists(self.file_path):
            os.remove(self.file_path)  # 刪除文件以清除對話歷史
        
str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    temperature=0.7,
    max_retries=2
)

# prompt = ChatPromptTemplate.from_template(
#     "你需要根據會話歷史回應用戶問題，對話歷史:{chat_history}。用戶提問: {user_input}，請回答"
# )

def print_prompt(full_prompt):
    print("="*20, full_prompt.to_string(), "="*20)
    return full_prompt


# 2. 修正 Prompt 結構：使用 MessagesPlaceholder 來接收歷史對話紀錄物件
prompt = ChatPromptTemplate.from_messages([
    ("system", "你需要根據會話歷史回應用戶問題。"),
    MessagesPlaceholder(variable_name="chat_history"), # 👈 歷史紀錄放這裡
    ("human", "{user_input}")                         # 👈 用戶當前輸入放這裡
])

base_chain = prompt | print_prompt | model | str_parser

store = {} #key就是session_id，value是InMemoryChatMessageHistory類物件

def get_history(session_id):
    return FileChatMessageHistory(session_id, storage_path="./chat_history") #根據session_id獲取歷史消息，這裡直接返回FileChatMessageHistory類物件
    
# 創建一個新的鏈，對原鏈自動附加歷史消息
chain_with_history = RunnableWithMessageHistory(
    base_chain, #增強原有的Chain
    get_history, #獲取歷史消息的函數，通過id獲取InMemoryChatMessageHistory類物件
    input_messages_key="user_input", #用戶輸入的消息在prompt中的變量名稱
    history_messages_key="chat_history" #歷史消息在prompt中的變量名稱
    )


if __name__ == "__main__":
    #固定格式，添加langChain的配置，為當前程序配置所屬的session_id，這樣就可以根據session_id獲取對應的歷史消息
    ssession_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }

    # res = chain_with_history.invoke({"user_input": "小明有兩隻貓"}, ssession_config)
    # print("第一次執行結果:", res)

    # res = chain_with_history.invoke({"user_input": "大明有兩隻狗"}, ssession_config)
    # print("第二次執行結果:", res)

    res = chain_with_history.invoke({"user_input": "總共有幾個寵物"}, ssession_config)
    print("第三次執行結果:", res)