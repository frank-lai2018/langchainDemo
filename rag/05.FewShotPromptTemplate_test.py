from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

example_template = PromptTemplate.from_template(
    "單詞:{word}，反義詞：{antonym}。"
)

example_data=[
    {"word": "快樂", "antonym": "悲傷"},
    {"word": "高", "antonym": "矮"},
    {"word": "大", "antonym": "小"}
]

# 定義 Few-Shot 提示模板
fewshot_template = FewShotPromptTemplate(
    example_prompt=example_template, # 用來格式化每一個範例的提示模板
    examples=example_data, # 範例資料，會被 example_prompt 格式化後插入到最終提示中
    prefix="你是我的人工智慧助手，請用中文回答我的問題。以下是一些單詞和它們的反義詞的例子：", # 最終提示的前綴部分
    suffix="請告訴我{keyword}的反義詞是什麼？", # 最終提示的後綴部分，其中 {keyword} 是一個變量，會在調用時被替換
    input_variables=["keyword"] # 定義在 suffix 中會被替換的變量名稱
)

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
chain = fewshot_template | llm
result = chain.invoke({"keyword": "爽快"})
print(result.content)