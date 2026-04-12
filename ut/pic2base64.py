import base64
from pathlib import Path
from typing import Optional

def image_to_base64(image_path: str) -> Optional[str]:
    """
    将本地图片文件转换为 Base64 编码字符串。
    
    适用于多模态模型上传本地图片的场景。
    
    Args:
        image_path: 图片文件的本地路径 (字符串)
        
    Returns:
        Base64 编码字符串 (不含 data URI scheme 前缀)，如果读取失败则返回 None
    """
    try:
        # 使用 Path 处理路径，兼容性更好
        path = Path(image_path)
        
        # 检查文件是否存在
        if not path.exists():
            print(f"错误：文件未找到 -> {image_path}")
            return None
            
        # 以二进制模式读取文件并进行 Base64 编码
        with open(path, "rb") as image_file:
            # 读取二进制数据
            binary_data = image_file.read()
            # 进行 Base64 编码 -> bytes -> 解码为 utf-8 字符串
            base64_encoded = base64.b64encode(binary_data).decode("utf-8")
            
        return base64_encoded
        
    except Exception as e:
        print(f"转换图片时发生错误: {e}")
        return None