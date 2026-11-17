## 附录 A　术语表 {#appA .chapter}

下表按"首次给出定义的章"分组排列，既可以用来查词，也可以当作全书的提纲来复习。"章"一栏给的是正式定义这个术语的章；有些术语在第 0 章的全景介绍里提前出现过，但定义在后面。

### A.1 地基（第 0–4 章）

| 术语 | 英文 | 含义 | 章 |
|------------|-------------|--------------------------|---|
| FLOP | floating-point operation | 一次浮点运算；训练计算量约为 $6ND$ FLOP | 0 |
| MFU | model FLOPs utilization | 模型实际用到的有效算力 ÷ 硬件峰值算力；40% 左右算优秀 | 0 |
| 消融实验 | ablation | 每次只改一个因素，看它对结果的影响 | 0 |
| 激活值 | activations | 前向计算的中间结果，反向传播要用，所以要保存 | 0 |
| token | token | 模型处理文本的基本单位，由分词器切出 | 1 |
| 词表 | vocabulary | 所有 token 的集合，大小记为 $V$ | 1 |
| 语言模型 | language model | 给定前文，输出下一个 token 的概率分布 | 1 |
| 自回归 | autoregressive | 一次生成一个 token，生成的结果再作为后面的条件 | 1 |
| 样本空间 | sample space | 语言模型的样本空间是所有以 ⟨eos⟩ 结尾的有限 token 序列，即完整的文档 | 1 |
| 柱集 | cylinder set | "文档以某个前缀开头"这个事件对应的文档集合 | 1 |
| logits | logits | softmax 之前、尚未归一化的分数 | 1 |
| softmax | softmax | $e^{z_i}/\sum_j e^{z_j}$，把 logits 变成概率分布 | 1 |
| 交叉熵 | cross-entropy | $-\sum p\log q$；训练 loss 是正确 token 负对数概率的平均 | 1 |
| KL 散度 | KL divergence | $\sum p\log(p/q)$；交叉熵 = 数据的熵 + KL 散度 | 1 |
| 不可约损失 | irreducible loss | 数据本身的熵 $H(p)$，任何模型的 loss 都不会低于它 | 1 |
| 最大似然估计 | maximum likelihood estimation, MLE | 让训练数据的概率最大，等价于最小化交叉熵 | 1 |
| 困惑度 | perplexity | $e^{\text{loss}}$，可理解为模型平均在多少个选项之间犹豫 | 1 |
| 每字节比特数 | bits-per-byte, BPB | 与分词器无关的 loss 度量，可以比较不同分词器的模型 | 1 |
| 基座模型 | base model | 只做过预训练、没有做后训练的模型 | 1 |
| teacher forcing | teacher forcing | 训练时每个位置都以真实的前文为条件 | 1 |
| 温度 | temperature | 采样前把 logits 除以 $\tau$；$\tau < 1$ 更确定，$\tau > 1$ 更随机 | 1 |
| n-gram | n-gram | 只看前 $n-1$ 个 token、靠计数估计概率的模型 | 1 |
| 平滑 | smoothing | 给没见过的组合分一点概率，比如每个计数都加 1 | 1 |
| embedding | embedding | 把 token 编号映射成向量的查找表 | 1 |
| 多层感知机 | multilayer perceptron, MLP | 线性层与非线性激活函数交替堆叠的网络 | 2 |
| 反向传播 | backpropagation | 沿计算图从 loss 往回，用链式法则求出所有参数的梯度 | 2 |
| 计算图 | computational graph | 记录每个运算及其输入的有向无环图 | 2 |
| 小批量随机梯度下降 | SGD | 每一步用一小批数据估计梯度，更新参数 | 2 |
| 过拟合 | overfitting | 训练集 loss 还在下降，验证集 loss 却开始上升 | 2 |
| 增益 | gain | 初始化时补偿激活函数缩小方差的系数：tanh 为 5/3，ReLU 为 $\sqrt2$ | 3 |
| 梯度消失 / 爆炸 | vanishing / exploding gradients | 梯度逐层连乘之后变得极小或极大 | 3 |
| 残差连接 | residual connection | $h + f(h)$，给信号和梯度一条直通的路径 | 3 |
| 残差流 | residual stream | 各层通过残差连接不断读写的那条主干向量 | 3 |
| LayerNorm / RMSNorm | — | 把向量归一化到固定尺度；RMSNorm 只除以均方根，不减均值 | 3 |
| Pre-norm / Post-norm | — | 归一化放在残差分支内部（Pre）或残差相加之后（Post）；Pre-norm 更稳定 | 3 |
| Adam / AdamW | — | 用梯度的一阶、二阶指数移动平均自适应调整步长；AdamW 把权重衰减与梯度更新分开 | 3 |
| warmup | warmup | 训练开始时学习率从很小逐步升到峰值 | 3 |
| 余弦衰减 / WSD | cosine decay / warmup–stable–decay | 两种学习率调度：余弦式逐渐下降；或长时间保持恒定，最后快速衰减 | 3 |
| 梯度累积 | gradient accumulation | 把几个 micro-batch 的梯度加起来再更新，模拟更大的 batch | 3 |
| 梯度裁剪 | gradient clipping | 梯度范数超过阈值（常用 1.0）时按比例缩小 | 3 |
| loss 尖峰 | loss spike | 训练中 loss 突然飙升 | 3 |
| SM / Tensor Core | streaming multiprocessor | GPU 的计算单元；Tensor Core 是其中专门做矩阵乘法的部件 | 4 |
| 内核 | kernel | 在 GPU 上运行的一个函数 | 4 |
| HBM / SRAM | high bandwidth memory | 显存（容量大、较慢）与片上存储（容量小、极快） | 4 |
| 算术强度 | arithmetic intensity | 每读写一个字节做多少次运算 | 4 |
| 平衡点 | ridge point | 峰值算力 ÷ 显存带宽；算术强度低于它就受限于带宽 | 4 |
| roofline 模型 | roofline model | 用算术强度判断一个运算受限于算力还是带宽 | 4 |
| 内存受限 / 计算受限 | memory-bound / compute-bound | 瓶颈在读写数据，还是在计算 | 4 |
| 算子融合 | kernel fusion | 把几个运算合并成一个内核，中间结果不写回显存 | 4 |

### A.2 架构（第 5–9 章）

| 术语 | 英文 | 含义 | 章 |
|------------|-------------|--------------------------|---|
| 分词器 | tokenizer | 把文本切成 token 序列、再把 token 还原成文本的程序 | 5 |
| BPE | byte pair encoding | 从字节出发，反复合并最常见的相邻对，得到子词词表 | 5 |
| 预切分 | pre-tokenization | BPE 之前先用正则表达式把文本切开，合并不跨越切分边界 | 5 |
| UTF-8 | UTF-8 | 把 Unicode 码点编码成 1 到 4 个字节的方案 | 5 |
| tied embeddings | tied embeddings | 输入 embedding 与输出层共用同一个矩阵 | 5 |
| 特殊 token | special tokens | 表示文档结束、对话角色等的保留 token | 5 |
| 注意力 | attention | 每个位置按内容相关度，对前文的 value 做加权平均 | 6 |
| query / key / value | — | 用于"提问"、"被匹配"和"被取走的内容"的三组投影向量 | 6 |
| 因果掩码 | causal mask | 禁止每个位置看到它后面的位置 | 6 |
| 多头注意力 | multi-head attention, MHA | 并行做多组注意力，每组关注不同的关系 | 6 |
| 前馈层 | feed-forward network, FFN | 每个位置独立做的 MLP | 6 |
| KV cache | KV cache | 生成时缓存已算过的 key 和 value，避免重复计算 | 6 |
| decoder-only | decoder-only | 只有带因果掩码的解码器，今天的主流架构 | 6 |
| RoPE | rotary position embedding | 按位置旋转 $q$ 和 $k$，让注意力分数只依赖相对位置 | 7 |
| SwiGLU | SwiGLU | 带门控的 FFN：$(\operatorname{SiLU}(xW_{\text{gate}})\odot xW_{\text{up}})W_{\text{down}}$ | 7 |
| MQA / GQA | multi-query / grouped-query attention | 多个 query 头共用一组（MQA）或几组（GQA）key/value，减小 KV cache | 7 |
| MLA | multi-head latent attention | 把 K 和 V 压缩成一个低维潜在向量来缓存 | 7 |
| MoE | mixture of experts | 每个 token 只激活少数几个"专家"FFN | 8 |
| 总参数 / 激活参数 | total / active parameters | 模型全部参数，与每个 token 实际用到的参数 | 8 |
| 路由器 | router | 为每个 token 选专家、给出权重的小网络 | 8 |
| 路由坍缩 | routing collapse | token 都挤到少数几个专家上 | 8 |
| 辅助损失（负载均衡） | auxiliary load-balancing loss | $\alpha E\sum_i f_iP_i$，鼓励各专家收到的 token 数均匀 | 8 |
| 不用辅助损失的负载均衡 | auxiliary-loss-free balancing | DeepSeek 的做法：只在选专家时加偏置，按负载动态调整 | 8 |
| 共享专家 | shared expert | 每个 token 都会经过的专家 | 8 |
| 专家并行 | expert parallelism, EP | 不同的专家放在不同的卡上，用 all-to-all 收发 token | 8 |
| 滑动窗口注意力 | sliding window attention | 每个位置只看最近 $W$ 个位置 | 9 |
| 注意力汇聚点 | attention sink | 模型把多余的注意力权重放在开头几个 token 上的现象 | 9 |
| 线性注意力 / 状态空间模型 | linear attention / SSM | 用固定大小的状态代替 KV cache，代价是难以精确回忆 | 9 |
| 位置插值 / YaRN | position interpolation / YaRN | 扩展 RoPE 上下文长度的方法；YaRN 按频率区别对待 | 9 |
| 打包 | packing | 把多篇短文档拼成一条训练序列 | 9 |
| 大海捞针 | needle in a haystack | 在长文中藏一句话，测模型能否找出来 | 9 |

### A.3 规模化的科学（第 10–13 章）

| 术语 | 英文 | 含义 | 章 |
|------------|-------------|--------------------------|---|
| scaling law | scaling law | loss 随参数量、数据量、计算量变化的幂律 | 10 |
| 等计算量曲线 | iso-FLOP curve | 固定计算量、改变模型大小，找 loss 最低点 | 10 |
| Chinchilla 比例 | Chinchilla-optimal | 计算最优时约 20 个 token 对应 1 个参数 | 10 |
| 过度训练 | overtraining | 为了降低推理成本，用远多于计算最优的 token 训练小模型 | 10 |
| 规模阶梯 | scaling ladder | 一组从小到大的模型，用来拟合规律、外推到大模型 | 10 |
| 涌现能力 | emergent abilities | 某些指标在规模达到一定程度后突然变好的现象 | 10 |
| 标准参数化 | standard parametrization, SP | 常规的初始化和学习率设定；最优学习率随宽度变化 | 11 |
| μP | maximal update parametrization | 按宽度调整初始化、学习率和输出乘子，让最优超参数不随宽度变化 | 11 |
| 梯度噪声尺度 / 临界 batch | gradient noise scale / critical batch size | 增大 batch 不再划算的那个规模 | 11 |
| QK-norm | QK-norm | 对 $q$、$k$ 做归一化，限制注意力 logits 的大小 | 12 |
| z-loss | z-loss | $10^{-4}(\log Z)^2$，防止输出 logits 漂移 | 12 |
| logit 软上限 | logit soft-capping | 用 $c\tanh(z/c)$ 把 logits 平滑地限制在 $\pm c$ 以内 | 12 |
| Muon | Muon | 把矩阵参数的更新正交化（所有奇异值变成 1）的优化器 | 12 |
| FP32 / FP16 / BF16 | — | 32 位和两种 16 位浮点格式；BF16 范围与 FP32 相同，精度较低 | 13 |
| 下溢 | underflow | 数值太小，变成 0 或失去精度 | 13 |
| loss scaling | loss scaling | FP16 训练时把 loss 乘上一个大数，防止梯度下溢 | 13 |
| 混合精度 | mixed precision | 矩阵乘法用低精度，主权重和累加用 FP32 | 13 |
| FP8（E4M3 / E5M2） | — | 两种 8 位浮点格式；E4M3 最大 448，E5M2 范围更大 | 13 |
| 细粒度缩放 | fine-grained scaling | 按小块（如 $1\times128$）各用一个缩放因子 | 13 |
| 随机舍入 | stochastic rounding | 按距离成比例地随机向上或向下舍入，期望无偏 | 13 |

### A.4 数据（第 14–17 章）

| 术语 | 英文 | 含义 | 章 |
|------------|-------------|--------------------------|---|
| Common Crawl | Common Crawl | 公开的网页抓取存档，按快照发布 | 14 |
| WARC / WET | — | Common Crawl 的原始网页格式 / 已抽取的纯文本格式 | 14 |
| robots.txt | robots.txt | 网站声明允许哪些爬虫抓取哪些路径的文件 | 14 |
| fastText | fastText | 很快的线性文本分类器，常用于语言识别和质量打分 | 14 |
| 正文提取 | text extraction | 从 HTML 中去掉导航、广告等模板内容，保留正文 | 15 |
| MinHash | MinHash | 用"最小哈希值相等的概率 = Jaccard 相似度"来估计文档的相似度 | 15 |
| LSH | locality-sensitive hashing | 把签名分成 $b$ 段、每段 $r$ 行，只比较至少一段相同的文档对 | 15 |
| shingle | shingle | 连续 $k$ 个词组成的片段，用来把文档变成集合 | 15 |
| 质量分类器 | quality classifier | 给文档打分、保留高分文档的模型（如 FineWeb-Edu、DCLM） | 16 |
| 退火 | annealing | 训练末尾学习率衰减时，提高高质量数据的比例 | 16 |
| 中期训练 | mid-training | 预训练和后训练之间，用特定数据（长文、推理等）继续训练 | 16 |
| 合成数据 | synthetic data | 由模型生成或改写的训练数据 | 17 |
| 模型崩溃 | model collapse | 只用上一代模型生成的数据训练，分布的尾部逐代消失 | 17 |
| 评测污染 / 去污染 | contamination / decontamination | 测试题出现在训练数据里 / 把它们找出来去掉 | 17 |
| 金丝雀字符串 | canary string | 放在评测集里的唯一标记，用来检测是否被训练过 | 17 |

### A.5 训练基础设施（第 18–23 章）

| 术语 | 英文 | 含义 | 章 |
|------------|-------------|--------------------------|---|
| NVLink / NVSwitch | — | 机器内部 GPU 之间的高速互联 / 让它们全互联的交换芯片 | 18 |
| InfiniBand / RoCE | — | 跨机器的高速网络；都支持 RDMA | 18 |
| RDMA | remote direct memory access | 网卡直接读写另一台机器的内存，不经过 CPU | 18 |
| 胖树 | fat tree | 由叶交换机和脊交换机组成、可以做到满对分带宽的网络拓扑 | 18 |
| 轨道优化 | rail-optimized | 各台机器上编号相同的 GPU 接到同一组交换机 | 18 |
| 收敛比 | oversubscription | 上行带宽小于下行带宽的比例，如 1:7 | 18 |
| PUE | power usage effectiveness | 设施总功耗 ÷ IT 设备功耗 | 18 |
| 集合通信 | collective communication | 一组进程一起参与的通信：broadcast、reduce、all-reduce、reduce-scatter、all-gather、all-to-all | 19 |
| rank / world size | — | 进程的编号 / 进程总数 | 19 |
| 环形 all-reduce | ring all-reduce | 先 reduce-scatter 再 all-gather，每卡发送 $2(n-1)S/n$ | 19 |
| NCCL | NVIDIA Collective Communications Library | NVIDIA 的集合通信库 | 19 |
| 数据并行 | data parallelism, DP | 每张卡一份完整模型、处理不同数据，梯度做 all-reduce | 20 |
| ZeRO-1/2/3 | zero redundancy optimizer | 依次把优化器状态、梯度、参数切分到各卡 | 20 |
| FSDP / HSDP | fully / hybrid sharded data parallel | PyTorch 的 ZeRO-3 实现 / 机内切分、机间复制的混合版本 | 20 |
| 重新计算（激活重计算） | activation recomputation | 只保存每层的输入，反向时重新算一遍前向 | 20 |
| HFU | hardware FLOPs utilization | 把重新计算也算进去的算力利用率 | 20 |
| 张量并行 | tensor parallelism, TP | 把一层的矩阵切到几张卡上 | 21 |
| 序列并行 / 上下文并行 | sequence / context parallelism | 沿序列方向切分激活值；上下文并行连注意力也切分 | 21 |
| 流水线并行 | pipeline parallelism, PP | 把不同的层放到不同的卡上，micro-batch 依次流过 | 21 |
| 气泡 | bubble | 流水线中卡在等待的空闲时间；GPipe/1F1B 为 $(p-1)/(m+p-1)$ | 21 |
| 1F1B / 交错调度 / DualPipe | — | 流水线调度：一前一后交替 / 每卡负责多段 / 双向流水线并重叠通信 | 21 |
| 在线 softmax | online softmax | 分块计算 softmax，边算边修正最大值和分母 | 22 |
| FlashAttention | FlashAttention | 分块在 SRAM 中计算注意力，不写出 $T\times T$ 矩阵 | 22 |
| Triton | Triton | 用 Python 写 GPU 内核的语言和编译器 | 22 |
| 有效训练时间占比 | goodput | 真正推进训练的时间占总时间的比例 | 23 |
| 检查点 | checkpoint | 保存下来、可以从中恢复训练的完整状态 | 23 |
| 静默数据损坏 | silent data corruption, SDC | 硬件算错了却不报错 | 23 |
| 处理手册 | runbook | 写好的故障处理步骤 | 23 |

### A.6 后训练（第 24–29 章）

| 术语 | 英文 | 含义 | 章 |
|------------|-------------|--------------------------|---|
| SFT | supervised fine-tuning | 在"指令–回答"数据上做监督训练，只对回答部分计算 loss | 24 |
| 对话模板 | chat template | 用特殊 token 标出 system、user、assistant 各个角色 | 24 |
| 拒绝采样 | rejection sampling | 生成多个回答，只保留通过检查的 | 24 |
| 表层对齐假说 | superficial alignment hypothesis | 知识来自预训练，SFT 主要教格式和风格 | 24 |
| LoRA / QLoRA | low-rank adaptation | 冻结原权重，只训练低秩增量 $BA$；QLoRA 再把原权重量化到 4 位 | 24 |
| RLHF | reinforcement learning from human feedback | 用人类偏好训练奖励模型，再用强化学习优化策略 | 25 |
| 奖励模型 | reward model | 给回答打分的模型，用 Bradley-Terry 损失在偏好对上训练 | 25 |
| 策略 / 参考模型 | policy / reference model | 正在训练的模型 / 用来计算 KL 惩罚的冻结副本 | 25 |
| 策略梯度 | policy gradient | 按奖励（优势）加权，提高好动作的对数概率 | 25 |
| 优势 / 基线 | advantage / baseline | 奖励减去基线；减基线不改变梯度期望，但降低方差 | 25 |
| 价值模型 | value model, critic | 估计某个状态之后期望奖励的模型 | 25 |
| PPO | proximal policy optimization | 用裁剪的重要性比率，限制每次更新的幅度 | 25 |
| 奖励模型的过度优化 | reward overoptimization | 代理奖励一路上升，真实质量先升后降（古德哈特定律） | 25 |
| Best-of-N | Best-of-N | 采样 $N$ 个回答，取奖励最高的 | 25 |
| RLAIF | RL from AI feedback | 用 AI 而不是人来标注偏好 | 25 |
| DPO | direct preference optimization | 不训练奖励模型，直接在偏好对上优化策略 | 26 |
| 隐式奖励 | implicit reward | $\beta\log(\pi_\theta/\pi_{\text{ref}})$，策略本身隐含的奖励 | 26 |
| IPO / KTO / ORPO / SimPO | — | DPO 的几种变体（见第 26 章） | 26 |
| RLVR | RL with verifiable rewards | 用程序可以验证的奖励（答案对错、测试通过）做强化学习 | 27 |
| GRPO | group relative policy optimization | 对同一题的一组回答做组内标准化，作为优势，不需要 critic | 27 |
| 推理模型 | reasoning model | 回答前先生成长思维链的模型，如 o1、R1 | 27 |
| 思维链 | chain of thought, CoT | 模型在给出答案前写出的推理过程 | 27 |
| 熵塌缩 | entropy collapse | 强化学习中策略过早变得确定，失去探索 | 27 |
| PRM / MCTS | process reward model / Monte Carlo tree search | 给每一步打分的奖励模型 / 树搜索；R1 报告这两条路没有走通 | 27 |
| 推理时计算 | test-time compute | 在推理时多花算力（想得更久、多采样、搜索）来提高效果 | 27 |
| Agent | agent | 根据观察到的结果不断调用工具、采取行动的模型系统 | 28 |
| 函数调用（工具调用） | function calling / tool calling | 模型输出结构化的调用请求，由运行环境执行并返回结果 | 28 |
| 约束解码 | constrained decoding | 生成时只允许符合语法（如 JSON Schema）的 token | 28 |
| RAG | retrieval-augmented generation | 先检索相关文档，再基于它们回答 | 28 |
| 提示注入 | prompt injection | 外部内容里夹带的指令被模型当成了用户的指令 | 28 |
| MCP | Model Context Protocol | 连接模型与工具、数据源的开放协议 | 28 |
| 蒸馏 | distillation | 用教师模型的输出分布训练学生模型 | 29 |
| 暗知识 | dark knowledge | 软标签中"错误答案之间的相对概率"所包含的信息 | 29 |
| 前向 KL / 反向 KL | forward / reverse KL | $\mathrm{KL}(p\Vert q)$ 覆盖所有模式；$\mathrm{KL}(q\Vert p)$ 只抓住一个模式 | 29 |
| 在线蒸馏 | on-policy distillation | 学生自己生成，教师逐 token 打分 | 29 |
| 剪枝 | pruning | 从大模型上去掉部分宽度或层数，得到小模型 | 29 |

### A.7 评测、安全与对齐（第 30–32 章）

| 术语 | 英文 | 含义 | 章 |
|------------|-------------|--------------------------|---|
| 基准 | benchmark | 一组固定的测试题和评分方法 | 30 |
| 标准误差 | standard error | $\sqrt{p(1-p)/n}$，题目有限带来的分数不确定性 | 30 |
| pass@$k$ | pass@$k$ | $k$ 次尝试中至少一次正确的概率 | 30 |
| 成对比较 | paired comparison | 在同一批题上逐题比较两个模型，比比较总分更灵敏 | 30 |
| 大模型当评委 | LLM-as-a-judge | 用大模型给回答打分；有位置、长度、偏爱自己等偏差 | 30 |
| 模型规范 | model spec | 写明模型应当怎样行为的文件 | 31 |
| Constitutional AI | Constitutional AI | 用一组写明的原则，让 AI 自己生成反馈来训练 | 31 |
| 过度拒绝 | over-refusal | 拒绝了看起来敏感、实际上正当的请求 | 31 |
| 越狱 | jailbreak | 设法让模型绕过安全训练 | 31 |
| 红队测试 | red teaming | 有组织地寻找模型的漏洞和危险行为 | 31 |
| 危险能力评估 | dangerous capability evaluation | 测量模型在生物、网络安全、自主性等方面的危险能力 | 31 |
| RSP | responsible scaling policy | 按能力阈值预先承诺相应安全措施的框架 | 31 |
| 系统卡 | system card | 随模型发布的能力与安全评估报告 | 31 |
| 谄媚 | sycophancy | 模型一味附和用户 | 31 |
| 探针 | probe | 在模型内部激活上训练的小分类器 | 32 |
| 线性表示假说 | linear representation hypothesis | 概念对应激活空间中的方向 | 32 |
| 叠加 | superposition | 特征数多于维度，用近似正交的方向挤在一起表示 | 32 |
| 稀疏自编码器 | sparse autoencoder, SAE | 把激活分解成大量稀疏特征的自编码器 | 32 |
| 归纳头 | induction head | 实现"找到上次出现的位置，复制下一个 token"的注意力头组合 | 32 |
| 激活修补 / 激活干预 | activation patching / steering | 替换或加减内部激活，检验因果作用或改变行为 | 32 |
| 对齐伪装 | alignment faking | 模型在认为被训练时表现顺从，以避免被修改 | 32 |

### A.8 推理与多模态（第 33–35 章）

| 术语 | 英文 | 含义 | 章 |
|------------|-------------|--------------------------|---|
| prefill / decode | — | 一次性处理输入（计算受限）/ 逐个生成输出（带宽受限） | 33 |
| TTFT / TPOT | time to first token / time per output token | 首 token 延迟 / 每个输出 token 的耗时 | 33 |
| continuous batching | continuous batching | 每个 decode 步骤都可以加入新请求、移出已完成的请求 | 33 |
| PagedAttention | PagedAttention | 把 KV cache 按块分配，用块表管理（vLLM） | 33 |
| 前缀缓存 | prefix caching | 相同前缀的 KV cache 只算一次，多个请求共享 | 33 |
| MBU | model bandwidth utilization | decode 时实际达到的显存带宽 ÷ 峰值带宽 | 33 |
| 量化 | quantization | 用更少的位数存储权重（或激活值、KV cache） | 34 |
| GPTQ / AWQ | — | 两种只量化权重的方法：逐列补偿误差 / 保护重要通道 | 34 |
| 投机解码 | speculative decoding | 草稿模型先猜几个 token，目标模型一次验证；输出分布不变 | 34 |
| 分离部署 | disaggregated serving | prefill 和 decode 在不同的机器上运行 | 34 |
| ViT | vision transformer | 把图片切成小块，当作 token 送进 Transformer | 35 |
| CLIP / SigLIP | — | 用对比学习把图片和文字映射到同一个空间 | 35 |
| 神经音频编解码器 | neural audio codec | 把语音压缩成离散 token、并能还原的网络 | 35 |
| 残差向量量化 | residual vector quantization, RVQ | 逐层量化上一层剩下的误差 | 35 |
| 扩散模型 | diffusion model | 学习逐步去噪，从纯噪声生成数据 | 35 |
| 无分类器引导 | classifier-free guidance, CFG | 把有条件和无条件的预测外推，增强对提示的遵循 | 35 |
| 流匹配 | flow matching | 学习从噪声到数据的速度场，路径更直 | 35 |

### A.9 公司与穿越（第 36–39 章）

| 术语 | 英文 | 含义 | 章 |
|------------|-------------|--------------------------|---|
| 单位经济 | unit economics | 每个请求或每个用户的收入与成本 | 36 |
| DGX-1 / DGX-2 | — | NVIDIA 的 8 卡服务器（混合立方体网格，非全互联）/ 16 卡 NVSwitch 全互联服务器 | 37 |
| TPU | tensor processing unit | Google 的矩阵计算芯片，v2 起支持 bf16 | 37 |
| 去风险训练 | de-risking run | 正式大规模训练前，用较小规模把整套系统完整跑一遍 | 39 |
