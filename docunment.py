from langchain_community.document_loaders import CSVLoader

from langchain_community.document_loaders import JSONLoader #jq

import json
#loader() 一次性加载全部文档
#lazy_load() 延迟流式传输文档

loader_csv = CSVLoader(
  file_path='./dcm/csv/stu.csv',
  encoding='utf-8',
  csv_args={
    'delimiter':',',              #指定分隔符
    'quotechar':'"',              #文本内含义分隔符，可以 '/" 包裹
    'fieldnames':['a','b','c']      #指定表头 （数据原本有表头时，第一行也会被当成数据）
  }
)

# documents = loader.load() #load() -> [Docunment,Docunment...]
#lazy_load() 迭代器[Document]


loader_json = JSONLoader(
  file_path='./dcm/json/stu.json',
  jq_schema=".",       #jq语法
  text_content=False,       #可选 抽取是否为字符串，默认True
  json_lines=False         #可选 JsonLines
)

loader_json_list = JSONLoader(
  file_path='./dcm/json/stu_list.json',
  jq_schema=".[].name",       #jq语法
  text_content=True,       #可选 抽取是否为字符串，默认True
  json_lines=False         #可选 JsonLines
)

loader_json_line = JSONLoader(
  file_path='./dcm/json/stu_lines.json',
  jq_schema=".",       #jq语法
  text_content=False,       #可选 抽取是否为字符串，默认True
  json_lines=True         #可选 JsonLines
)





if __name__ == '__main__':
  print('hello,langchain')

  # json_doc = loader_json.load()
  # json_doc_list = loader_json_list.load()
  # json_doc_lines = loader_json_line.load()

