$$
Y=\left(L\circ(QK^T)\right)V
$$

其中 $L$ 是一个由 $a_j$ 决定的1-半可分掩码矩阵，$Q,K,V$ 由输入 $x$ 通过投影得到。这与Transformer的多头注意力公式 $\mathrm{softmax}(QK^T)V$ 仅在归一化方式（softmax vs. 门控线性）和掩码矩阵的精细结构上有所不同。
