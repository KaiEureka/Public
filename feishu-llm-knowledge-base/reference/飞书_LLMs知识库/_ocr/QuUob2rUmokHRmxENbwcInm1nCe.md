通过**随机正交特征**显式地逼近 softmax 核。它使用随机投影来近似 $\exp(q^Tk)\approx\phi(q)^T\phi(k)$。FAVOR+ 是 Performer 提出的正交随机特征，它具有无偏估计且方差更小的优点，能够以极低维的投影达到接近 softmax 的效果。形式为：

$$
\phi(x)=\frac{1}{\sqrt{m}}e^{-\frac{\|x\|^2}{2}}\left[\exp(w_1^Tx),\ldots,\exp(w_m^Tx)\right]
$$
