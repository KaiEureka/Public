LayerNorm 的计算复杂度为 $O(n \cdot d)$，其中 n 是序列长度，d 是特征维度。而 Transformer 中的自注意力计算复杂度为 $O(n^2 \cdot d)$。当序列长度增加时，注意力的计算量呈平方增长，远超 LayerNorm 的线性增长。因此，LayerNorm 在整个推理耗时中的占比极小（通常 <1%），不会成为瓶颈。
