对于一个线性层 $Y=X\cdot W$，其中 $X\in\mathbb{R}^{b\times d_{\text{in}}}$，$W\in\mathbb{R}^{d_{\text{in}}\times d_{\text{out}}}$。AWQ 引入一个逐输入通道的缩放向量 $s\in\mathbb{R}^{d_{\text{in}}}$（全部为正）。变换过程为：

$$
\tilde{X}=X\cdot\mathrm{diag}(s)^{-1}\quad\text{（激活缩小）}
$$

$$
\tilde{W}=\mathrm{diag}(s)\cdot W\quad\text{（权重放大）}
$$

则变换后的前向计算为：

$$
\tilde{Y}=\tilde{X}\cdot\tilde{W}=(X\cdot\mathrm{diag}(s)^{-1})\cdot(\mathrm{diag}(s)\cdot W)
$$

由于对角矩阵乘法满足结合律且 $\mathrm{diag}(s)^{-1}\cdot\mathrm{diag}(s)=I$，有：

$$
\tilde{Y}=X\cdot W=Y
$$

因此，**数学上严格等效**，没有任何近似。

在实际量化中，我们对变换后的权重 $\tilde{W}$ 进行量化（得到 $\hat{W}$），而激活 $\tilde{X}$ 保持 FP16（W4A16 方案）。最终计算时：

$$
Y\approx\tilde{X}\cdot\hat{W}
$$

量化误差来源于 $\hat{W}\ne\tilde{W}$，但通过选择合适的 $s$，我们可以让量化误差对输出 $Y$ 的影响最小化——特别是保护那些对应大激活通道的权重行（输入通道维度上的权重向量），从而保证整体精度。
