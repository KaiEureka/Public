4. **代入 Bradley-Terry 偏好模型**：人类偏好通常用 Bradley-Terry 模型来描述，即认为人类偏好 $y_w \succ y_l$ 的概率取决于两者之间隐式奖励的差值：

$$
P(y_w \succ y_l|x) = \sigma \left( r(x, y_w) - r(x, y_l) \right)
$$
