$$
\text{节省比例}=\frac{\text{MHA KV}-\text{MQA KV}}{\text{MHA KV}}=\frac{2hd_kn-2\cdot1\cdot d_kn}{2hd_kn}=\frac{h-1}{h}=1-\frac{1}{h}
$$

若用 $h$ 表示查询头数，公式为 $\left(1-\frac{1}{h}\right)\times100\%$。例如，当 $h=32$ 时，节省了约 96.875% 的 KV 缓存；当 $h=8$ 时，节省 87.5%。这极大地缓解了显存压力，使长序列和大 batch 推理成为可能。节省比例公式清晰地表明，头数越多，MQA 的相对收益越大。
