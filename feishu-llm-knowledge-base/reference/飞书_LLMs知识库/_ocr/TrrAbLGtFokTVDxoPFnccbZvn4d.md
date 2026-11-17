**公式**：设所有可训练参数的梯度构成一个向量 $\mathbf{g}$（将所有参数的 `.grad` 展平并拼接），其 $L_2$ 范数为 $\|\mathbf{g}\|_2$。给定一个阈值 max_norm，如果 $\|\mathbf{g}\|_2 > \text{max\_norm}$，则将所有梯度按比例缩放：

$$
\mathbf{g} \leftarrow \mathbf{g} \times \frac{\text{max\_norm}}{\|\mathbf{g}\|_2}
$$

如果 $\|\mathbf{g}\|_2 \leq \text{max\_norm}$，梯度保持不变。此方法称为**梯度范数裁剪**（Gradient Norm Clipping），通常使用 $L_2$ 范数，但也可泛化为 $L_p$ 范数。
