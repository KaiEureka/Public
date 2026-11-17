Performer 的核心是 **FAVOR+ 算法**（Fast Attention Via positive Orthogonal Random features）。它目标是找到一种特征映射 $\phi$，使得 $\phi(q)^T\phi(k)$ 能够无偏地近似 $\exp(q^Tk/\sqrt{d})$。
