import pandas as pd

# 读取 data.txt 文件
df = pd.read_csv("data.txt", delim_whitespace=True, header=None,
                 names=["year", "category", "process", "yield_all", "yield_none"])

# 替换 category 中的下划线为连字符
df["category"] = df["category"].str.replace("_", "-")

# 按年份分组
grouped_by_year = df.groupby("year")

# 为每个年份生成一个单独的 LaTeX 文件
for year, year_group in grouped_by_year:
    # 按 category 分组
    grouped_by_category = year_group.groupby("category")

    # 创建一个 LaTeX 文件并写入开头部分
    with open(f"tables_{year}.tex", "w") as f:
        # 写入文档开头
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage{longtable}\n")
        f.write("\\begin{document}\n")

        # 为每个 category 生成 LaTeX 表格并追加到文件中
        for category, group in grouped_by_category:
            # 写入表格标题
            f.write(f"\\section*{{Category: {category}}}\n")
            f.write("\\begin{longtable}[c]{|l|l|r|r|}\n")
            f.write("\\hline\n")
            f.write(f"\\multicolumn{{4}}{{|c|}}{{\\textbf{{{year}: {category}}}}} \\\\\n")
            f.write("\\hline\n")
            f.write("\\textbf{Category} & \\textbf{Process} & \\textbf{Yield All} & \\textbf{Yield None} \\\\\n")
            f.write("\\hline\n")
            f.write("\\endfirsthead\n")
            f.write("\\hline\n")
            f.write(f"\\multicolumn{{4}}{{|c|}}{{\\textbf{{{year}: {category}}}}} \\\\\n")
            f.write("\\hline\n")
            f.write("\\textbf{Category} & \\textbf{Process} & \\textbf{Yield All} & \\textbf{Yield None} \\\\\n")
            f.write("\\hline\n")
            f.write("\\endhead\n")

            # 写入表格内容
            for _, row in group.iterrows():
                f.write(f"{row['category']} & {row['process']} & {row['yield_all']} & {row['yield_none']} \\\\\n")
                f.write("\\hline\n")

            f.write("\\end{longtable}\n\n")

        # 写入文档结尾部分
        f.write("\\end{document}\n")
