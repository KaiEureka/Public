1. **输入**：前一层的输出特征 $x\in\mathbb{R}^d$。
2. **下投影层 (Down-Projection)**：一个线性层 $W_{down}\in\mathbb{R}^{d\times r}$，将输入 $x$ 从原始维度 $d$ 映射到一个极低的瓶颈维度 $r$（$r\ll d$，例如 $r=64$）。
3. **非线性激活函数**：通常是 GeLU 或 ReLU，用于引入非线性，增强模型的表达能力。
4. **上投影层 (Up-Projection)**：另一个线性层 $W_{up}\in\mathbb{R}^{r\times d}$，将低维特征映射回原始维度 $d$。
5. **残差连接**：Adapter 的最终输出是其自身的计算结果加上原始的输入 $x$，即 $h=x+W_{up}\cdot\mathrm{ReLU}(W_{down}\cdot x)$。
