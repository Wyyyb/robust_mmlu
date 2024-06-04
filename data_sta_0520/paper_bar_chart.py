import matplotlib.pyplot as plt
import numpy as np

# 设置风格和更大的字体
plt.style.use('bmh')
plt.rcParams.update({'font.size': 15, 'figure.dpi': 120})

models = [
    'GPT-4o', 'Claude-3-Opus', 'GPT-4-Turbo', 'Gemini-1.5-Flash',
    'Llama-3-70B-\nInstruct', 'Phi-3-medium-4k-\ninstruct', 'Qwen1.5-110B',
    'Yi-34B', 'Llama-2-70B', 'Gemma-7B'
]
mmlu_scores = np.array([0.887, 0.868, 0.865, 0.789, 0.82, 0.78, 0.802, 0.763, 0.697, 0.6603])
mmlu_pro_scores = np.array([0.7255, 0.6845, 0.6371, 0.5912, 0.562, 0.5348, 0.4993, 0.4303, 0.3753, 0.3373])

bar_width = 0.35
index = np.arange(len(models))

fig, ax = plt.subplots(figsize=(12, 8))
bar1 = ax.bar(index, mmlu_scores, bar_width, label='MMLU', color='#FFA500')
bar2 = ax.bar(index + bar_width, mmlu_pro_scores, bar_width, label='MMLU-Pro', color='#0077B6')

# 在柱子上添加数值
for rect in bar1:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.3f}', ha='center', va='bottom')

for rect in bar2:
    height = rect.get_height()
    # 调整 x 坐标以向右偏移
    ax.text(rect.get_x() + rect.get_width() / 2.0 - 0.2, height, f'{height:.3f}', ha='left', va='bottom')

ax.set_xlabel('')
ax.set_ylabel('Accuracy')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(models, rotation=30, ha="right")
ax.legend()
ax.grid(True, linestyle='--', which='major', color='gray', alpha=0.5)

plt.savefig('performance_comparison.png', bbox_inches='tight', dpi=300)
