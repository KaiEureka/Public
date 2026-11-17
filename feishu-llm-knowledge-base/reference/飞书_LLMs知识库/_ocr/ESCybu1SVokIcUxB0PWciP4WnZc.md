对于第 $l$ 层的参数 $W^l$，设其梯度为 $G^l$。首先计算该层的**参数范数** $\|W^l\|_F$（Frobenius 范数）和**梯度范数** $\|G^l\|_F$。然后定义一个裁剪因子 $\lambda$（如 0.1）。如果：

$$
\|G^l\|_F > \lambda \cdot \|W^l\|_F
$$

则对该层梯度进行裁剪：

$$
G^l \leftarrow G^l \times \frac{\lambda \cdot \|W^l\|_F}{\|G^l\|_F}
$$
