from dotenv import load_dotenv
load_dotenv()
import os

import json

from ut.md2str import md_read

from langchain.chat_models import init_chat_model
from langchain_core.runnables.history import RunnableWithMessageHistory #历史对话增强链

from langchain_core.chat_history import InMemoryChatMessageHistory #存储历史对话
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder,PromptTemplate

from langchain_core.messages import SystemMessage
from FileChatMessageHistory import FileChatMessageHistory
from SQLiteChatMessageHistory import SQLiteChatMessageHistory

# store = {} #历史对话消息

# def get_history(session_id):
#   if session_id not in store:
#     store[session_id] = InMemoryChatMessageHistory()
#   return store[session_id]

def get_history(session_id):
  return FileChatMessageHistory(session_id,'./history_chat')

def get_db_history(session_id:str) -> SQLiteChatMessageHistory:
  return SQLiteChatMessageHistory(
    session_id=session_id,
    db_path='history_chat/memory.db' 
  )

system_prompt = md_read("prompt/system_prompt.md")

# str_parser = StrOutputParser()

model = init_chat_model(model='deepseek-chat')
prompt = ChatPromptTemplate.from_messages(
  [
    ('system',system_prompt),
    MessagesPlaceholder('chat_history'),
    ('human','{usrInput}')
  ]
)

base_chain = prompt | model 

conversation_chain = RunnableWithMessageHistory(
  base_chain, #原链
  get_db_history,  #通过会话id获取InMemoryChatMessageHistory对象
  input_messages_key = 'usrInput',  #输入占位符
  history_messages_key = 'chat_history' #历史消息占位符
)

if __name__ == '__main__':
  total_tokens = 0

  #langchain当前程序配置 固定格式
  session_config = {
    'configurable':{
      'session_id' : 'user_001'
    }
  }

  while True:
    usrInput = input("input: ")
    
    if usrInput == 'quit':
      break
    response = conversation_chain.invoke({'usrInput':usrInput},session_config)
    print(response.content)

    total_tokens += response.usage_metadata['total_tokens']

  print(f'total_tokens: {total_tokens}')





# store['user_001']
# |
# |- <class 'langchain_core.chat_history.InMemoryChatMessageHistory'>
#     |
#     |--<class 'tuple'>
#         |
#         |- <class 'str'> "messages" 
#         |- <class 'list'>
#               |- [HumanMessage,AIMessage...]          
#                   |- <class 'tuple'> 
#                             |- ('content',
#                                 'additional_kwargs',
#                                 'response_metadata',
#                                 'type', 
#                                 'name',
#                                 'id')
#                           