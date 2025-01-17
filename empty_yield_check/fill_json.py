import json

# 假设你有这样的输出数据
raw_output = """
0bh3h
ProbMultiH_regubin
c3_0_d4_0 : 0.0180357
c3_0_d4_99 : 0.435691
c3_0_d4_m1 : 0.00381525
c3_19_d4_19 : 6.07797
c3_1_d4_0 : 0.00268206
c3_1_d4_2 : 0.0015165
c3_2_d4_m1 : 0.00478217
c3_4_d4_9 : 0.0134154
c3_m1_d4_0 : 0.00794499
c3_m1_d4_m1 : 0.00784359
c3_m1p5_d4_m0p5 : 0.0123798
"""

# 处理输出数据
lines = raw_output.strip().split('\n')
header = lines[0]  # 例如 "0bh3h"
results = {}

for line in lines[2:]:  # 从第三行开始
    key, value = line.split(':')
    key = key.strip()
    value = float(value.strip())
    
    # 填充结果字典
    if key not in results:
        results[key] = {}
    
    results[key][header] = {
        "nominal": {
            "run2": [value]
        }
    }

# 输出为 JSON 字符串
json_output = json.dumps(results, indent=4)
print(json_output)

# 可选：将结果写入文件
with open('output.json', 'w') as f:
    f.write(json_output)
