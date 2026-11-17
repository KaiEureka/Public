- **Min-Max 归一化**：$Score_{norm} = \frac{Score - Score_{min}}{Score_{max} - Score_{min}}$。将分数缩放到 `[0,1]` 区间。
- **Z-Score 归一化**：$Score_{norm} = \frac{Score - \mu}{\sigma}$。将分数转换为均值为 0、标准差为 1 的标准分布。

归一化后，通过加权和得到最终分数：

$$
Score_{final}(d) = w_{dense} \cdot Score_{dense\_norm}(d) + w_{sparse} \cdot Score_{sparse\_norm}(d)
$$
