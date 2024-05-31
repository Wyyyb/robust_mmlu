import matplotlib.pyplot as plt
import numpy as np

# 创建数据
# 高斯分布数据
x = np.linspace(-5, 5, 100)
y1 = np.exp(-0.5 * (x - 1) ** 2)
y2 = np.exp(-0.5 * (x - 0) ** 2)
y3 = np.exp(-0.5 * (x + 1) ** 2)

# 柱状图数据
np.random.seed(0)
data1 = np.random.randn(100)
data2 = np.random.randn(100)
data3 = np.random.randn(100)
data4 = np.random.randn(100)
data5 = np.random.randn(100)

# 创建图形和子图网格
fig = plt.figure(figsize=(24, 8))  # 整个画布的大小

# 添加子图
# 左边的柱状图
ax1 = plt.subplot2grid((3, 4), (0, 0), rowspan=3)
ax1.hist(data1, bins=20, color='blue', alpha=0.7)
ax1.set_title('Histogram 1')

# 中间的三张高斯分布图
ax2 = plt.subplot2grid((3, 4), (0, 1), colspan=1)
ax2.plot(x, y1, 'r-')
ax2.set_title('Gaussian Distribution 1')

ax3 = plt.subplot2grid((3, 4), (1, 1), colspan=1)
ax3.plot(x, y2, 'g-')
ax3.set_title('Gaussian Distribution 2')

ax4 = plt.subplot2grid((3, 4), (2, 1), colspan=1)
ax4.plot(x, y3, 'b-')
ax4.set_title('Gaussian Distribution 3')

# 右边的四张柱状图
ax5 = plt.subplot2grid((3, 4), (0, 3))
ax5.hist(data2, bins=20, color='red', alpha=0.7)
ax5.set_title('Histogram 2')

ax6 = plt.subplot2grid((3, 4), (1, 3))
ax6.hist(data3, bins=20, color='green', alpha=0.7)
ax6.set_title('Histogram 3')

ax7 = plt.subplot2grid((3, 4), (2, 3))
ax7.hist(data4, bins=20, color='purple', alpha=0.7)
ax7.set_title('Histogram 4')

ax8 = plt.subplot2grid((3, 4), (0, 2))
ax8.hist(data5, bins=20, color='orange', alpha=0.7)
ax8.set_title('Histogram 5')

# 调整子图间距
plt.tight_layout()
plt.show()