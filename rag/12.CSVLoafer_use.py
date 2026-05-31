from langchain_community.document_loaders import CSVLoader

#UnicodeDecodeError: 'cp950' codec can't decode byte 0xe7 in position 23: illegal multibyte sequence
#這是Window問題，因為編碼不同，所以需要指定編碼為utf-8
loader = CSVLoader(file_path="./rag/data/stu.csv", encoding="utf-8")
data = loader.load()
print(data)

