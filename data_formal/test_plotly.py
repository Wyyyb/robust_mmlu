import plotly.express as px
import plotly.io as pio
pio.kaleido.scope.mathjax = None

# 定义来源数据
src_data = {
    'Source': ['Original MMLU Questions', 'TheoremQA', 'STEM Website', 'Scibench'],
    'Count': [6810, 598, 4083, 541]
}

# 创建饼状图
# fig = px.pie(src_data, values='Count', names='Source', title='Data Source Distribution in MMLU-Pro')
fig = px.pie(src_data, values='Count', names='Source')


# 更新布局设置，包括标题和图例的字体大小
fig.update_layout(
    width=1200,
    height=800,
    title_font_size=32,  # 设置标题字体大小
    legend_title_font_size=20,  # 设置图例标题的字体大小
    legend_font_size=28,  # 设置图例的字体大小
)
fig.update_traces(textfont_size=26)
# 保存图像
fig.write_image("data_source_distribution.eps", scale=2)
fig.write_image("data_source_distribution.pdf", scale=2)

# 定义学科数据
data = {
    'Subject': ['Business', 'Law', 'Psychology', 'Biology', 'Chemistry',
                'History', 'Other', 'Health', 'Economics', 'Math',
                'Physics', 'Computer Science', 'Philosophy', 'Engineering'],
    'Count': [789, 1101, 798, 717, 1132, 381, 924, 818, 844, 1351, 1299, 410, 499, 969]
}

# 创建饼状图
# fig = px.pie(data, values='Count', names='Subject', title='Distribution of Disciplines in MMLU-Pro')
fig = px.pie(data, values='Count', names='Subject')

# 更新布局设置，包括标题和图例的字体大小
fig.update_layout(
    width=1200,
    height=800,
    title_font_size=32,  # 设置标题字体大小
    legend_title_font_size=20,  # 设置图例标题字体大小
    legend_font_size=28,  # 设置图例字体大小
)
fig.update_traces(textfont_size=26)
# 保存图像
fig.write_image("subject_distribution.eps", scale=2)
fig.write_image("subject_distribution.pdf", scale=2)

