from langchain_core.messages import AIMessage

def get_AIMessage(result):
  # 获取所有消息
        str = ""
        messages = result["messages"]
        
        # 收集所有的AIMessage
        # ai_messages = [msg for msg in messages if isinstance(msg, AIMessage)]
        ai_messages = []
        for msg in messages:
            if isinstance(msg, AIMessage):
                ai_messages.append(msg)


        str += "\n=== 所有AIMessage的content ===\n"

        if ai_messages:
            for i, ai_msg in enumerate(ai_messages):
                # 打印每个AIMessage的content，包括空的
                content_display = ai_msg.content if ai_msg.content.strip() else "[空内容]"

                str0 = f"AIMessage #{i+1}: {content_display}"
                str += str0
                str += '\n'
                
                # 如果有tool_calls，也打印出来
                if hasattr(ai_msg, 'tool_calls') and ai_msg.tool_calls:
                    strt = f"Tool Calls: {ai_msg.tool_calls}"
                    str += strt
                    str +='\n'
        else:
            strddd = "未找到任何AIMessage"
            str +=strddd
            str += '\n'
        return str

def get_finalAIMessage(result):
    str = ""
    messages = result["messages"]
        
    ai_messages = []
    for msg in messages:
        if isinstance(msg, AIMessage):
            ai_messages.append(msg)

    non_empty_ai_messages = [msg for msg in ai_messages if msg.content.strip()]
    if non_empty_ai_messages:
            final_content = non_empty_ai_messages[-1].content
            strddd = f"{final_content}"
            str +=strddd
    else:
            strddd = "未找到有效AI回复内容"
            str +=strddd
    return str
    pass