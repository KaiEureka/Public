**核心创新**：FlashAttention 的核心创新在于**利用分块（tiling）和重计算（recomputation），将注意力计算从 IO-bound 转变为 compute-bound**，同时将显存复杂度从 $O(n^2)$ 降低到 $O(n)$，并且实现了精确的注意力（非近似）。它通过以下方式实现：
