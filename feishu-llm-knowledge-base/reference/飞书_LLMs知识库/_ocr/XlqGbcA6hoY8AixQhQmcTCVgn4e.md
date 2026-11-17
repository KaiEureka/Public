$$
h_t=\overline{\mathbf{A}}(\Delta_t)h_{t-1}+\overline{\mathbf{B}}(\Delta_t,x_t)x_t
$$

其中步长 $\Delta_t$ 是输入 $x_t$ 的函数。在离散化过程中，$\Delta_t$ 直接影响状态转移矩阵 $\overline{\mathbf{A}}$ 的“遗忘速率”。如果 $\Delta_t$ 很小，$h_{t-1}$ 的贡献就小，模型更多地关注当前输入；如果 $\Delta_t$ 很大，则历史信息被更大程度地保留。
