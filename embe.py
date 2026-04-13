from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import CSVLoader
from langchain_core.vectorstores import InMemoryVectorStore #向量对象(内存)

import asyncio

#Chroma 轻量级向量数据库
from langchain_chroma import Chroma

# 加载环境变量
load_dotenv()

embeddings_model = DashScopeEmbeddings()


csv_loader = CSVLoader(
        file_path='dcm/data/info.csv',
        encoding='utf-8',
        source_column='source' #指定本条数据来源（元数据）
    )

csv_doc = csv_loader.load()


def InMemorySearch():

    vector_store_InMemory = InMemoryVectorStore(
        embedding=embeddings_model
        )

    #添加文档到向量存储，并指定id
    vector_store_InMemory.add_documents(
        documents=csv_doc,           #被添加的文档 class<list[Document..]>
        ids=[f"id{i+1}" for i in range(len(csv_doc))]                       #给添加的文档提供id（字符串） class<list[str..]>          
    )

    #删除 传入[id1,id2...] (idx 是字符串)
    vector_store_InMemory.delete(['id1','id2'])

    #检索
    res1 = vector_store_InMemory.similarity_search(
        "Python是不是简单易学？",
        k=1                        #检索结果个数
    )

    print(res1)
    pass


def InChromaSearch():

    file_id = 1
    vector_store_InMemory = Chroma(
        collection_name='test',     #数据库表名
        embedding_function=embeddings_model,
        persist_directory=f'./vectordb{file_id}'    #数据库存放文件夹目录
    )

    # 添加文档到向量存储，并指定id
    vector_store_InMemory.add_documents(
        documents=csv_doc,           #被添加的文档 class<list[Document..]>
        ids=[f"id{i+1}" for i in range(len(csv_doc))]                       #给添加的文档提供id（字符串） class<list[str..]>          
    )

    # 删除 传入[id1,id2...] (idx 是字符串)
    vector_store_InMemory.delete(['id1','id2'])

    #检索
    res1 = vector_store_InMemory.similarity_search(
        "Python是不是简单易学？",
        k=1,                        #检索结果个数
        filter={"source":"黑马程序员"}  #过滤检索结果 指定检索为 {"source":"黑马程序员"}
    )

    print(res1)
    pass



if __name__ == '__main__':
    InMemorySearch()
    print()
    InChromaSearch()
    pass