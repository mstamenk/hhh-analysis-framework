import re

# 输入文件和输出文件路径
input_file = 'address.txt'
output_file = 'address_fxid.txt'

# 正则表达式模式
pattern = r'fxid:(\w{16})'

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        match = re.search(pattern, line)
        if match:
            fxid = match.group(1)
            outfile.write(fxid + '\n')

print(f'fxid finished,  saved in  {output_file} file')
