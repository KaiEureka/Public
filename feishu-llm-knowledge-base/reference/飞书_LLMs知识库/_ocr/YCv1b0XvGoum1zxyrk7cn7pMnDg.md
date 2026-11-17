$$
\begin{aligned}
\dot{h}(t)&=\mathbf{A}h(t)+\mathbf{B}x(t)\\
y(t)&=\mathbf{C}h(t)+\mathbf{D}x(t)
\end{aligned}
$$

其中：

- $x(t)\in\mathbb{R}$ 是输入信号（在深度学习中通常是输入序列在时刻 $t$ 的一个特征维度）。
- $h(t)\in\mathbb{R}^N$ 是系统的隐状态，$N$ 是状态的维度。
- $\mathbf{A}\in\mathbb{R}^{N\times N}$ 是状态转移矩阵，描述了系统内部状态的演化规律。
- $\mathbf{B}\in\mathbb{R}^{N\times1}$ 是输入矩阵，控制输入 $x(t)$ 如何影响状态。
- $\mathbf{C}\in\mathbb{R}^{1\times N}$ 是输出矩阵，将隐状态映射到输出 $y(t)$。
- $\mathbf{D}\in\mathbb{R}$ 是直接传输矩阵（通常可忽略或视为残差连接）。
