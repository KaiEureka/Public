1. 通过线性变换得到 Query、Key、Value 矩阵，形状均为 $(1, t, d)$，计算量为 $3 \times (t \times d \times d) \approx O(td^2)$。
2. 计算注意力分数：$QK^T$，形状为 $(1, t, t, d_k)$ 或 $(1, h, t, t)$，计算量为 $O(t^2 d)$。
3. Softmax 归一化：计算量为 $O(t^2)$。
4. 加权求和：将注意力权重与 Value 相乘，计算量为 $O(t^2 d)$。

总计算复杂度为 $O(td^2 + t^2 d)$。由于在实际 LLM 中 $d$ 是常数，且通常 $t \gg d$，因此主导项是 $O(t^2 d)$。
