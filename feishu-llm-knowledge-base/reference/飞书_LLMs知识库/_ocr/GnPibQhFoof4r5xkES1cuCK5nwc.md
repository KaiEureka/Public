**叠加方法**：

在注意力分数矩阵 $S = QK^T/\sqrt{d_k}$ 上，首先应用填充掩码 $M_{pad}$（形状为 `(batch, 1, 1, seq_len)` 或广播到 `(batch, 1, seq_len, seq_len)`），将 `<pad>` 对应位置的列全部设为 $-\infty$。然后应用因果掩码 $M_{causal}$（上三角为 $-\infty$，下三角为 0）。由于这两种掩码都是加性的（+0 或 + $-\infty$），它们可以直接相加：

$$
S_{\mathrm{masked}} = S + M_{pad} + M_{causal}
$$
