给定 $Q, K, V \in \mathbb{R}^{n \times d}$，注意力计算：

$$
A = \mathrm{softmax}\left(\frac{QK^T}{\sqrt{d}}\right), \quad O = AV
$$

假设损失 $L$ 对输出 $O$ 的梯度为 $\frac{\partial L}{\partial O}$，反向传播需要计算对 $Q, K, V$ 的梯度，以及对 softmax 输入的梯度。计算过程中需要以下前向中间量：

- **softmax 的输出** $A$（注意力权重矩阵）：计算 $\frac{\partial L}{\partial V} = A^T \frac{\partial L}{\partial O}$ 以及对 softmax 输入的反向梯度公式需用到 $A$。
- **或 softmax 的输入** $S = QK^T/\sqrt{d}$：若保留 $S$，可通过导数和 $A$ 的关系计算。
- $V$ 本身：用于计算关于 $A$ 的梯度。
- $Q, K$（可选，取决于实现）：通过 $S$ 进一步反传到 $Q, K$。
