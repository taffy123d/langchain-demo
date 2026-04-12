from dotenv import load_dotenv
load_dotenv()
import os


from ut.md2str import md_read
from ut.output import out_invoke,out_stream,hist_out_stream

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage,ToolMessage

from tools.get_weather import create_weather_tool
from langchain_community.tools import DuckDuckGoSearchRun



model = init_chat_model(model='deepseek-chat')

tools = [DuckDuckGoSearchRun(), create_weather_tool()]

system_prompt = md_read("prompt/system_prompt.md")

agent = create_agent(model,tools)



if __name__ == '__main__':
    
    history_msg = [("system",system_prompt)]
    while True:
        usrInput = input("input: ")
        if usrInput == 'quit':
            print('exit...')
            break

        # 追加用户输入
        history_msg.append(("human",usrInput))

        # 获取流式响应
        response = agent.stream(
            {'messages': history_msg},
            stream_mode='messages'
        )

        full_response = hist_out_stream(response)
        history_msg.append(("ai",full_response))



