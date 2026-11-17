标准 softmax 对于向量 $x$ 计算：$\mathrm{softmax}(x_i)=\frac{e^{x_i-\max(x)}}{\sum_je^{x_j-\max(x)}}$，减去最大值是为了防止指数溢出。但在分块计算时，我们无法一次性获取整个行的最大值，因此 FlashAttention 使用 **online softmax** 技术，动态更新最大值和归一化因子。
