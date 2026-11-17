"""Ring all-reduce written by hand with point-to-point send/recv (torch.distributed, gloo backend, CPU processes)."""
import os, time, torch, torch.distributed as dist, torch.multiprocessing as mp

def ring_all_reduce(x, trace=False):
    r, N = dist.get_rank(), dist.get_world_size()
    nxt, prv = (r + 1) % N, (r - 1) % N
    chunks = list(x.chunk(N)); sent = 0
    for step in range(N - 1):                                  # phase 1: reduce-scatter
        s_idx, r_idx = (r - step) % N, (r - step - 1) % N
        buf = torch.empty_like(chunks[r_idx])
        reqs = [dist.isend(chunks[s_idx], nxt), dist.irecv(buf, prv)]
        for q in reqs: q.wait()
        chunks[r_idx] += buf; sent += chunks[s_idx].numel()
        if trace: report(f"after reduce-scatter step {step+1}", x)
    for step in range(N - 1):                                  # phase 2: all-gather
        s_idx, r_idx = (r + 1 - step) % N, (r - step) % N
        buf = torch.empty_like(chunks[r_idx])
        reqs = [dist.isend(chunks[s_idx], nxt), dist.irecv(buf, prv)]
        for q in reqs: q.wait()
        chunks[r_idx].copy_(buf); sent += chunks[s_idx].numel()
        if trace: report(f"after all-gather step {step+1}", x)
    return sent

def report(title, x):
    out = [torch.zeros_like(x) for _ in range(dist.get_world_size())]
    dist.all_gather(out, x)                                    # only to print every rank's state
    if dist.get_rank() == 0:
        print(f"  {title:28s} " + " | ".join(f"GPU{i}: {[int(v) for v in o.tolist()]}" for i, o in enumerate(out)))

def worker(r, N):
    os.environ.update(MASTER_ADDR="127.0.0.1", MASTER_PORT="29511")
    dist.init_process_group("gloo", rank=r, world_size=N)
    torch.set_num_threads(1)
    # 1) tiny traced example: GPU r holds 10^r * [1, 2, 3, 4]
    x = torch.tensor([1., 2., 3., 4.]) * 10 ** r
    if r == 0: print("[1] traced ring all-reduce, 4 ranks, 4 chunks of 1 element")
    report("initial", x); ring_all_reduce(x, trace=True)
    # 2) correctness + traffic on a 64 MB tensor
    torch.manual_seed(r); big = torch.randn(16 * 2**20)
    ref = big.clone(); dist.all_reduce(ref)
    dist.barrier(); t0 = time.time(); sent = ring_all_reduce(big); dist.barrier(); t = time.time() - t0
    err = (big - ref).abs().max().item()
    if r == 0:
        print(f"\n[2] 64 MB tensor, {N} ranks: max |mine - dist.all_reduce| = {err:.2e}")
        print(f"    elements sent per rank = {sent:,} = {sent/big.numel():.3f} x tensor size "
              f"(theory 2(N-1)/N = {2*(N-1)/N:.3f});  wall time {t*1e3:.0f} ms")
    dist.destroy_process_group()

if __name__ == "__main__":
    mp.spawn(worker, args=(4,), nprocs=4)
