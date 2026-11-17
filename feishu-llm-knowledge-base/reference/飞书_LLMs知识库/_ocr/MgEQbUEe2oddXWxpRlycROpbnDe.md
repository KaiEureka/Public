这是一个工程上更实用的方案。设定两个阈值：$T_{good}$ 和 $T_{bad}$。

- 评分 $\ge T_{good}$（如 4-5 星）：标记为 desirable，计算 $\mathcal{L}_D$。
- 评分 $\le T_{bad}$（如 1-2 星）：标记为 undesirable，计算 $\mathcal{L}_U$。
- 评分在 $T_{bad}$ 和 $T_{good}$ 之间（如 3 星）：这些中评可以被视为弱信号。我们可以选择忽略它们，或者对它们分别计算 $\mathcal{L}_D$ 和 $\mathcal{L}_U$，但赋予一个很小的权重 $\lambda_{neutral}$。

这种方法简单、可解释，且能有效地利用评分中的高置信度信息，同时避免了中评带来的噪声。
