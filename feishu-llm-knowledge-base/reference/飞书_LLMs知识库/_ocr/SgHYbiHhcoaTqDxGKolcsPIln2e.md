在标准的多头注意力中，输入 $X\in\mathbb{R}^{s\times d_{\text{model}}}$ 分别通过三个权重矩阵 $W_Q,W_K,W_V\in\mathbb{R}^{d_{\text{model}}\times d_{\text{head}}\cdot h}$ 得到 Q, K, V。

**融合方法**：

将三个权重矩阵在列维度上拼接，构造一个大的权重矩阵 $W_{QKV}\in\mathbb{R}^{d_{\text{model}}\times3\cdot d_{\text{head}}\cdot h}$。一次矩阵乘法计算：

$$
Y=X\cdot W_{QKV}
$$

得到的输出 $Y$ 形状为 $[s,3\cdot d_{\text{head}}\cdot h]$。然后将其在最后一个维度上等分为三份：Q, K, V，每份形状为 $[s,d_{\text{head}}\cdot h]$。
