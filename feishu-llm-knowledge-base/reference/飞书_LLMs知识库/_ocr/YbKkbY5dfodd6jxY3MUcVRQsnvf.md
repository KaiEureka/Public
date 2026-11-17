2. **动态惩罚**：对于候选 token $y_t$，查询以它为结尾的 n-gram 的计数。然后修改其 logit：$\tilde{z}_{y_t} = z_{y_t} - \lambda \cdot \text{ngram\_count}$。重复次数越多，惩罚越重。
