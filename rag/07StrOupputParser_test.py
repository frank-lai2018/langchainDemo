from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

parser = StrOutputParser()
model = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    temperature=0.7,
    max_retries=2
)
prompt = PromptTemplate.from_template(
    "我的鄰居姓：{lastname}，剛生了{gender}，請起名，僅告知我名字即可。"
)

chain = prompt | model | parser | model | parser

res: str = chain.invoke({"lastname": "張", "gender": "女兒"})
print(res)
print(type(res))
