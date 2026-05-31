from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    temperature=0.7,
    max_retries=2
)

first_prompt = PromptTemplate.from_template(
   "我的鄰居姓：{lastname}，剛生了{gender}，請起名，僅告知我名字即可。"
)

second_prompt = PromptTemplate.from_template(
    "姓名{name}，請幫我解析含義。"
)

# 函数的入参：AIMessage -> dict  ({"name": "xxx"})
# my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

# chain = first_prompt | model | (lambda ai_msg: {"name": ai_msg.content}) | second_prompt | model | str_parser
chain = first_prompt | model 

presult = chain.invoke({"lastname": "劉", "gender": "女孩"})
print(presult)

# for chunk in chain.stream({"lastname": "劉", "gender": "女孩"}):
#     print(chunk, end="", flush=True)
