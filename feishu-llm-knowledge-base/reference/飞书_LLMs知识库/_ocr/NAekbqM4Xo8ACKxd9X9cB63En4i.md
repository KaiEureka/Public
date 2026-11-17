1. **前向传播**：如前所述，前缀作为 Key-Value 被拼接，参与自注意力的计算。最终的输出是 Value 的加权和，这个“权”是由 Query 和 Key（包括前缀 Key）决定的。
2. **反向传播**：损失函数 $L$ 对前缀参数 $P$ 的梯度 $\frac{\partial L}{\partial P}$，通过链式法则，会流经注意力分数矩阵 $S=Q\cdot K^T$。
