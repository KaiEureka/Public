- 原始 logits 向量为 $z = [z_1, z_2, \ldots, z_V]$。
- 假设 token $k$ 是已生成的 token，其被惩罚后的 logit 为 $\tilde{z}_k = z_k - \delta$，其中 $\delta > 0$。（注意，乘性惩罚 $\tilde{z}_k = z_k / c$ 也等价于在 log 空间中减去一个正数 $\delta = z_k(1 - 1/c)$，由于通常 $c > 1$，且对于高概率 token 其 $z_k$ 较大且为正，因此 $\delta > 0$。）
- 其他所有 token 的 logits 保持不变。

**推导**：
原始概率分布为 $P_i = \frac{e^{z_i}}{S}$，其中 $S = \sum_j e^{z_j}$。
惩罚后的概率分布为 $\tilde{P}_i = \frac{e^{\tilde{z}_i}}{\tilde{S}}$，其中 $\tilde{z}_i = z_i$ for $i \neq k$，且 $\tilde{z}_k = z_k - \delta$。
