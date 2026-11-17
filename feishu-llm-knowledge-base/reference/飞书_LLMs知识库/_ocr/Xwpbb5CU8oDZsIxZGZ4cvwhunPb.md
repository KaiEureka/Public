**相加过程**：

对于序列中的第 $pos$ 个 token（经过 WordPiece 分词），从 Token Embedding 矩阵中取出它的词向量 $e_{tok}$；从 Segment Embedding 中取出其所属句子的段向量 $e_{seg}$（通常 0 或 1）；从 Position Embedding 矩阵中取出位置 $pos$ 对应的位置向量 $e_{pos}$。然后将三者逐元素相加：

$$
\mathrm{input}_i = e_{tok} + e_{seg} + e_{pos}
$$
