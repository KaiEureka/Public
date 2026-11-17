自回归解码的每一轮迭代中，最耗时的操作往往不是矩阵乘法本身，而是从 HBM 读取巨大的 KV Cache。MHA 需要读取 $2\times h\times d_k$ 维的 K 和 V 向量（每 token），MQA 则只需读取 $2\times1\times d_k$。在给定的硬件内存带宽 $B_{\text{mem}}$ 下，理论最大 token 生成速率由 **Roofline 模型** 的带宽受限区域决定：

$$
\text{Max tokens/s}\propto\frac{B_{\text{mem}}}{\text{Bytes per token per iteration}}
$$
