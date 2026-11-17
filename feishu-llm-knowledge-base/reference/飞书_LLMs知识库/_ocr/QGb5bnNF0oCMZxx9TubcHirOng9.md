- **MHA**：
  - $W_Q$：`[d_model, H * d_k]`（或分为 H 个 `[d_model, d_k]`）
  - $W_K$：`[d_model, H * d_k]`
  - $W_V$：`[d_model, H * d_k]`

  每个投影矩阵的输出维度为 $H \times d_k = d_{model}$，然后再拆分为 H 个头。
- **MQA**：
  - $W_Q$：仍为 `[d_model, H * d_k]`（独立头）
  - $W_K$：`[d_model, d_k]` —— 因为所有头共享，输出维度仅为一个头的维度。
  - $W_V$：同理。
