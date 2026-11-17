$$
y_i=\frac{\sum_j\phi(q_i)^T\phi(k_j)v_j}{\sum_j\phi(q_i)^T\phi(k_j)}=\frac{\phi(q_i)^T\sum_j\phi(k_j)v_j^T}{\phi(q_i)^T\sum_j\phi(k_j)}
$$

令 $S=\sum_j\phi(k_j)v_j^T$ 和 $Z=\sum_j\phi(k_j)$，这两个量可以在遍历一次序列后算出，然后每个 $y_i$ 只需与这个全局状态交互即可得出。
