$$
\mathrm{SwiGLU}(x) = \mathrm{Swish}(xW_g + b_g) \odot (xW_1 + b_1)
$$

其中：

- $W_g, W_1$ 是不同线性变换的权重矩阵，$b_g, b_1$ 为偏置（可省略）。
- $\mathrm{Swish}(z) = z \cdot \sigma(z)$（SiLU）。
- $\odot$ 表示逐元素乘法。
