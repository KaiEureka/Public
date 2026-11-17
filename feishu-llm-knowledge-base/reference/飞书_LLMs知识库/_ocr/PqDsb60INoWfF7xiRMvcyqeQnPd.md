为了在计算机上处理离散序列，需要将连续SSM离散化。给定一个步长（或采样间隔）Δ，常用的离散化方法有双线性变换、零阶保持等。离散化后得到：

$$
\begin{aligned}
h_t&=\overline{\mathbf{A}}h_{t-1}+\overline{\mathbf{B}}x_t\\
y_t&=\mathbf{C}h_t+\mathbf{D}x_t
\end{aligned}
$$

其中 $\overline{\mathbf{A}}=f(\mathbf{A},\Delta)$ 和 $\overline{\mathbf{B}}=g(\mathbf{B},\mathbf{A},\Delta)$ 是离散化后的矩阵，包含了步长信息。在S4等结构化SSM中，$\mathbf{A}$ 被设计为特定的形式（如HiPPO矩阵），以捕捉长期记忆，并通过高效的卷积计算实现并行训练。
