import os
import pandas as pd

# 文件夹路径
folder_path = r"C:\\Users\\DELL\\Desktop\\工具\\文件夹模板\\Trial Master File\\01试验管理"
# folder_path = "../"
data = {"name": []}
for root, dirs,files in os.walk(folder_path): # 获取文件夹中的所有文件名
 for file in files:
  data["name"].append(os.path.join(root, file))
print(data)
df = pd.DataFrame(data)
df.to_excel('file_names.xlsx')

