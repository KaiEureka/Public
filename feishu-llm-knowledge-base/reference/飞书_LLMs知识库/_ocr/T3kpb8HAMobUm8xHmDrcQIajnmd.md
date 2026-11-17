$$
\nabla_\theta \mathcal{L}_{\text{DPO}} \propto -\nabla_\theta \left( \log \frac{\pi_\theta(y_w)}{\pi_{\text{ref}}(y_w)} - \log \frac{\pi_\theta(y_l)}{\pi_{\text{ref}}(y_l)} \right)
$$

其中，$\pi_{\text{ref}}$ 的对数概率在梯度计算中作为常数被减去，但它会影响梯度的尺度和方向。
