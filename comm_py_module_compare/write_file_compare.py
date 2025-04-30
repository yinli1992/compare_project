def write_aligned_txt(data, filename):
    # 计算每列最大宽度（包含表头）
    headers = ["源表", "目标表", "源数据库", "目标数据库", "源字段", "目标字段", "差异类型", "描述"]
    col_widths = [len(h) for h in headers]

    for row in data:
        for i, item in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(item)))

    # 生成格式字符串（如："{:<15}{:<15}..."）
    format_str = "".join([f"{{:<{w + 2}}}" for w in col_widths]) + "\n"

    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(format_str.format(*headers))  # 表头
        for row in data:
            f.write(format_str.format(*map(str, row)))