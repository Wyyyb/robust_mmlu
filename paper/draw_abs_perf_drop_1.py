import matplotlib.pyplot as plt
import numpy as np

# 设置风格和更大的字体
plt.style.use('bmh')
plt.rcParams.update({'font.size': 16, 'figure.dpi': 120})

models = ['GPT-4o', 'Llama-3-70B\n-Instruct', 'Gemma-7B']
mmlu_scores = np.array([0.887, 0.82, 0.6603])
mmlu_pro_scores = np.array([0.7255, 0.562, 0.3373])

bar_width = 0.35
index = np.arange(len(models))

fig, ax = plt.subplots(figsize=(6, 8))
bar1 = ax.bar(index, mmlu_scores, bar_width, label='MMLU', color='#FFA500')
bar2 = ax.bar(index + bar_width, mmlu_pro_scores, bar_width, label='MMLU-Pro', color='#0077B6')

# 在柱子上添加数值
# for rect in bar1:
#     height = rect.get_height()
#     ax.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.3f}', ha='center', va='bottom')
#
# for rect in bar2:
#     height = rect.get_height()
#     # 调整 x 坐标以向右偏移
#     ax.text(rect.get_x() + rect.get_width() / 2.0 - 0.17, height, f'{height:.3f}', ha='left', va='bottom')

ax.set_xlabel('')
ax.set_ylabel('Accuracy')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(models, rotation=30, ha="right")
ax.legend()
ax.grid(True, linestyle='--', which='major', color='gray', alpha=0.5)

plt.savefig('performance_comparison.png', bbox_inches='tight', dpi=600)
