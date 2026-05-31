from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import CSVLoader


# 初始化嵌入模型
embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

vector_store = InMemoryVectorStore(embedding_model)

loader = CSVLoader(
    file_path="./rag/data/info.csv",
    encoding="utf-8",
    source_column="source",     #   
)

documents = loader.load()
# id1 id2 id3 id4 ...
# 向量儲存、刪除、檢索
vector_store.add_documents(
    documents=documents,        #   
    ids=["id"+str(i) for i in range(1, len(documents)+1)] #     
)

# 刪除  傳入[id, id...]
vector_store.delete(["id1", "id2"])

# 檢索 返回類型list[Document]
result = vector_store.similarity_search(
    "瑞达法",
    3       # 檢索的結果要幾個
)

print(result)