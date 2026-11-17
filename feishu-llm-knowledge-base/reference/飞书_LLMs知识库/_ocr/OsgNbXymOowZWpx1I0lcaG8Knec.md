```cpp
__global__ void FusedAddRMSNormKernel(
    const half* x, const half* y, const half* gamma,
    half* out, float eps, int D)
{
    int row = blockIdx.x;          // 每个 block 处理一行
    int tid = threadIdx.x;         // 线程在线程块内索引
    extern __shared__ float s_rms; // 共享内存用于归约平方和

    if (row >= N) return;

    // 1. 加载 x 和 y 到寄存器，计算残差和，同时计算平方和
    float sum_sq = 0.0f;
    for (int i = tid; i < D; i += blockDim.x) {
        float val = __half2float(x[row * D + i]) + __half2float(y[row * D + i]);
        sum_sq += val * val;
    }

    // 2. 块内归约求平方和
    // 简化：使用 warp 级 shuffle 归约，最终 block 内 sum_sq 存于 s_rms[0]
    // ... (归约步骤)
    if (tid == 0) s_rms[0] = sum_sq;
    __syncthreads();
    float rms = sqrt(s_rms[0] / D + eps);

    // 3. 计算归一化输出并写回
    for (int i = tid; i < D; i += blockDim.x) {
        float val = __half2float(x[row * D + i]) + __half2float(y[row * D + i]);
        float norm_val = val / rms;
        float out_val = norm_val * __half2float(gamma[i]);
        out[row * D + i] = __float2half(out_val);
    }
}
```
