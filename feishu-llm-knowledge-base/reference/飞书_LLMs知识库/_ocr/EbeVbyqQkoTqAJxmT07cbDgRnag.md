- 输入序列长度为 $n$，嵌入维度为 $d_{\text{model}}$。
- 设有 $h$ 个注意力头，每个头的维度为 $d_k=d_{\text{model}}/h$。
- 对于每个头 $i$，通过权重矩阵 $W_Q^i,W_K^i,W_V^i\in\mathbb{R}^{d_{\text{model}}\times d_k}$ 生成查询（Query）、键（Key）、值（Value）：

$$
Q_i=XW_Q^i,\quad K_i=XW_K^i,\quad V_i=XW_V^i
$$

- 每个头独立计算缩放点积注意力：

$$
\mathrm{Head}_i=\mathrm{softmax}\left(\frac{Q_iK_i^T}{\sqrt{d_k}}\right)V_i
$$

- 所有头的输出沿最后一维拼接，再用 $W_O\in\mathbb{R}^{hd_k\times d_{\text{model}}}$ 映射回 $d_{\text{model}}$。
