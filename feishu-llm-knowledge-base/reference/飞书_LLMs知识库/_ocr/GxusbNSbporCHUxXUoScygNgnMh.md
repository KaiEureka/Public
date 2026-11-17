以 LayerNorm 为例，对于输入 $x$，输出 $y = \gamma \hat{x} + \beta$，反向传播的梯度 $\frac{\partial L}{\partial x}$ 可以分解为多个部分。归一化层的梯度具有以下关键特性：

- **梯度去相关效应**：由于 $\hat{x} = (x - \mu)/\sigma$，该变换引入了与其他输入维度的依赖（通过 $\mu$ 和 $\sigma$）。因此，$\frac{\partial y}{\partial x}$ 不是对角矩阵，这意味着梯度在通过 LayerNorm 后会被“重新分配”，减小了不同维度梯度之间的相关性，有利于加速收敛（类似于白化效应）。
