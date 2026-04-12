from dotenv import load_dotenv
load_dotenv()
import os

from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain.chat_models import init_chat_model

model = init_chat_model(model='deepseek-chat')


example_template = PromptTemplate.from_template('单词:{word},反义词:{antonym}')
example_data = [
  {'word':'大','antonym':'小'},
  {'word':'美丽','antonym':'丑陋'}
]
few_shot_prompt = FewShotPromptTemplate(
  example_prompt = example_template, #示例数据的提示词模板
  examples = example_data,          #示例数据
  prefix = '给出给定词的反义词，有如下示例：',        #示例数据前内容
  suffix='基于示例告诉我：{inputWord}的反义词是？',     #示例数据后内容
  input_variables = {'inputWord'}           #在前缀或后缀中需要注入的变量名列表
)
if __name__ == '__main__':
  prompt_text = few_shot_prompt.invoke(input={'inputWord':'胜'}).to_string()
  print("prompt: ",end='')
  print(prompt_text)
  print()
  res = model.invoke(input=prompt_text)

  print(res.content)
  pass