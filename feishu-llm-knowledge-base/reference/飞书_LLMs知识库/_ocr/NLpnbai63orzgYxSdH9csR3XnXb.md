**计算公式**：

对于每一层 Transformer，前缀参数的数量为 $L\times d$，用于 Key；再乘 $L\times d$，用于 Value。因此，对于一层，总参数量为 $2\times L\times d$。对于整个模型，如果有 $N$ 层，总参数量为：

$$
\mathrm{Total\ Parameters}=N\times\left(L\times d_{\mathrm{key}}+L\times d_{\mathrm{value}}\right)
$$

在标准 Transformer 中，$d_{\mathrm{key}}=d_{\mathrm{value}}=d$，所以公式简化为 $N\times2\times L\times d$。

**示例**：

假设一个 GPT-2 模型有 $N=12$ 层，隐藏维度 $d=768$，前缀长度 $L=10$。

总前缀参数量 $=12\times2\times10\times768=184,320$。

这个数字与 GPT-2 的总参数量（约 1.24 亿）相比，仅占 0.15%。
