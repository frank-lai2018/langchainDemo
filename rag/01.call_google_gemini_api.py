import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

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
response = llm.invoke("請用一句話形容生成式 AI 的未來。")
print("--- 基本對話回應 ---")
print(response.content)


# 4. 串流輸出範例 (Stream) - 適合需要逐字產生的前端應用
print("\n--- 串流回應 ---")
for chunk in llm.stream("你是誰? 能做什麼?"):
    print(chunk.content, end="", flush=True)

messages = [
    HumanMessage(content="我想去日本東京旅遊3天兩夜，請幫我規劃行程。")
    ]
print("\n--- 串流回應2 ---")
for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)