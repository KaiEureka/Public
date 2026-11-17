设教师模型在时间步 $t$ 的输出logits为 $z_t^T$，学生模型为 $z_t^S$。经过温度 $T$ 的softmax后得到概率分布：

$$
P_T(y_t|x_{<t}) = \mathrm{softmax}(z_t^T/T), \quad P_S(y_t|x_{<t}) = \mathrm{softmax}(z_t^S/T)
$$

蒸馏损失为所有时间步的平均KL散度，并乘以 $T^2$ 以补偿温度对梯度缩放的影响：

$$
\mathcal{L}_{\mathrm{KD}} = \frac{1}{L}\sum_{t=1}^{L} T^2 \cdot \mathrm{KL}\left(P_T(y_t|x_{<t}) \parallel P_S(y_t|x_{<t})\right)
$$
