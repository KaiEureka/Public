压缩率 = $\frac{2\times H\times d_k}{d_{latent}}$（若 K、V 共享同一个潜在向量，缓存元素数为 $d_{latent}$）。

- DeepSeek-V2 中，$H=128$，$d_k=128$，总 KV 维度为 16384。$d_{latent}$ 被设为 512。若 K、V 共享潜在向量，压缩比高达 $2\times16384/512\approx64$ 倍。
- 若 K、V 各有独立的潜在向量（部分设计），压缩比约为 32 倍。
