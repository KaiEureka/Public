（如 `[MASK]`、随机词或保持不变），得到被破坏的序列 $\tilde{\mathbf{x}}$。

BERT 使用双向 Transformer 编码器处理 $\tilde{\mathbf{x}}$，得到每个位置的上下文表示 $\mathbf{h}_i \in \mathbb{R}^d$。然后，对于每个被掩码位置 $i$，通过一个分类头（通常是与输入嵌入矩阵共享权重的线性层）将 $\mathbf{h}_i$ 映射为词汇表上的概率分布：

$$
P_\theta(x_i \mid \tilde{\mathbf{x}}) = \mathrm{softmax}(\mathbf{W}\mathbf{h}_i + \mathbf{b})_{x_i},
$$

其中 $\mathbf{W} \in \mathbb{R}^{V \times d}, \mathbf{b} \in \mathbb{R}^V$，$V$ 为词汇量大小。
