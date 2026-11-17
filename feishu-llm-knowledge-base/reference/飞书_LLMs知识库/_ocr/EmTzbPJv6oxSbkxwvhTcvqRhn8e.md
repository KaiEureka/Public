**如何调整RoPE基频**：在RoPE公式 $\theta_i=\frac{1}{\text{base}^{2i/d}}$ 中，将基频 `base`（通常为10000）替换为一个更大的值 `base_new`。

$$
\text{base\_new}=\text{base}\times\left(\frac{L_{\text{test}}}{L_{\text{train}}}\right)^{d/(d-2)}
$$
