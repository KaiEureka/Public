具体而言，对于序列中位置为 $m$ 的 token，我们将其查询向量 $q_m$ 和键向量 $k_n$（位置 $n$）分别乘以一个与位置相关的旋转矩阵 $R_m$ 和 $R_n$：

$$
q'_m = R_m q_m, \quad k'_n = R_n k_n
$$

其中 $R_m$ 是一个分块对角矩阵，每个 $2 \times 2$ 块的形式为：

$$
\begin{pmatrix} \cos m\theta_i & -\sin m\theta_i \\ \sin m\theta_i & \cos m\theta_i \end{pmatrix}
$$

这里 $\theta_i = 10000^{-2i/d}$ 是第 $i$ 个维度对的旋转频率，$d$ 是向量维度，$i = 0, 1, \ldots, d/2 - 1$。
