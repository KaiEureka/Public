**SmoothQuant 的核心思想**：利用矩阵乘法的线性等价变换，引入 per-channel 的平滑因子 $s\in\mathbb{R}^{d_{in}}$（$d_{in}$ 为输入通道数），重写线性层：

$$
Y=X\cdot W=(X\cdot\mathrm{diag}(s)^{-1})\cdot(\mathrm{diag}(s)\cdot W)=\hat{X}\cdot\hat{W}
$$

通过巧妙选择 $s$，可以**平滑激活 X 的离群值，同时将额外负担转嫁给更容易量化的权重 W**，最终使 $\hat{X}$ 和 $\hat{W}$ 都易于 INT8 量化。
