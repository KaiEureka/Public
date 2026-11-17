$$
\text{Memory} = 2 \times B \times L \times H \times S \times d_k \times \text{bytes\_per\_element}
$$

其中：

- $B$：batch size（批次大小）
- $L$：模型的总层数
- $H$：每个注意力层的头数（对于 GQA/MQA，此处为键值头数 $H_{kv}$）
- $S$：序列总长度（prompt + 已生成的 token）
- $d_k$：每个头的维度（通常为 $d_{model}/H$）
- 系数 2：因为需要缓存 Key 和 Value 两个张量
- bytes_per_element：每个元素的字节数（FP16 为 2 字节）
