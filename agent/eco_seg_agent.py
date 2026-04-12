from dotenv import load_dotenv
load_dotenv()
import os
import json
from pydantic import BaseModel

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

model = init_chat_model(model='deepseek-chat')


class StockInfo(BaseModel):
    日期: str
    股票名称: str
    开盘价: str
    收盘价: str
    成交量: str

structured_llm = model.with_structured_output(StockInfo)

examples_data = [
  {
    'content':'2023-01-10,股市震荡。股票强大科技A股今日开盘价100人民币，一度飙升至105人民币，随后回落至98人民币，最终以102人民币收盘，成交量达到520000。',
    'answers': {"日期":"2023-01-10","股票名称":"强大科技A股","开盘价":"100人民币","收盘价":"102人民币","成交量":"520000"}
  },
  {
    'content':'2024-05-16,股市利好。股票英伟达美股今日开盘价105美元，一度飙升至109美元，随后回落至100美元，最终以116美元收盘，成交量达到3560000。',
    'answers': {"日期":"2024-05-16","股票名称":"英伟达美股","开盘价":"105美元","收盘价":"116美元","成交量":"3560000"}
  }
]

questions = [
  "2025-06-16,股市利好。股票传智教育A股今日开盘价66人民币，一度飙升至70人民币，随后回落至65人民币，最终以68人民币收盘，成交量达到123000。",
  "2025-06-06,股市利好。股票黑马程序员A股今日开盘价200人民币，一度飙升至211人民币，随后回落至201人民币，最终以206人民币收盘。"
]

def eco_seg(input_text):
    messages = []
    
    messages.append(SystemMessage(content="你是股票信息提取专家，严格提取字段，无数据填'无'，仅返回JSON"))

    for example in examples_data:
        messages.append(HumanMessage(content=example['content']))
        messages.append(AIMessage(content=json.dumps(example['answers'], ensure_ascii=False)))

    messages.append(HumanMessage(content=input_text))

    result = structured_llm.invoke(messages)
    #返回dic类型    
    return result.model_dump()

if __name__ == '__main__':
  for idx, question in enumerate(questions):
    print(f"===== 第{idx+1}条提取结果 =====")
    res = eco_seg(question)

    print(type(res))
    print(res)
    print()