import re

text = " The annual depreciation by the straight line method is calculated as follows:\n\n1. Determine the total depreciation over the 4 years:\n   \\[\n   \\text{Total depreciation} = \\text{Initial cost} - \\text{Resale value} = 80 - 15 = 65\n   \\]\n\n2. Calculate the annual depreciation:\n   \\[\n   \\text{Annual depreciation} = \\frac{\\text{Total depreciation}}{\\text{Number of years}} = \\frac{65}{4} = 16.25\n   \\]\n\nNext, we calculate the annual rate of depreciation:\n\n1. Determine the initial cost and the total depreciation:\n   \\[\n   \\text{Initial cost} = 80\n   \\]\n   \\[\n   \\text{Total depreciation} = 65\n   \\]\n\n2. Calculate the annual rate of depreciation:\n   \\[\n   \\text{Annual rate of depreciation} = \\left( \\frac{\\text{Total depreciation}}{\\text{Initial cost}} \\right) \\times 100 = \\left( \\frac{65}{80} \\right) \\times 100 = 81.25\\%\n   \\]\n\nHowever, since the options provided are in terms of annual depreciation and annual rate of depreciation, we need to match the calculated values with the options:\n\n- Annual depreciation: $16.25 per year\n- Annual rate of depreciation: 20.3%\n\nThus, the correct option is:\n\\[\n\\boxed{B}\n\\]"

pattern = r"[A-J](?=[^A-J]*$)"

# 搜索匹配的内容
match = re.search(pattern, text)

if match:
    print("提取的最后一个大写字母是:", match.group(0))
else:
    print("没有找到匹配的大写字母。")





