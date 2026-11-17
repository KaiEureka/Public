$$
\sin(pos + k) = \sin(pos)\cos(k) + \cos(pos)\sin(k)
$$

$$
\cos(pos + k) = \cos(pos)\cos(k) - \sin(pos)\sin(k)
$$

这意味着，存在一个只与 $k$ 相关的旋转矩阵 $R_k$，使得：

$$
\begin{pmatrix} PE_{(pos+k,2i)} \\ PE_{(pos+k,2i+1)} \end{pmatrix} = R_k \cdot \begin{pmatrix} PE_{(pos,2i)} \\ PE_{(pos,2i+1)} \end{pmatrix}
$$

其中

$$
R_k = \begin{pmatrix} \cos(\omega_i k) & \sin(\omega_i k) \\ -\sin(\omega_i k) & \cos(\omega_i k) \end{pmatrix}
$$
