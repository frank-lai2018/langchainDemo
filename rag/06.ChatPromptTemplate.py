from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

# 定義一個簡單的提示模板
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是我的人工智慧助手，請用中文回答我的問題。"),
        MessagesPlaceholder(variable_name="history"), # 用來插入對話歷史的占位符
        ("human", "請問你記得我叫什麼名字嗎？ 你還記得我幾歲嗎?")
    ]
)

history = [
    {"role": "human", "content": "我叫小明，我今年25歲。"},
    {"role": "assistant", "content": "你好，小明！很高興認識你。"}
]

# 初始化 Gemini 聊天模型
llm = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    temperature=0.7,
    max_retries=2
)

# 進行基本調用 (Invoke)
chain = prompt_template | llm

result = chain.invoke({"history": history})
print(result.content)
# print(result.to_string())

# 檢查 content 是否為列表 (代表包含了思考過程等多個區塊)
raw_content = result.content
if isinstance(raw_content, list):
    for block in raw_content:
        # 只抓取類型為 'text' 的區塊
        if isinstance(block, dict) and block.get("type") == "text":
            # 提取真正的回答文字並印出
            print(block.get("text"))
else:
    # 如果它不是列表，代表模型這次只回傳了單純的字串，直接印出即可
    print(raw_content)