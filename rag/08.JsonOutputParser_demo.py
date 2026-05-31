from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    temperature=0.7,
    max_retries=2
)

# 定義一個簡單的提示模
prompt = PromptTemplate.from_template(
    "我的鄰居姓：{lastname}，剛生了{gender}，請起名，請用JSON輸出，key=name，僅告知我名字即可。"
)

second_prompt = PromptTemplate.from_template(
    "姓名：{name}，請用中文介紹一下這個名字的由來和意義。"
)

# 這裡我們將模型的輸出直接解析為 JSON 格式，假設模型會回傳一個包含名字的 JSON 物件，例如：{"name": "張小花"}
chain = prompt | model | json_parser | second_prompt | model | str_parser

presult = chain.invoke({"lastname": "張", "gender": "女兒"})
print(presult)
print(type(presult))