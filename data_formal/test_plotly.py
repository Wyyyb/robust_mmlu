import plotly.express as px

# 定义数据
data = {
    'Subject': ['Business', 'Law', 'Psychology', 'Biology', 'Chemistry',
                'History', 'Other', 'Health', 'Economics', 'Math',
                'Physics', 'Computer Science', 'Philosophy', 'Engineering'],
    'Count': [796, 1120, 818, 722, 1143, 390, 942, 825, 861, 1357, 1312, 418, 511, 972]
}

# 创建饼状图
fig = px.pie(data, values='Count', names='Subject', title='Distribution of Disciplines in MMLU-Pro')

# 保存图像
fig.write_image("image.png")
