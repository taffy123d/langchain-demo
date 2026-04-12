def md_read(file_path, default=""):
    try:
        # 用 utf-8-sig 自动去掉 Windows 保存的 BOM 乱码
        with open(file_path, "r", encoding="utf-8-sig") as f:
            content = f.read()

        # 可选：去除首尾空白（推荐，让提示词更干净）
        content = content.strip()

        # 你可以保留后缀判断，但不要阻止返回内容！
        if not file_path.endswith((".md", ".txt", ".tpl")):
            print(f"⚠️  警告：{file_path} 不是常见提示词格式")

        return content

    except FileNotFoundError:
        print(f"❌ 错误：提示词文件不存在 {file_path}")
    except PermissionError:
        print(f"❌ 错误：无权限读取 {file_path}")
    except Exception as e:
        print(f"❌ 读取提示词失败：{e}")

    # 绝不会返回 None！保证 Agent 可运行
    return default