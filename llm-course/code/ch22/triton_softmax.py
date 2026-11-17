"""A fused row-softmax Triton kernel, run on CPU with TRITON_INTERPRET=1 (correctness only, no speed)."""
import torch, triton, triton.language as tl

@triton.jit
def softmax_kernel(out_ptr, in_ptr, n_cols, BLOCK: tl.constexpr):
    row = tl.program_id(0)                                   # one program instance per row
    offs = tl.arange(0, BLOCK)
    mask = offs < n_cols
    x = tl.load(in_ptr + row * n_cols + offs, mask=mask, other=-float("inf"))   # read the row once
    x = x - tl.max(x, axis=0)                                # everything below stays in registers
    num = tl.exp(x)
    tl.store(out_ptr + row * n_cols + offs, num / tl.sum(num, axis=0), mask=mask)  # write once

x = torch.randn(64, 1000)
y = torch.empty_like(x)
softmax_kernel[(x.shape[0],)](y, x, x.shape[1], BLOCK=triton.next_power_of_2(x.shape[1]))
print("max |triton - torch.softmax| =", (y - torch.softmax(x, -1)).abs().max().item())
