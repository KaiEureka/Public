回顾 BM25 公式的分母部分：$f(q_i, D) + k_1 \cdot (1 - b + b \cdot \frac{|D|}{\text{avgdl}})$。其中，`|D|/avgdl` 是当前文档长度与平均长度的比值。参数 `b` 控制了这个比值对最终评分的影响程度。
