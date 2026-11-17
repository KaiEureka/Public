**13. 说明 “memory fragmentation” 问题，以及 PyTorch 缓存分配器如何缓解**

**显存碎片化** 指显存中存在大量不连续的空闲小块，即使总空闲量足够，也无法分配出一个大的连续显存块。大模型训练中，张量尺寸差异大，频繁分配和释放容易导致碎片。

**PyTorch 缓存分配器** 通过以下机制缓解碎片：

1. **缓存池**：释放的张量显存不会立即归还给 CUDA，而是由分配器保留在内存池中，划分为不同大小的 block。后续申请显存时，优先从池中匹配。
2. **分割与合并**：当找不到完全匹配的 block 时，大 block 可以分割；当相邻 block 都空闲时，可以合并为大 block。分配器通过隐式链表管理这些 block。
3. **固定分配策略**：PyTorch 使用 `round_robin` 分配器，尽量减少外部碎片。但长期训练仍可能出现碎片，此时可通过 `torch.cuda.empty_cache()` 强制将所有缓存归还 CUDA，促使驱动层整理显存。
4. **张量生命周期管理**：及时释放不再需要的张量（例如用 `del tensor` 并调用 `empty_cache`）可以减少碎片。

**碎片对训练的影响**：当出现 OOM 但实际空闲显存够用时，往往是碎片导致。解决方法：减小 micro batch size、启用梯度检查点（降低激活内存）、使用更规整的张量形状、定期调用 `empty_cache()`。

**监控碎片**：`torch.cuda.memory_stats()` 返回的 `"active_bytes"` 和 `"reserved_bytes"` 可帮助判断。如果 reserved 远大于 active，且分配大张量失败，很可能是碎片。

---

**14. 通信缓冲区（如 All-Reduce 缓冲）对峰值显存的影响及估算**

分布式训练中，集合通信操作（如 All-Reduce、All-Gather、Reduce-Scatter）需要临时缓冲区来存储发送/接收的数据。这部分显存占用称为**通信缓冲区**。

**影响来源**：

- **数据并行梯度同步**：PyTorch DDP 将梯度分成多个桶 (bucket)，每次对一个桶进行 All-Reduce。桶的大小可通过 `bucket_cap_mb` 设置（默认 25MB）。因此，单个梯度桶的缓冲区通常为几十 MB。所有桶的通信串行进行，峰值缓冲区约为**最大桶大小**，而非全部梯度总和。
- **ZeRO-3 参数收集**：前向/反向时需要 All-Gather 完整参数，每个参数的 All-Gather 也需要缓冲区。通常通过设置 `allgather_bucket_size` 控制。若桶大小设为 500MB，则参数收集峰值缓冲约 500MB。
- **张量并行**：每个 Transformer 层的 All-Reduce 或 Reduce-Scatter 也会产生临时缓冲区。这部分通常与计算重叠，大小类似层内激活。
