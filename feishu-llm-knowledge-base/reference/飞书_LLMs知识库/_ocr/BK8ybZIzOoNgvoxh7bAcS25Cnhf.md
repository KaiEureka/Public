有些实现会再经过一个输出投影：$y = \mathrm{SwiGLU}(x)W_2 + b_2$。在 Transformer FFN 中，标准 SwiGLU 使用三个线性层：`gate_proj`（接 SiLU）、`up_proj`，两者乘积后再经过 `down_proj`。
