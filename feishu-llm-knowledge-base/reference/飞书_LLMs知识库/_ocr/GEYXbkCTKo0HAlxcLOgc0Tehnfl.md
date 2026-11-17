$$
\mathrm{Input} = \mathrm{TokenEmbedding} + \mathrm{SegmentEmbedding} + \mathrm{PositionEmbedding}
$$

其中：

- **Token Embedding**：对词表中的每个 token（子词）的嵌入向量，维度为 $d_{\mathrm{model}}$（BERT-base 中为 768）。
- **Segment Embedding**：用于区分句子对（A 句还是 B 句）的嵌入，形状同样为 $d_{\mathrm{model}}$，只有两个向量（0 和 1），在对应位置相加。
- **Position Embedding**：可学习的位置嵌入矩阵，大小通常为 $(512, 768)$（最大长度 512，维度 768）。根据 token 在输入序列中的位置索引（从 0 开始），查找对应的位置嵌入向量，形状为 $d_{\mathrm{model}}$。
