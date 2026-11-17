1. 从 HBM 加载 Q、K 矩阵到片上，计算得分矩阵 $S = QK^T$（大小 $n \times n$），写回 HBM。
2. 从 HBM 加载 $S$，计算 softmax 得到注意力权重 $P$（大小 $n \times n$），写回 HBM。
3. 从 HBM 加载 $P$ 和 $V$，计算输出 $O = PV$，写回 HBM。
