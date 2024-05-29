import plotly.express as px

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
fig.write_image("data_source_distribution.pdf", scale=2)

