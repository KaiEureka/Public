这是现代大模型训练中最经典的学习率调度策略。假设总训练步数为 $T$，warmup 步数为 $T_w$，最大学习率为 $\eta_{\max}$，最小学习率为 $\eta_{\min}$。

学习率 $\eta_t$ 在步数 $t$ 的计算公式为：

$$
\eta_t = \begin{cases} \dfrac{t}{T_w} \cdot \eta_{\max}, & \text{if } t < T_w \\[2ex] \eta_{\min} + \dfrac{1}{2}(\eta_{\max} - \eta_{\min})\left(1 + \cos\left(\pi \cdot \dfrac{t - T_w}{T - T_w}\right)\right), & \text{if } t \geq T_w \end{cases}
$$

**曲线形状**（文本描述）：

- 在 $[0, T_w]$ 阶段，学习率从 0 线性增长到 $\eta_{\max}$，是一条上升的直线。
- 在 $[T_w, T]$ 阶段，学习率遵循余弦曲线从 $\eta_{\max}$ 平滑下降到 $\eta_{\min}$。该曲线在 $t = T_w$ 时斜率为 0（与线性段平滑衔接），在 $t = T$ 时接近 $\eta_{\min}$。
