- **缩放因子 ($\alpha$)**：它是我们想要扩展的目标长度 $L_{\text{test}}$ 与训练长度 $L_{\text{train}}$ 的比值，$\alpha=L_{\text{test}}/L_{\text{train}}$。这个因子决定了我们NTK-aware缩放的强度，是**先验已知的**。
- **温度参数 ($\tau$)**：它的确定更复杂，YaRN提出一个经验公式，将其与**缩放因子 $\alpha$** 和**序列的实际相对距离**关联起来。核心思想是：当相对距离在训练窗口（$L_{\text{train}}$）以内时，我们希望温度 $\tau\approx1$，即不改变已训练好的注意力模式；当相对距离超出训练窗口时，我们希望温度逐渐减小，以锐化注意力分布。一个常用的简化公式是：

$$
\tau=\exp\left(\frac{-\Delta\cdot(\alpha-1)}{\alpha}\right)
$$
