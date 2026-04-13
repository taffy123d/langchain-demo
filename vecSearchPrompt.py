# =======================================================================================
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_core.vectorstores import InMemoryVectorStore #向量对象(内存)
from langchain_chroma import Chroma #Chroma 轻量级向量数据库
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document  # 导入Document类型
# =======================================================================================

# 加载环境变量
load_dotenv()
#模型设定
model_deepseek = init_chat_model(model='deepseek-chat')
embeddings_model = DashScopeEmbeddings(model='text-embedding-v4')

#================InMemoryVectorStore()也可改用Chroma向量数据库============================
vec_store = InMemoryVectorStore(embedding=embeddings_model)
#add_text 传入一个list[str...]
vec_store.add_texts([
  '减肥就是要少吃多练','在减脂期间吃东西很重要，清淡少油控制卡路里摄入并运动起来','跑步是很好的运动'
])
#========================================================================================
input_text = '怎么减肥？'

# ==================检索================================================================
#检索
res_search = vec_store.similarity_search(input_text,k=2)  
reference_text = '[\n'
i = 1
for doc in res_search:
  reference_text = reference_text+f'{i}: '+doc.page_content+'\n'
  i+=1
reference_text += ']'
    # ---------------------------------------------------------------------
#Runnable对象检索
res_runnable_search = vec_store.as_retriever(search_kwargs={'k':2})
# <InMemoryVectorStore>.as_retriever
#     - 输入: 用户提问 <str>
#     - 输出: 向量库检索结果 <list[Document...]>
# <PromptTemplate>
#     - 输入: <dict>
#     - 输出: <PromptValue>
# =======================================================================================

#======================提示词模板======================================================
prompt = ChatPromptTemplate.from_messages(
  [
    ('system','以我提供的已知参考资料为主，简洁且专业的回答用户问题。\n 参考资料:\n{context}'),
    ('user','用户提示词: {input}')
  ]
)
# =======================================================================================

# ===================================链式调用时用到的函数=========================================
def print_prompt(prompt): #打印总提示词(debug函数)
  print('='*20)
  print(prompt.to_string())
  print('='*20)
  return prompt

def format_func(docs:list[Document]) -> str:
  if not docs:
    return '无参考资料'
  else:
    f_str = '[\n'
    i=1
    for it in docs:
      f_str += f'{i}.{it.page_content}\n'
      i+=1
    f_str+=']'
    return f_str
  pass
# =======================================================================================

# =======================================================================================
chain = prompt | print_prompt | model_deepseek

# 1 <dict>在链中接收输入时，同一份输入会被广播给字典中的所有键 然后再输出赋值后的dict
# 2 RunnablePassthrough() 透传,即接收什么输入，就原封不动地输出什么 
chain_search = res_runnable_search | format_func #输入问题相关，检索后输出Docment再传入format_func返回str
dict_chain_input = {'input':RunnablePassthrough(),'context':chain_search}
chain_r = (
  dict_chain_input| 
  prompt | 
  print_prompt | #打印最终提示词
  model_deepseek
)
# =======================================================================================


# =======================================================================================
def test():
  response = chain.invoke({'context':reference_text , 'input':input_text})
  print(response.content)

def rtest():
  response = chain_r.invoke(input_text)
  print(response.content)
  pass
# =======================================================================================

if __name__ == '__main__':
  rtest()
  pass