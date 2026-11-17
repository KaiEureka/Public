2. **分块计算（Tiling）**：将 Q, K, V 切分成小块，逐块从 HBM 加载到 SRAM，在片上完成该块的部分注意力计算，并不断用 online softmax 更新最终结果，无需显式构造完整的 $S=QK^T$ 矩阵。
