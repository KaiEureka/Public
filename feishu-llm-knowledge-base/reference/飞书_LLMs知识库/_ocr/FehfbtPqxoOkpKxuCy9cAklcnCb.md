$$
a_i=\mathrm{mean}(|X_{:,i}|)
$$

然后缩放因子定义为：

$$
s_i=\frac{a_i^\alpha}{\max(a^\alpha)}\quad\text{或}\quad s_i=a_i^\alpha
$$

并经过归一化或裁剪处理。更常用的实际操作形式为：

$$
s_i=\left(\frac{\max(|X_{:,i}|)}{\mathrm{clip\_max}}\right)^\alpha
$$
