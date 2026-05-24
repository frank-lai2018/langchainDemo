import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 1. 設定 API Key (若已在系統環境變數中設定，此行可省略)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# 2. 初始化 Gemini 聊天模型
# 建議使用最新的 gemini-2.5-flash (速度快、性價比高) 或 gemini-2.5-pro (適合複雜推理)
llm = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    temperature=0.7,
    max_retries=2
)

# 3. 進行基本調用 (Invoke)
# messages = [
#     SystemMessage(content="你是我的人工智慧助手，請用中文回答我的問題。"),
#     HumanMessage(content="您好，我是Frank"),
#     AIMessage(content="您好，Frank！很高興見到您。我是您的人工智慧助手，有什麼我可以幫助您的嗎？"),
#     HumanMessage(content="你知道我是誰嗎? 你能做什麼?")
# ]

# 簡寫
# messages = [
#     ('system',"你是我的人工智慧助手，請用中文回答我的問題。"),
#     ('user',"您好，我是Frank"),
#     ('assistant',"您好，Frank！很高興見到您。我是您的人工智慧助手，有什麼我可以幫助您的嗎？"),
#     ('user',"你知道我是誰嗎? 你能做什麼?")
# ]
messages = [
    ('system',"你是我的人工智慧助手，請用中文回答我的問題。"),
    ('human',"您好，我是Frank"),
    ('ai',"您好，Frank！很高興見到您。我是您的人工智慧助手，有什麼我可以幫助您的嗎？"),
    ('human',"你知道我是誰嗎? 你能做什麼?")
]


print("\n--- 串流回應 ---")
for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)