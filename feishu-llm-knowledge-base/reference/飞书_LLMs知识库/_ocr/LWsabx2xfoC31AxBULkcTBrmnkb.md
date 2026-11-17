$$
d_{ff} = \frac{8}{3} \times d_{model} = \frac{8}{3} \times 4096 = \frac{32768}{3} \approx 10922.666\ldots
$$

在实际实现中，通常会对该值进行取整。LLaMA-7B（$d_{model} = 4096$）使用的中间维度为 **11008**，这个值正是最接近 10922.67 且满足硬件对齐（如 256 的倍数）的整数。取整方式为：

$$
d_{ff} = \mathrm{round}\left(\frac{8}{3} \cdot d_{model}\right)
$$
