**公式**：对于一个训练时最大长度为 $L_{\text{train}}$ 的模型，在推理时面对长度为 $L_{\text{test}}$（$L_{\text{test}}>L_{\text{train}}$）的序列，将所有位置索引 $pos$ 乘以一个缩放因子 $\lambda=\frac{L_{\text{train}}}{L_{\text{test}}}$，得到新的位置索引 $\bar{pos}$。

$$
\bar{pos}=pos\times\frac{L_{\text{train}}}{L_{\text{test}}}
$$
