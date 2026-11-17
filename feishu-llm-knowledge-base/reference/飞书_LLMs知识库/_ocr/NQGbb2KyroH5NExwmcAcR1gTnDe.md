以 LLaMA-7B 为例，参数量 $\Psi = 7 \times 10^9$。假设：

- 混合精度训练：参数 FP16，梯度 FP16，优化器 FP32 (Adam)。
- 无任何并行、无检查点、无卸载、无 FlashAttention。
- 序列长度 $S = 2048$，batch size $B = 1$，隐藏维度 $H = 4096$，层数 $L = 32$，头数 $h = 32$。
