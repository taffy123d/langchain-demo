from dotenv import load_dotenv
load_dotenv()
import os

from ut.md2str import md_read

from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

from langchain_core.runnables import RunnableLambda

from pydantic import BaseModel, Field
from typing import Optional

class outName(BaseModel):
  name : str

outName2json = RunnableLambda(lambda x: x.model_dump_json())

# def outName2json(x) :
#   return x.model_dump_json()
#   pass


json_parser = JsonOutputParser()
str_parser = StrOutputParser()

model_with_json = init_chat_model(model='deepseek-chat').with_structured_output(outName)
model2 = init_chat_model(model='deepseek-chat')

prompt_temp = PromptTemplate.from_template(
  '亲戚家刚生的孩子，爸爸姓{lastname},是个{gender},请你帮取一个名字,生日是{date}。'
)

prompt_temp2 = PromptTemplate.from_template('解释一下这个名字{name}的由来,100字内') 


chain = (
  prompt_temp | 
  model_with_json | 
  # (lambda x: x.model_dump_json()) |
  outName2json |
  json_parser |
  prompt_temp2 |
  model2 |
  str_parser 
  )

if __name__ == '__main__':
  for chunk_content in chain.stream(input=({'lastname':'张','gender':'男孩','date':'2025.4.3'})):
    print(chunk_content,end='',flush=True)
  print()

  pass

