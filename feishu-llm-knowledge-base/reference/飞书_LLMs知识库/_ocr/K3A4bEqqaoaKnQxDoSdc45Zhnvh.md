1. **离群值检测**：对 FP16 输入激活 $X\in\mathbb{R}^{s\times d_{in}}$（s 为 token 数），按特征维度（列）计算绝对值，若某列存在值超过阈值（通常为 6.0）则认为该列为离群值特征。记录下离群值列的索引集合 $O$，以及非离群值列集合 $R$。
2. **矩阵拆分**：
   - 将权重矩阵 $W\in\mathbb{R}^{d_{in}\times d_{out}}$ 按行拆分：$W_O$（离群值对应的行）和 $W_R$（正常行）。
   - 将输入 $X$ 按列拆分：$X_O$ 和 $X_R$。
3. **混合精度计算**：
   - **正常部分**：对 $X_R$ 和 $W_R$ 进行标准 INT8 量化（per-token 对 X，per-channel 对 W），使用 INT8 Tensor Core 进行矩阵乘，结果反量化为 FP16。
   - **离群值部分**：对 $X_O$ 和 $W_O$ 保留 FP16，直接调用 FP16 GEMM。
   - **最终输出**：`Y = INT8_MatMul(X_R, W_R) + FP16_MatMul(X_O, W_O)`。
