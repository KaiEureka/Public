**可学习位置嵌入**（Learned Positional Embedding）是将每个位置视为一个独立的"词"，在词嵌入矩阵旁边再维护一个位置嵌入矩阵 $W_{pos} \in \mathbb{R}^{L_{\max} \times d_{\mathrm{model}}}$，其中每一行对应一个绝对位置的嵌入向量。这些向量是随机初始化的，然后在训练过程中通过反向传播与模型其他参数一同更新。
