$$
\mathrm{SwiGLU}(x) = (xW_1 + b_1) \otimes \mathrm{Swish}(xW_g + b_g)
$$

其中：

- $W_1 \in \mathbb{R}^{d \times d_{ff}}, W_g \in \mathbb{R}^{d \times d_{ff}}$ 分别是信息和门控路径的权重。
- $\mathrm{Swish}(z) = z \cdot \sigma(z)$，$\sigma$ 是 sigmoid 函数。
- $\otimes$ 表示逐元素乘法（Hadamard 积）。
