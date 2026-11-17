4. **监控 chosen 和 rejected 的概率比**：观察损失函数内部的核心部分——$\log(\pi_\theta(y_w)/\pi_{\text{ref}}(y_w)) - \log(\pi_\theta(y_l)/\pi_{\text{ref}}(y_l))$ 的分布。如果这个差值变得异常巨大，说明模型在 $y_w$ 和 $y_l$ 上分配的概率失衡，是过拟合的表现。
