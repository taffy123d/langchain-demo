from langchain_core.messages import SystemMessage,HumanMessage,AIMessage,ToolMessage

def hist_out_stream(response):
  full_response = ""
  for token, metadata in response:
    if token.content:
      print(token.content, end='', flush=True)
      full_response += token.content
  print()  # 换行
  return full_response




def out_stream(response):
  for token,metadata in response:
    if token.content:
      print(token.content,end='',flush=True)
  print()

def out_invoke(response):
  msg = response['messages']
  for it in msg:
    it.pretty_print()


