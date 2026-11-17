$$
\delta L\approx\frac{1}{2}\delta w_q^2\cdot[H^{-1}]_{qq}^{-1}
$$

其中 $H$ 是损失对权重的海森矩阵。为保持输出不变，OBS 会在剪枝后对剩余权重执行更新：

$$
\delta w_{\text{remain}}=-\frac{w_q}{[H^{-1}]_{qq}}\cdot H_{:,q}^{-1}
$$
