3. **计算 TD 误差**：$\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$。它代表了当前步的实际价值 $r_t + \gamma V(s_{t+1})$ 与预期价值 $V(s_t)$ 之间的偏差。
4. **GAE 计算**：$\hat{A}_t = \sum_{l=0}^{\infty} (\gamma\lambda)^l \delta_{t+l}$。这是对未来的 TD 误差进行指数衰减加权求和。
