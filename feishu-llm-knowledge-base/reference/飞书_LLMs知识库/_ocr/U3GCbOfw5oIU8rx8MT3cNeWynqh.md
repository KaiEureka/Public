$$
\mathrm{Cache}_{\mathrm{MHA}} = 2 \times L \times H \times S \times d_k
$$

其中 $L$ 为层数，$H$ 为头数，$S$ 为序列长度，$d_k$ 为每个头的维度。

对于 MQA，因为所有头共享 $K$ 和 $V$，等效头数 $H_{kv} = 1$，缓存大小变为：

$$
\mathrm{Cache}_{\mathrm{MQA}} = 2 \times L \times 1 \times S \times d_k
$$
