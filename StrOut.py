from dotenv import load_dotenv
load_dotenv()
import os

from ut.md2str import md_read

from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate


parser = StrOutputParser()

model = init_chat_model(model='deepseek-chat')
system_prompt = md_read("prompt/system_prompt.md")

prompt_temp = PromptTemplate.from_template(
  '亲戚家刚生的孩子，爸爸姓{lastname},是个{gender},请你帮取个名字,生日是{date}。只用给出一个名字无需输出其它内容'
)

prompt_temp2 = PromptTemplate.from_template('解释一下这个名字的由来') 


chain = prompt_temp | model | parser 

if __name__ == '__main__':
  res = chain.invoke(input=({'lastname':'张','gender':'女儿','date':'2025.1.3'}))

  print(res)
  print(type(res))

  print()
  pass

