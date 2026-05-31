# 需先安裝pypdf庫：python -m pip install pypdf

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="./rag/data/pdf2.pdf",
    mode="single", #single:將整個PDF作為一個文檔加載，返回一個包含整個PDF內容的Document對象。
    password="itheima", #如果PDF文件受密碼保護，則可以在此處提供密碼以進行解密和加載。
    )
data = loader.lazy_load()
i = 1
for page in data:
    i += 1
    print(page.page_content)
    print("-" * 50)
    print(f"第{i}頁")