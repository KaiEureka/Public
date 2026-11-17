设 $r=r_\theta(x,y)$，$z=z_{\mathrm{ref}}$。对于单个样本，其损失对 $r$ 的梯度为：

- **对于 Desirable 样本**：

$$
\frac{\partial\mathcal{L}_D}{\partial r}=-\lambda_D\cdot\beta\cdot\left(1-\sigma(\beta(r-z))\right)
$$
