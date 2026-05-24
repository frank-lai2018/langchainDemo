from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# 定義一個簡單的提示模板
template = PromptTemplate(
    input_variables=["name", "task"],
    template="你是我的人工智慧助手，請用中文回答我的問題。我的名字是{name}，我需要幫助的任務是：{task}。"
)

# 使用模板生成提示
prompt = template.format(name="Frank", task="規劃一個去日本東京旅遊的行程")
print(prompt)

# 定義一個更複雜的提示模板，包含系統、使用者和助手的角色
# complex_template = PromptTemplate(
#     input_variables=["name", "task"],
#     template=[
#         ("system", "你是我的人工智慧助手，請用中文回答我的問題。"),
#         ("human", "您好，我是{name}"),
#         ("human", "我需要幫助的任務是：{task}"),
#         ("assistant", "好的，{name}！我會幫你規劃一個去日本東京旅遊的行程。")
#     ]
# )

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
# response = llm.invoke(prompt)
# print("--- 基本對話回應 ---")
# print(response.content)


print("\n--- 串流回應 ---")
for chunk in llm.stream(prompt):
    print(chunk.content, end="", flush=True)

chain = prompt | llm
response = chain.invoke(name="Frank", task="規劃一個去日本東京旅遊的行程")
print("\n--- 使用鏈式調用的回應 ---")
print(response.content)