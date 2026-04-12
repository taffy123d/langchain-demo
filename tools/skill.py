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

    def _run() -> str:
      pass

def create_weather_tool():
    """创建天气查询工具实例"""
    return WeatherTool()