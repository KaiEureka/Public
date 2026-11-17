我们可以将 $Q$ 按头切分为 $h$ 个块，每个块为 $Q_i\in\mathbb{R}^{b\times s_q\times d}$。对于所有 $i=1\ldots h$，它们与同一个 $K$（去掉头维度为 $b\times s_{kv}\times d$）和 $V$ 进行计算。

1. **计算注意力分数**：每个头独立计算 $\mathrm{Score}_i=Q_iK^T/\sqrt{d}$，得到形状 $[b,s_q,s_{kv}]$。由于 $K$ 对所有 $i$ 相同，我们可以通过矩阵运算一次性完成：将 $Q$ 重塑为 $[b,s_q,h,d]$，$K$ 扩展为 $[b,s_{kv},h,d]$（或者利用广播），计算 `einsum('bqhd,bkhd->bhqk', Q, K)` 或直接利用 PyTorch 的广播机制：`scores = torch.matmul(Q, K.transpose(-2, -1))`，其中 Q 为 [b, h, s_q, d]，K 为 [b, 1, s_{kv}, d]，广播后自动匹配。
