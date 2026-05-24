from google import genai
# 💡 重點：請確保檔案頂端有補上下面這一行！
from google.genai import types

client = genai.Client()

# 呼叫純文字向量模型
# 3,072 維（預設，精準度最高）

# 1,536 維（平衡型）

# 768 維（輕量高效，能大幅節省向量資料庫的儲存成本）
response = client.models.embed_content(
    model="gemini-embedding-001",
    contents="你好，這是一段要轉成向量的繁體中文測試。",
    config=types.EmbedContentConfig(
        output_dimensionality=2 # 在這裡指定你想要的維度
    )
)

# 取得向量結果
print(response.embeddings[0].values)