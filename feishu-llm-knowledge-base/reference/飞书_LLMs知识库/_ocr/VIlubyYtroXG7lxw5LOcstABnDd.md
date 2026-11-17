在每个子层（自注意力层、前馈网络层）周围，都有一个残差连接。具体操作是：

- 子层的输入记为 $x$。
- 子层的运算（如多头注意力或 FFN）得到输出 $\mathrm{Sublayer}(x)$。
- 将两者相加：$x + \mathrm{Sublayer}(x)$，然后再进行层归一化（LayerNorm）。

即：$\mathrm{Output} = \mathrm{LayerNorm}(x + \mathrm{Dropout}(\mathrm{Sublayer}(x)))$（在原始论文中，是先加后归一化；某些变体中顺序可能不同，但主流实现先加后归一化）。
