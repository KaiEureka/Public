$$
X_q=\mathrm{clamp}\left(\mathrm{round}\left(\frac{X}{s}\right)+z,0,2^b-1\right)
$$

反量化：

$$
X\approx s\cdot(X_q-z)
$$

其中 $s=\frac{\max(X)-\min(X)}{2^b-1}$，$z=-\frac{\min(X)}{s}$（四舍五入）。
