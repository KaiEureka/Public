1. 输入 $X$ 形状为 $(B,n,d_{model})$。
2. 使用合并后的权重矩阵一次性计算所有头的 Q, K, V，输出形状为 $(B,n,h\cdot d_k)$。
3. `reshape` 为 $(B,n,h,d_k)$，再 `transpose` 为 $(B,h,n,d_k)$。
4. 批量计算注意力分数 `scores = Q @ K^T / sqrt(d_k)`，形状为 $(B,h,n,n)$。
5. softmax 并乘以 V，得到输出 $(B,h,n,d_k)$。
6. `transpose` 回 $(B,n,h,d_k)$，`reshape` 回 $(B,n,d_{model})$。
7. 通过 $W_O$ 线性投影。
