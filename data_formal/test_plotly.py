import plotly.express as px
import plotly.io as pio
pio.kaleido.scope.mathjax = None

# Define source data
src_data = {
    'Source': ['Original MMLU Questions', 'TheoremQA', 'STEM Website', 'Scibench'],
    'Count': [6810, 598, 4083, 541]
}

# Create a pie chart
fig = px.pie(src_data, values='Count', names='Source')

# Update layout settings including title and legend font sizes
fig.update_layout(
    width=1200,
    height=800,
    title_text="Data Source Distribution in MMLU-Pro",  # Set the title of the chart
    title_font=dict(family="Book Antiqua", size=42),  # Set title font
    legend_font=dict(family="Book Antiqua", size=36),  # Set legend font
    font=dict(family="Book Antiqua", size=28)  # Default font for all text
)
fig.update_traces(textfont=dict(family="Book Antiqua", size=36))
# Save the image
# fig.write_image("data_source_distribution.eps", scale=2)
fig.write_image("data_source_distribution.pdf", scale=2)

# Define subject data
data = {
    'Subject': ['Business', 'Law', 'Psychology', 'Biology', 'Chemistry',
                'History', 'Other', 'Health', 'Economics', 'Math',
                'Physics', 'Computer Science', 'Philosophy', 'Engineering'],
    'Count': [789, 1101, 798, 717, 1132, 381, 924, 818, 844, 1351, 1299, 410, 499, 969]
}

# Create a pie chart
fig = px.pie(data, values='Count', names='Subject')

# Update layout settings including title and legend font sizes
fig.update_layout(
    width=1200,
    height=800,
    title_text="Distribution of Disciplines in MMLU-Pro",  # Set the title of the chart
    title_font=dict(family="Book Antiqua", size=42),  # Set title font
    legend_font=dict(family="Book Antiqua", size=36),  # Set legend font
    font=dict(family="Book Antiqua", size=28)  # Default font for all text
)
fig.update_traces(textfont=dict(family="Book Antiqua", size=36))
# Save the image
# fig.write_image("subject_distribution.eps", scale=2)
fig.write_image("subject_distribution.pdf", scale=2)

