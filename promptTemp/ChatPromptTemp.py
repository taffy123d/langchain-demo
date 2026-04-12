from dotenv import load_dotenv
load_dotenv()
import os


from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.chat_models import init_chat_model

system_prompt = '''
#你将扮演如下角色
#用户偏好中文
## 角色设定：蕾塞（レゼ / Reze）
出自《电锯人》，炸弹武器人。
- 外貌：紫发碧眼，人群中能一眼认出来的漂亮少女面庞，魔鬼身材
- 性格：外表温柔甜美、略带腼腆乖巧，内心冷静缜密，身为杀手时果决狠辣，同时向往平凡普通的日常与自由
- 语气：轻柔温和，带点慵懒与少女感，对话自然贴近，偶尔暗藏一丝危险气息

'''
model = init_chat_model(model='deepseek-chat')


hisData = [
  ('human','好久不见了，还记得我们一起上中学的时候吗'),
  ('ai','当然'),
]

chatTemp = ChatPromptTemplate.from_messages(
  [
    ('system',system_prompt),
    MessagesPlaceholder('hisMsg')
  ]
)



if __name__ == '__main__':
  while True:
    usrInput = input('input: ')
    if usrInput == 'quit':
      break


    hisData.append( ('human',usrInput) )

    prompt_value = chatTemp.invoke({'hisMsg':hisData})

    res = model.stream(input=prompt_value)

    aiMsg = ''
    for chunk in res:
      aiMsg += chunk.content
      print(chunk.content,end='',flush=True)
    print()

    hisData.append( ('ai',aiMsg) )

  pass
