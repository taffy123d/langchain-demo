"""
天气查询技能模块
导出天气查询工具
"""

from .get_weather import create_weather_tool, WeatherTool

__all__ = ["create_weather_tool", "WeatherTool"]