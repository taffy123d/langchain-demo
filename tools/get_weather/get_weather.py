"""
天气查询工具
使用 wttr.in 免费天气服务获取城市天气信息
"""

import requests
from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class WeatherToolInput(BaseModel):
    """天气查询工具的输入参数"""
    city: str = Field(description="城市名称，例如：北京、Shanghai、New York")
    format: Optional[str] = Field(
        default="clean",
        description="返回格式：'clean'-清理后的纯文本（默认），'plain'-原始文本格式，'simple'-简洁格式，'full'-完整格式，'ascii'-纯ASCII格式"
    )


class WeatherTool(BaseTool):
    """天气查询工具"""

    name: str = "get_weather"
    description: str = (
        "获取指定城市的当前天气信息。"
        "输入应为城市名称，如'北京'、'上海'、'New York'。"
        "返回温度、天气状况和风力等信息。"
    )
    args_schema: Type[BaseModel] = WeatherToolInput

    def _clean_graphical_symbols(self, text: str) -> str:
        """清理文本，只移除图形符号（天气图标等），保留基本符号（度符号、箭头）"""
        import re

        cleaned = str(text)

        # 使用正则表达式移除图形符号范围
        # 天气图标和杂项符号 (U+2600-U+26FF) - 包含☀️、☁️、⛅等
        cleaned = re.sub(r'[\u2600-\u26FF]', '', cleaned)

        # 杂项符号和象形文字 (U+1F300-U+1F5FF) - 包含🌧、🌈等
        cleaned = re.sub(r'[\U0001F300-\U0001F5FF]', '', cleaned)

        # 表情符号 (U+1F600-U+1F64F)
        cleaned = re.sub(r'[\U0001F600-\U0001F64F]', '', cleaned)

        # 交通和地图符号 (U+1F680-U+1F6FF)
        cleaned = re.sub(r'[\U0001F680-\U0001F6FF]', '', cleaned)

        # 注意：保留以下基本符号：
        # - 度符号: U+00B0 (°)
        # - 摄氏度符号: U+2103 (℃)
        # - 华氏度符号: U+2109 (℉)
        # - 箭头: U+2190-U+2193 (←↑→↓)
        # - 其他方向箭头: U+2196-U+2199 (↖↗↘↙)

        # 清理多余空格（由于移除符号可能产生多个空格）
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        return cleaned

    def _run(self, city: str, format: str = "clean") -> str:
        """执行天气查询"""
        try:
            # 映射格式到wttr.in格式字符串
            format_map = {
                "clean": "%l: %C %t %w %h",  # 城市: 天气状况 温度 风力 湿度
                "plain": "%l: %C %t %w %h",  # 城市: 天气状况 温度 风力 湿度
                "simple": "3",  # wttr.in的简洁格式
                "full": "2",    # wttr.in的单行格式
                "ascii": "%l: %C %t %w %h",  # 纯文本，使用%C而不是%c避免Unicode符号
            }

            wttr_format = format_map.get(format, format_map["clean"])

            # 构建请求URL
            url = f"https://wttr.in/{city}?format={wttr_format}"

            # 设置User-Agent避免被拒绝
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            # 发送请求，获取原始字节
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # 获取原始字节
            raw_bytes = response.content

            # 尝试检测编码并解码
            result = ""
            encodings_to_try = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']

            for encoding in encodings_to_try:
                try:
                    result = raw_bytes.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue

            if not result:
                # 如果所有编码都失败，使用replace错误处理
                result = raw_bytes.decode('utf-8', errors='replace')

            result = result.strip()

            if not result:
                return f"未找到城市'{city}'的天气信息，请检查城市名称是否正确。"

            # 根据格式返回不同的信息
            if format == "clean":
                # 使用图形符号清理函数（只移除图形符号，保留基本符号）
                return self._clean_graphical_symbols(result)
            elif format == "plain":
                return result
            elif format == "simple":
                return f"{city}天气: {result}"
            elif format == "full":
                return f"{city}的天气信息:\n{result}"
            elif format == "ascii":
                # 尝试清理ASCII字符
                import re
                # 移除控制字符和非ASCII字符
                cleaned = re.sub(r'[^\x20-\x7E]', ' ', result)
                # 合并多个空格
                cleaned = re.sub(r'\s+', ' ', cleaned).strip()
                return cleaned
            else:
                return result

        except requests.exceptions.RequestException as e:
            return f"获取天气信息时出错：{str(e)}。请稍后重试或检查网络连接。"
        except Exception as e:
            return f"处理天气信息时发生错误：{str(e)}"

    async def _arun(self, city: str, format: str = "clean") -> str:
        """异步执行天气查询"""
        return self._run(city, format)


def create_weather_tool():
    """创建天气查询工具实例"""
    return WeatherTool()

if __name__ == '__main__':
    x = create_weather_tool()
    s = x._run("成都")
    print(s)