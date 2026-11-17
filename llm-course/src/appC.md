## 附录 C　实验与代码索引 {#appC .chapter}

正文中所有标为"实验（实测）"的结果，都来自本附录列出的程序。程序都很小，只用 CPU，大多几秒到几分钟就能跑完。

### C.1 运行环境

**正文的实测环境**：4 核 Intel Xeon 云端虚拟机（2.1 GHz，L3 缓存 260 MB），15 GB 内存，没有 GPU；Python 3.13，numpy 2.5，PyTorch 2.14（CPU 版），Triton 3.8（只用解释器模式）。

**复跑**：整理本书时，在另一台 4 核 Intel Xeon 虚拟机（2.8 GHz，L3 缓存 33 MB，软件版本相同）上，把全部程序按 C.4 节的命令重新运行了一遍，C.3 节表中的"用时"就是这次复跑的实测值。

**复跑结果**：所有程序都正常运行。计时类的结果（第 4 章的 roofline 实验、第 19 章的通信耗时、第 33 章的速度与吞吐量，以及各程序打印的用时）随机器而变，但结论不变（例如第 33 章的 batch 实验，复跑时总吞吐量在 $B = 16$ 时最高，约为 $B = 1$ 时的 3.4 倍，之后不再提升，同样是很快就饱和）；其余数值结果都与正文一致，第 6 章重新训练出的模型权重与原来的逐字节相同。有三处例外，已经在正文中处理：① 第 11 章的学习率扫描中，学习率过高、训练接近不稳定的几格有小的出入（例如 SP、$H = 1024$、学习率 $2^{-3}$ 时，正文为 26.57，复跑为 22.36），各宽度的最优学习率和结论不变；② 第 15 章的程序原先按字符串集合的迭代顺序挑选替换词，而 Python 每次运行的字符串哈希都不同，所以检出率每次都会变化几个百分点。现已改为确定性的写法，第 15 章表格中的检出率换成了新的实测值；③ 第 32 章 $\lambda = 3\times10^{-3}$ 那一行原先训练了 4,000 步，与另一行的 3,000 步不一致，现统一为 3,000 步，并更新了数字。复跑的完整输出保存在 `code/rerun_logs/` 中。

### C.2 目录与数据

```
code/
  data/shakespeare.txt     Tiny Shakespeare，1,115,394 个字符（第 1–6、11、15、17、29、32–34 章）
  data/zh/                 唐诗两卷和《孟子》，来自 GitHub 上公开的 chinese-poetry 仓库（第 5 章）
  ch01/ … ch35/            第 N 章的程序放在 chNN/ 目录下
  ch06/gpt_T128.pt         第 6 章训练好的字符级 GPT，第 32–34 章的实验都基于它
  rerun_logs/              整理时复跑全部程序的输出，times.tsv 记录每个程序的用时
```

所有程序都从命令行参数读取数据路径。第 32–34 章的程序把 `../ch06` 作为第一个参数，从那里读取第 6 章的模型定义和权重。

### C.3 按章索引

| 章 | 程序 | 内容（正文位置） | 用时 |
|---|----------|----------------------------------|------|
| 1 | `bigram.py` | 均匀分布、unigram、bigram（计数与梯度下降两种写法）、采样，以及 n-gram 扫描（1.6、1.7 节） | 约 8 秒 |
| 1 | `examples.py` | 数据集的字符统计（1.6 节） | 不到 1 秒 |
| 2 | `micrograd.py` | 约 30 行的标量自动微分引擎（2.3 节） | 不到 1 秒 |
| 2 | `mlp_lm.py` | Bengio 式 MLP 语言模型，numpy 手写反向传播，含梯度检验；第三个参数是上下文长度 $K$（2.4–2.6 节） | $K = 4$、8、16 时分别约 2.4、3.3、4.5 分钟 |
| 3 | `nn.py` | 第 3 章各实验共用的可配置 MLP（numpy，手写反向传播） | — |
| 3 | `check.py` | `nn.py` 的梯度检验 | 约 3 秒 |
| 3 | `e1_init_stats.py` | 实验 1：20 层网络初始化时的信号（3.1 节） | 约 3 秒 |
| 3 | `e3_depth.py` | 实验 2，以及残差连接 + RMSNorm（3.1、3.2 节） | 约 5.3 分钟 |
| 3 | `e_rest.py` | 实验 3–6：输出层的初始尺度、优化器、学习率调度、batch size（3.1、3.3–3.5 节） | 约 5.7 分钟 |
| 4 | `roofline.py` | 实验 A：方阵乘法的算力（4.5 节） | 约 22 秒 |
| 4 | `roofline3.py` | 内存带宽，实验 B、C（4.5 节） | 约 28 秒 |
| 5 | `bpe.py`、`run.py` | 字节级 BPE（GPT-4 式预切分，增量更新）；合并过程、词表大小与压缩率、中文的切分（5.3、5.5、5.6 节） | 约 15 秒 |
| 6 | `gpt.py`、`eval_pos.py` | 从零写的字符级 GPT 及训练；按上下文长度分组的 loss、各个头的注意力距离（6.9、6.10 节） | 训练 约 4.0 分钟，分析 约 7 秒 |
| 7 | `modern_block.py` | RoPE 只依赖相对位置的数值检验；Llama 式 block（7.2、7.7 节） | 约 2 秒 |
| 8 | `balance.py` | 不用辅助损失的负载均衡（只模拟路由器）（8.4 节） | 约 7 秒 |
| 10 | `chinchilla.py` | 按拟合公式计算的计算最优分配、偏离最优点的代价、过度训练的账（10.4–10.6 节） | 不到 1 秒 |
| 11 | `mup_demo.py` | 常规参数化与 μP 的学习率扫描，60 次训练（11.3 节） | 约 5.6 分钟 |
| 12 | `muon_ns.py` | Newton–Schulz 正交化对奇异值的影响（12.4 节） | 约 3 秒 |
| 13 | `precision.py` | 五个数值演示：范围、精度、累加、权重更新被吞掉、loss scaling（13.2 节） | 约 2 秒 |
| 13 | `fp8_outliers.py` | 离群值与 FP8 的缩放粒度（13.4 节） | 约 2 秒 |
| 15 | `minhash.py` | MinHash + LSH 去重（15.5 节） | 约 6 秒 |
| 17 | `collapse.py` | 模型崩溃：替换与累积（17.3 节） | 不到 1 秒 |
| 19 | `ring_allreduce.py` | 用 4 个 CPU 进程手写环形 all-reduce（Gloo 后端）（19.4 节） | 约 9 秒 |
| 22 | `flash_cpu.py` | 分块注意力 + 在线 softmax，与标准注意力对比（22.2 节） | 不到 1 秒 |
| 22 | `triton_softmax.py` | 融合的 softmax 内核，用 Triton 解释器模式验证（22.4 节） | 约 2 秒 |
| 25 | `goodhart.py` | 奖励过度优化的模拟（25.7 节） | 不到 1 秒 |
| 26 | `dpo_toy.py` | 8 个候选回答上的 DPO 与 IPO（26.2 节） | 约 15 秒 |
| 27 | `grpo_toy.py` | 只决定"思考几步"的策略，用 GRPO 训练（27.4 节） | 不到 1 秒 |
| 29 | `distill_toy.py` | 软标签与硬标签；前向 KL 与反向 KL（29.1、29.2 节） | 约 1 秒 |
| 30 | `eval_noise.py` | 小基准上的统计噪声；pass@$k$ 的无偏估计（30.4、30.5 节） | 约 49 秒 |
| 32 | `sae.py`、`steer.py` | 在第 6 章的 GPT 上训练 SAE；用特征干预生成（32.4、32.6 节） | SAE 每个 $\lambda$ 约 约 1.6 分钟，干预 约 49 秒 |
| 33 | `kvcache.py` | KV cache 的正确性与加速；batch 大小对 decode 的影响（33.2、33.3 节） | 约 79 秒 |
| 34 | `quant.py` | 权重的 RTN 量化（34.1 节） | 约 17 秒 |
| 34 | `speculative.py` | 投机采样的精确性检验；用 bigram 当草稿（34.2 节） | 约 58 秒 |
| 35 | `mm_toys.py` | CLIP 式对比学习；二维扩散模型（35.2、35.5 节） | 约 25 秒 |

### C.4 运行命令

在 `code/` 目录下执行。`-I` 让 Python 不从脚本所在的目录导入模块；第 3、5 章的程序会自己把当前目录加入搜索路径，第 6 章的 `eval_pos.py` 从当前目录读取 `gpt.py` 和模型权重，所以要像下面这样先进入对应的目录再运行。

```bash
D=$(pwd)/data/shakespeare.txt
(cd ch01 && python3 -I bigram.py $D && python3 -I examples.py $D)
(cd ch02 && python3 -I micrograd.py && for K in 4 8 16; do python3 -I mlp_lm.py $D 60000 $K; done)
(cd ch03 && python3 -I check.py $D && python3 -I e1_init_stats.py $D \
         && python3 -I e3_depth.py $D 0.1 6000 && python3 -I e_rest.py $D)
(cd ch04 && python3 -I roofline.py && python3 -I roofline3.py)
(cd ch05 && python3 -I run.py $D ../data/zh)
(cd ch06 && python3 -I gpt.py $D 1000 128 128 4 4 32 && python3 -I eval_pos.py $D)
#   gpt.py 的参数：训练步数、上下文长度、宽度、层数、头数、batch；运行后会覆盖 gpt_T128.pt
(cd ch07 && python3 -I modern_block.py)
(cd ch08 && python3 -I balance.py)
(cd ch10 && python3 -I chinchilla.py)
(cd ch11 && python3 -I mup_demo.py $D)
(cd ch12 && python3 -I muon_ns.py)
(cd ch13 && python3 -I precision.py && python3 -I fp8_outliers.py)
(cd ch15 && python3 -I minhash.py $D)
(cd ch17 && python3 -I collapse.py $D)
(cd ch19 && python3 ring_allreduce.py)
(cd ch22 && python3 -I flash_cpu.py && TRITON_INTERPRET=1 python3 -I triton_softmax.py)
(cd ch25 && python3 -I goodhart.py)
(cd ch26 && python3 -I dpo_toy.py)
(cd ch27 && python3 -I grpo_toy.py)
(cd ch29 && python3 -I distill_toy.py $D)
(cd ch30 && python3 -I eval_noise.py)
(cd ch32 && python3 -I sae.py ../ch06 $D 3e-3 && python3 -I sae.py ../ch06 $D 3e-2 \
         && python3 -I steer.py ../ch06 $D)      # steer.py 使用最后保存的 sae.pt
(cd ch33 && python3 -I kvcache.py ../ch06 $D)
(cd ch34 && python3 -I quant.py ../ch06 $D && python3 -I speculative.py ../ch06 $D)
(cd ch35 && python3 -I mm_toys.py)
```

### C.5 没有做实验的章节

第 0、9、14、16、18、20、21、23、24、28、31、36–39 章没有实验程序。它们的内容要么依赖大规模的数据或集群（预训练数据、并行训练、大规模运维），要么属于设计、组织和判断，书中的数字来自公开资料或标为"估算""示意"的计算。
