$$
s_i=\frac{\max(|X_{:,i}|)}{\mathrm{mean}(\max(|X_{:,i}|))}\quad\text{或更平滑的变体}
$$

或者基于分位数的鲁棒统计量。这种方案完全避免了任何优化循环，校准只需一次前向统计。

- AutoAWQ 库中默认使用基于激活最大绝对值的平滑版本：$s_i=(\max(|X_{:,i}|)/\mathrm{smooth\_factor})^\alpha$，并经过简单 clip。
