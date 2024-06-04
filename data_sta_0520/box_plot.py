import matplotlib.pyplot as plt
import numpy as np

# 设置风格和字体大小
plt.style.use('bmh')
plt.rcParams.update({'font.size': 15, 'figure.dpi': 120})

# 模型数据
models = ['Llama-2-7b-hf', 'Mistral-7B-v0.1', 'Mistral-7B-\nInstruct-v0.2',
          'gemma-7b', 'Meta-Llama-3-8B', 'Meta-Llama-3-8B-\nInstruct']

# 数据提取，只包含最小值和最大值
mmlu_data = np.array([
    [0.3418, 0.4516],
    [0.5732, 0.6149],
    [0.5452, 0.6027],
    [0.5865, 0.6222],
    [0.5992, 0.6481],
    [0.6137, 0.6604]
])

mmlu_pro_data = np.array([
    [0.1481, 0.1855],
    [0.2749, 0.2869],
    [0.2237, 0.2547],
    [0.2521, 0.2701],
    [0.2873, 0.3154],
    [0.3311, 0.3519]
])

fig, ax = plt.subplots(figsize=(10, 8))

# 绘制错误条图
bars_mmlu = ax.errorbar(models, np.mean(mmlu_data, axis=1), yerr=[np.mean(mmlu_data, axis=1) - mmlu_data[:, 0], mmlu_data[:, 1] - np.mean(mmlu_data, axis=1)],
                        fmt='o', label='MMLU', color='#0077B6', linewidth=2, capsize=5)
bars_mmlu_pro = ax.errorbar(models, np.mean(mmlu_pro_data, axis=1), yerr=[np.mean(mmlu_pro_data, axis=1) - mmlu_pro_data[:, 0], mmlu_pro_data[:, 1] - np.mean(mmlu_pro_data, axis=1)],
                            fmt='^', label='MMLU-Pro', color='#ff9d76', linewidth=2, capsize=5)

# 添加最小值和最大值的文本
for i in range(len(models)):
    ax.text(i, mmlu_data[i, 0] - 0.02, f'{mmlu_data[i, 0]:.4f}', ha='center', va='top', color='#0077B6')
    ax.text(i, mmlu_data[i, 1] + 0.02, f'{mmlu_data[i, 1]:.4f}', ha='center', va='bottom', color='#0077B6')
    ax.text(i, mmlu_pro_data[i, 0] - 0.02, f'{mmlu_pro_data[i, 0]:.4f}', ha='center', va='top', color='#ff9d76')
    ax.text(i, mmlu_pro_data[i, 1] + 0.02, f'{mmlu_pro_data[i, 1]:.4f}', ha='center', va='bottom', color='#ff9d76')

ax.set_ylabel('Performance Range')
ax.legend(loc='upper left')
ax.set_xticks(range(len(models)))  # 确保 x 轴标签正确
ax.set_xticklabels(models, rotation=30, ha="right")
ax.set_ylim(0.1, 0.8)  # 设置纵轴的区间为从0到0.7

plt.tight_layout()
plt.savefig('variance_comparison.png', dpi=300, bbox_inches='tight')
