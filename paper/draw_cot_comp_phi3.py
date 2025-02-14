import matplotlib.pyplot as plt
import numpy as np

# 设置风格和更大的字体
plt.style.use('bmh')
plt.rcParams.update({'font.size': 28, 'figure.dpi': 120})

tasks = ['MMLU', 'MMLU-Pro']
cot_scores = np.array([0.7936, 0.557])
non_cot_scores = np.array([0.78, 0.4749])

bar_width = 0.35
index = np.arange(len(tasks))

fig, ax = plt.subplots(figsize=(9, 6))
bar1 = ax.bar(index - bar_width / 2, cot_scores, bar_width, label='CoT', color='#0077b6')
bar2 = ax.bar(index + bar_width / 2, non_cot_scores, bar_width, label='Direct Answer', color='#ff9d76')

# # 在柱子上添加数值标签
# for rect in bar1 + bar2:
#     height = rect.get_height()
#     ax.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.3f}', ha='center', va='bottom')
plt.subplots_adjust(left=0.17, right=0.99, top=0.99, bottom=0.15)
ax.set_xlabel('Phi3-medium-4k-instruct')
ax.set_ylabel('Accuracy')
ax.set_xticks(index)
ax.set_xticklabels(tasks, rotation=0)
ax.legend()

ax.grid(True, linestyle='--', which='major', color='gray', alpha=0.5)

# plt.show()
plt.savefig("phi3.png", dpi=300)
