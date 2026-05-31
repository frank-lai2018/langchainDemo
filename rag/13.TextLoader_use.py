from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(file_path="./rag/data/Python基础语法.txt", encoding="utf-8")
data = loader.load()
print(data)

#文本分割器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, #chunk_size:指定每個文本塊的最大字符數量，這有助於將長文本分割成更小的部分，以便更有效地處理和分析。
    chunk_overlap=50, #chunk_overlap:指定文本塊之間的重疊字符數量，這有助於確保在分割文本時不會丟失重要的上下文信息，特別是在處理自然語言文本時。
    length_function=len, #length_function:指定用於計算文本長度的函數，默認為內置的len函數，可以根據需要自定義。
    separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""] #separators:指定用於分割文本的分隔符列表，這些分隔符將按照優先順序用於分割文本，從而確保文本被合理地分割成塊。
    )

split_docs = text_splitter.split_documents(data)
print(len(split_docs))
for doc in split_docs:
    print("="*20)
    print(doc)
    print("="*20)