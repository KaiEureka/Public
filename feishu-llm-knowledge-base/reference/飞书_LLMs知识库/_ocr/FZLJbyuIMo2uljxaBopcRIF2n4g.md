已知：查询头数 $h=32$，GQA 的 KV 头数 $g=8$。这意味着有 8 个分组，每组包含 $32/8=4$ 个查询头，每个组共享一对 $K,V$。假设单头维度 $d_k$ 在两种结构中相同，序列长度为 $n$。

- MHA 的 KV Cache 大小（每层）：$\mathrm{MHA}_{kv}=2\times h\times d_k\times n=2\times32\times d_k\times n=64d_kn$
- GQA 的 KV Cache 大小（每层）：$\mathrm{GQA}_{kv}=2\times g\times d_k\times n=2\times8\times d_k\times n=16d_kn$
