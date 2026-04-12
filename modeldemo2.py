from dotenv import load_dotenv
load_dotenv()
import os

from ut.md2str import md_read

from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_core.messages import AIMessage,SystemMessage

from langchain.chat_models import init_chat_model


model = init_chat_model(model='deepseek-chat')
system_prompt = SystemMessage(content=md_read("prompt/system_prompt.md"))

chain = system_prompt | model

conversation_chain = RunnableWithMessageHistory(
  chain,
  None,
  input_messages_key='input',
  history_messages_key='chat_history'
)

chat_history_store = {}

if __name__ == '__main__':
  total_tokens = 0
  while True:
    usrInput = input("input: ")
    
    if usrInput == 'quit':
      break

    
    response = model.invoke([
      ('system',system_prompt),
      ('human',usrInput) 
      ])
    print(response.content)
    total_tokens += response.usage_metadata['total_tokens']

  print(total_tokens)
  pass
