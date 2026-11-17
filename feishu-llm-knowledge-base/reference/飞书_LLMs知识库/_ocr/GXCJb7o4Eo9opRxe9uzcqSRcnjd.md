例如，假设我们有三个维度的偏好数据：有用性 $D_{help}$、诚实性 $D_{honest}$ 和安全性 $D_{safe}$。那么，最终的训练损失可以定义为：

$$
\mathcal{L}_{\text{total}} = \lambda_{help} \cdot \mathcal{L}_{\text{DPO}}(D_{help}) + \lambda_{honest} \cdot \mathcal{L}_{\text{DPO}}(D_{honest}) + \lambda_{safe} \cdot \mathcal{L}_{\text{DPO}}(D_{safe})
$$
