逐位置的前馈神经网络（Position-wise Feed-Forward Network, FFN）是 Transformer 每个层中的关键组成部分，位于注意力子层之后。它由两个线性变换和一个激活函数组成（如 $FFN(x) = \mathrm{ReLU}(xW_1 + b_1)W_2 + b_2$）。其作用如下：
