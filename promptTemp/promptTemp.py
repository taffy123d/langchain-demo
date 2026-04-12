from dotenv import load_dotenv
load_dotenv()
import os

from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

from ut.md2str import md_read

model = init_chat_model(model='deepseek-chat',temperature=1.4)

prompt_template = PromptTemplate.from_template(
  '亲戚家刚生的孩子，爸爸姓{lastname},是个{gender},请你帮取个名字,生日是{date}'
)

system_prompt = md_read("prompt/system_prompt.md")

# prompt_text = prompt_template.format(name = 'tafei',gender='男',job='学生',age='19')

chain = prompt_template | model

if __name__ == '__main__':
  res = chain.stream(input=({'lastname':'张','gender':'女儿','date':'2025.3.21'}))
  for chunk in res:
    print(chunk.content,end='',flush=True)

