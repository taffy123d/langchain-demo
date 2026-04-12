from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

embeddings = DashScopeEmbeddings()

def emb_query(text):
  return embeddings.embed_query(text)

def emb_documents(text):
  return embeddings.embed_documents(text)


if __name__ == '__main__':
# ------------------- 1. 单文本生成向量 -------------------
  query = "LangChain如何调用嵌入模型？"
  query_embedding = embeddings.embed_query(query)
  print(f'type: {type(query_embedding)}')
  print(f"向量维度：{len(query_embedding)}")
  print(f"向量前5个值：{query_embedding[:5]}")

  # ------------------- 2. 批量文本生成向量 -------------------
  texts = [
      "DeepSeek提供文本嵌入API",
      "LangChain是大模型应用开发框架",
      "嵌入模型用于生成语义向量"
  ]
  text_embeddings = embeddings.embed_documents(texts)
  print(f'type: {type(text_embeddings)}')
  print(f"批量生成向量数量：{len(text_embeddings)}")