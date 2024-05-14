import plotly.express as px

# 定义学科数据
data = {
    'Subject': ['Business', 'Law', 'Psychology', 'Biology', 'Chemistry',
                'History', 'Other', 'Health', 'Economics', 'Math',
                'Physics', 'Computer Science', 'Philosophy', 'Engineering'],
    'Count': [796, 1120, 818, 722, 1143, 390, 942, 825, 861, 1357, 1312, 418, 511, 972]
}

# 创建饼状图
fig = px.pie(data, values='Count', names='Subject', title='Distribution of Disciplines in MMLU-Pro')

# 更新布局设置，包括标题和图例的字体大小
fig.update_layout(
    width=1200,
    height=800,
    title_font_size=32,  # 设置标题字体大小
    legend_title_font_size=20,  # 设置图例标题字体大小
    legend_font_size=28,  # 设置图例字体大小
)

# 保存图像
fig.write_image("subject_dis.png", scale=2)

# 定义来源数据
src_data = {
    'Source': ['Original MMLU Questions', 'TheoremQA', 'STEM Website', 'Scibench'],
    'Count': [6933, 599, 4111, 544]
}

# 创建饼状图
fig = px.pie(src_data, values='Count', names='Source', title='Data Source Distribution in MMLU-Pro')

# 更新布局设置，包括标题和图例的字体大小
fig.update_layout(
    width=1200,
    height=800,
    title_font_size=32,  # 设置标题字体大小
    legend_title_font_size=20,  # 设置图例标题的字体大小
    legend_font_size=28,  # 设置图例的字体大小
)

# 保存图像
fig.write_image("data_source_distribution.png", scale=2)


