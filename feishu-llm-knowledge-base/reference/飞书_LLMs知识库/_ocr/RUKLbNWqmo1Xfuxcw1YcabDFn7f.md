将 $Q$ 按头写为块矩阵 $[Q_1;Q_2;\ldots;Q_h]$（沿头维度堆叠）。$K,V$ 分别为单个矩阵 $K,V\in\mathbb{R}^{s_{kv}\times d}$。注意力输出：

$$
\mathrm{Output}=\begin{bmatrix}\mathrm{softmax}\left(\frac{Q_1K^T}{\sqrt{d}}\right)V\\\mathrm{softmax}\left(\frac{Q_2K^T}{\sqrt{d}}\right)V\\\vdots\\\mathrm{softmax}\left(\frac{Q_hK^T}{\sqrt{d}}\right)V\end{bmatrix}
$$
