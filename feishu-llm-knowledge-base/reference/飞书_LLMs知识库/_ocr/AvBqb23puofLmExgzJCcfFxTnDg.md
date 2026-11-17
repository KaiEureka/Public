- **MSE Loss**：是最直接、最常用的损失函数。它的目标是让 Critic 模型预测的价值 $V(s_t)$ 尽可能接近通过 GAE 算法计算出的目标价值 $V_{target}$。

$$
\mathcal{L}_{Critic}^{MSE} = \frac{1}{N} \sum_t (V(s_t) - V_{target})^2
$$
