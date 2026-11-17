**典型PyTorch实现流程**（以输入 $X\in\mathbb{R}^{B\times N\times D}$，$D$ 为 $d_{model}$，$H$ 为头数，$d_k=D/H$ 为例）：

1. **一次性投影**：使用合并的权重矩阵 $W_Q\in\mathbb{R}^{D\times D}$（将 $H$ 个共小的 $W_Q^{(i)}$ 沿列拼接），计算 $Q=X@W_Q$，形状为 $(B,N,D)$。对K、V同理。这一步产生了所有头的完整Q、K、V，尚未区分头。
2. **重塑与转置**：
    - `Q = Q.view(B, N, H, d_k).transpose(1, 2)` → 形状 $(B,H,N,d_k)$。
    - 这一步是精髓：通过 `view` 将 $D$ 维拆成 $H\times d_k$，然后通过 `transpose` 将头维度移到batch维度之后，使得张量变为 `(batch_size, num_heads, seq_len, head_dim)`。现在，`H` 和 `B` 在逻辑上都作为并行的批次维度。
