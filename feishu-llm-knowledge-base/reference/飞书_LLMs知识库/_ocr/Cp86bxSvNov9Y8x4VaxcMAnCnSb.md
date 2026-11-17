**参数量增加**：

相比标准 FFN（两个线性层：`fc1` 和 `fc2`），SwiGLU 引入了第三个线性层（门控投影）。假设模型维度为 $d$，原始 FFN 隐藏维度 $d_{ff} = 4d$，参数量为：

$$
2 \cdot d \cdot d_{ff} = 8d^2
$$

若 SwiGLU 同样使用隐藏维度 $d_{ff}$，参数量将变为：

$$
3 \cdot d \cdot d_{ff} = 12d^2 \text{（假设 } \texttt{down\_proj} \text{ 的输入维度等于 } \texttt{up\_proj} \text{ 和 } \texttt{gate\_proj} \text{ 的输出维度，即 } d_{ff}\text{）。}
$$

为控制总参数量，通常会缩小 SwiGLU 的中间层维度。如果希望参数量与标准 FFN 相当，可设 SwiGLU 的中间维度为 $\frac{8}{3}d$ 左右（具体推导：解 $3 \cdot d \cdot d' = 8d^2$ 得 $d' = \frac{8}{3}d$）。因此，现代大模型（如 LLaMA）采用 $d_{ff} = \frac{8}{3}d$ 并取整。这样总参数量基本保持不变，同时获得门控机制的益处。
