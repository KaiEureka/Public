$$
\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( \beta \cdot \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \cdot \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]
$$

其中：

- $\pi_\theta$：待优化的策略模型（即我们最终想要的对齐模型）。
- $\pi_{\text{ref}}$：参考模型，通常为 SFT 模型，且在整个 DPO 训练过程中参数被冻结。
- $x$：提示，$y_w$ 和 $y_l$ 分别是偏好数据中的“较好回复”和“较差回复”。
- $\beta$：一个超参数，用于控制对参考模型的偏离程度。
- $\sigma$：sigmoid 函数。
