$$
P(x_1, x_2, \ldots, x_T) = \prod_{t=1}^{T} P(x_t \mid x_{<t})
$$

这个分解要求每个 $x_t$ 的预测**仅依赖于它之前生成的 token** $(x_1, \ldots, x_{t-1})$，而不能偷看未来的真实答案。
