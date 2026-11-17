"""KV cache on the lesson-6 GPT: correctness on the trained model, speed on a longer-context copy."""
import sys, math, time, torch, torch.nn.functional as F
torch.set_num_threads(4); torch.manual_seed(0)
L6 = sys.argv[1]
sys.argv = ["gpt.py", sys.argv[2], "0", "128", "128", "4", "4", "32"]
exec(open(f"{L6}/gpt.py").read().split("model = GPT(")[0])

@torch.no_grad()
def forward_cached(m, idx, cache, pos0):
    """Process only the NEW tokens idx (B, t); keys/values of earlier tokens come from cache."""
    B, t = idx.shape
    x = m.tok(idx) + m.pos(torch.arange(pos0, pos0 + t))
    for l, blk in enumerate(m.blocks):
        a = blk.attn; dn = x.shape[-1]; dh = dn // a.H
        q, k, v = a.qkv(blk.ln1(x)).split(dn, dim=2)
        q, k, v = (z.view(B, t, a.H, dh).transpose(1, 2) for z in (q, k, v))
        if cache[l] is not None:
            k = torch.cat([cache[l][0], k], 2); v = torch.cat([cache[l][1], v], 2)
        cache[l] = (k, v)                                         # store K, V for all tokens so far
        att = q @ k.transpose(-2, -1) / math.sqrt(dh)              # (B, H, t, pos0 + t)
        qpos = torch.arange(pos0, pos0 + t)[:, None]; kpos = torch.arange(pos0 + t)[None, :]
        att = att.masked_fill(kpos > qpos, float("-inf")).softmax(-1)
        x = x + a.proj((att @ v).transpose(1, 2).reshape(B, t, dn))
        x = x + blk.mlp(blk.ln2(x))
    return m.head(m.ln_f(x))

@torch.no_grad()
def gen_naive(m, prompt, n):
    ctx = prompt.clone()
    for _ in range(n):
        nxt = m(ctx)[:, -1].argmax(-1, keepdim=True); ctx = torch.cat([ctx, nxt], 1)   # recompute everything
    return ctx

@torch.no_grad()
def gen_cached(m, prompt, n):
    cache = [None] * len(m.blocks)
    logits = forward_cached(m, prompt, cache, 0)                   # prefill: whole prompt at once
    ctx = prompt.clone()
    for i in range(n):
        nxt = logits[:, -1].argmax(-1, keepdim=True); ctx = torch.cat([ctx, nxt], 1)
        if i < n - 1: logits = forward_cached(m, nxt, cache, ctx.shape[1] - 1)          # decode: 1 token
    return ctx

# 1) correctness on the trained model (greedy decoding must match exactly)
m = GPT(V, T, d, L, H); m.load_state_dict(torch.load(f"{L6}/gpt_T128.pt")); m.eval()
prompt = val[:28][None]
a, b = gen_naive(m, prompt, 100), gen_cached(m, prompt, 100)
print("trained model, greedy, 100 new tokens: identical =", torch.equal(a, b))
print("   text:", repr("".join(chars[i] for i in b[0, 28:].tolist())[:80]))

# 2) speed: same architecture, longer context (random weights are fine for timing)
big = GPT(V, 1024, 256, 4, 8).eval()
p = torch.randint(0, V, (1, 32))
print("\nd=256, 4 layers: time to generate n tokens after a 32-token prompt")
for n in (128, 256, 512, 960):
    t0 = time.time(); gen_naive(big, p, n); tn = time.time() - t0
    t0 = time.time(); gen_cached(big, p, n); tc = time.time() - t0
    print(f"   n={n:4d}: no cache {tn:6.2f}s   KV cache {tc:5.2f}s   speedup {tn/tc:5.1f}x")

# 3) batching: one decode step for B sequences that each already have 512 cached tokens
print("\ndecode step with 512 cached tokens per sequence, varying batch size B")
for Bsz in (1, 4, 16, 64):
    cache = [None] * 4
    forward_cached(big, torch.randint(0, V, (Bsz, 512)), cache, 0)
    tok = torch.randint(0, V, (Bsz, 1))
    t0 = time.time()
    for s in range(20):
        c2 = [(k[:, :, :512], v[:, :, :512]) for k, v in cache]   # keep length fixed for timing
        forward_cached(big, tok, c2, 512)
    st = (time.time() - t0) / 20
    print(f"   B={Bsz:3d}: {st*1e3:6.1f} ms per step  ->  {Bsz/st:8.0f} tokens/s total, {1/st:6.0f} tokens/s per sequence")
