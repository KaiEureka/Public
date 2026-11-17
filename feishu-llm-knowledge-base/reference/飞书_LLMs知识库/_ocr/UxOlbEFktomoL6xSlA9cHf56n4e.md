$$
\mathbf{B}_t=s_B(x_t),\quad\mathbf{C}_t=s_C(x_t),\quad\Delta_t=\mathrm{softplus}(s_\Delta(x_t))
$$

其中 $s_B,s_C,s_\Delta$ 是简单的线性投影层。这使得SSM变为**时变系统**：

$$
h_t=\overline{\mathbf{A}}(\Delta_t)h_{t-1}+\overline{\mathbf{B}}(\Delta_t,x_t)x_t
$$
