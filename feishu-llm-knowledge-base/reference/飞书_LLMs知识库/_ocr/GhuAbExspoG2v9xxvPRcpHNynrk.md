$$
X_q=\mathrm{clamp}\left(\mathrm{round}\left(\frac{X}{s}\right),-2^{b-1},2^{b-1}-1\right)
$$

反量化：

$$
X\approx s\cdot X_q
$$

其中缩放因子 $s=\frac{\max(|X|)}{2^{b-1}-1}$，零点固定为 0。
