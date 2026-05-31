from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

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

#根據session_id獲取歷史消息，這裡直接返回InMemoryChatMessageHistory類物件
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
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

    res = chain_with_history.invoke({"user_input": "小明有兩隻貓"}, ssession_config)
    print("第一次執行結果:", res)

    res = chain_with_history.invoke({"user_input": "大明有兩隻狗"}, ssession_config)
    print("第二次執行結果:", res)

    res = chain_with_history.invoke({"user_input": "總共有幾個寵物"}, ssession_config)
    print("第三次執行結果:", res)