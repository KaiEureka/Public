$$
\mathcal{L}_{Critic}^{Huber} = \frac{1}{N} \sum_t \begin{cases} 0.5 \cdot (V(s_t) - V_{target})^2, & \text{if } |V(s_t) - V_{target}| \le \delta \\ \delta \cdot (|V(s_t) - V_{target}| - 0.5 \cdot \delta), & \text{otherwise} \end{cases}
$$
