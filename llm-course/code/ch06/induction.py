"""Look for a previous-token head and an induction head in the trained ch06 GPT.
Feed random letter strings repeated twice; compare loss on the two copies and score every head.
Run inside code/ch06:  python3 induction.py"""
import sys, math, torch, torch.nn.functional as F
sys.argv = ["gpt.py", "../data/shakespeare.txt", "0", "128", "128", "4", "4", "32"]
exec(open("gpt.py").read().split("model = GPT(")[0])
model = GPT(V, T, d, L, H); model.load_state_dict(torch.load("gpt_T128.pt")); model.eval()
g = torch.Generator().manual_seed(0)
letters = torch.tensor([stoi[c] for c in "abcdefghijklmnopqrstuvwxyz"])
Lr, n = 60, 64                                    # random string length, number of strings
seq = letters[torch.randint(0, 26, (n, Lr), generator=g)]
x = torch.cat([seq, seq], dim=1)                  # (n, 120): the same random string twice
with torch.no_grad():
    logits = model(x[:, :-1])
loss = F.cross_entropy(logits.transpose(1, 2), x[:, 1:], reduction="none") / math.log(2)
print(f"loss on 1st copy (positions 1-59):   {loss[:, :Lr-1].mean():.2f} bits/char")
print(f"loss on 2nd copy (positions 61-119): {loss[:, Lr:].mean():.2f} bits/char")
idx = torch.arange(Lr + 1, 2 * Lr - 1)            # query positions inside the 2nd copy
for l, blk in enumerate(model.blocks):
    att = blk.attn.last_att                       # (n, H, T, T)
    for h in range(H):
        a = att[:, h]
        prev = a[:, idx, idx - 1].mean()          # attention to the immediately previous position
        ind = a[:, idx, idx - Lr + 1].mean()      # attention to the token AFTER the earlier copy of the current token
        print(f"  layer {l} head {h}: to previous token {prev:.2f}   to 'next of earlier copy' {ind:.2f}")
