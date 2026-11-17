1. 计算缩放点积注意力分数：$S = QK^T/\sqrt{d_k}$，形状为 $[n, n]$，其中 $S_{ij}$ 表示 query $i$ 对 key $j$ 的分数。
2. 构建偏置矩阵 $B$，其元素 $B_{ij}$ 仅取决于相对距离 $j - i$：

$$
B_{ij} = -m \cdot (j - i), \quad \text{对于 } j \geq i \text{（因果掩码允许的范围内）}
$$
