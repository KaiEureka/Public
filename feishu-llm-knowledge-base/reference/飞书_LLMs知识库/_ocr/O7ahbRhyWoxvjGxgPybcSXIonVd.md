$$
y_t\approx\frac{\sum_{i=1}^{t}e^{-(t-i)w+k_i}v_i}{\sum_{i=1}^{t}e^{-(t-i)w+k_i}}
$$

但更关键的是其RNN形式，它维护一个状态矩阵 $S_t$ 和归一化因子 $Z_t$，通过递归更新：

$$
S_t=e^{-w}S_{t-1}+e^{k_t}v_t^T,\quad Z_t=e^{-w}Z_{t-1}+e^{k_t}
$$

输出 $y_t=(r_t\odot\mathrm{sigmoid}(q_t))\cdot S_t/Z_t$，其中 $r_t$ 是接受门。

**本质区别**：

- **复杂度**：标准自注意力是 $O(n^2)$，WKV是 $O(n)$。
