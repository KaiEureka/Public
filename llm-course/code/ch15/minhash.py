"""MinHash + LSH near-duplicate detection demo (FineWeb-like settings: word 5-grams, 14 bands x 8 rows)."""
import sys, re, hashlib, time
import numpy as np
from collections import defaultdict
rng = np.random.default_rng(0); t0 = time.time()
words = re.findall(r"\S+", open(sys.argv[1], encoding="utf-8").read())
docs = [words[i:i + 80] for i in range(0, len(words) - 80, 80)][:3000]
vocab = sorted(set(words))                          # sorted: set order of strings changes from run to run
pairs = []                                            # (original index, variant index, edit fraction)
for p in (0.02, 0.05, 0.1, 0.2, 0.3, 0.5):
    for i in rng.choice(len(docs), 50, replace=False):
        d = list(docs[i])
        for j in rng.choice(len(d), int(round(p * len(d))), replace=False):
            d[j] = vocab[rng.integers(len(vocab))]   # replace a fraction p of the words
        docs.append(d); pairs.append((i, len(docs) - 1, p))

def shingles(d, n=5):
    return {int.from_bytes(hashlib.md5(" ".join(d[i:i + n]).encode()).digest()[:8], "little")
            for i in range(len(d) - n + 1)}
S = [np.fromiter(shingles(d), dtype=np.uint64) for d in docs]
def jaccard(a, b): a, b = set(a.tolist()), set(b.tolist()); return len(a & b) / len(a | b)

B, R = 14, 8; K = B * R; P = (1 << 61) - 1
A = rng.integers(1, P, K, dtype=np.uint64); C = rng.integers(0, P, K, dtype=np.uint64)
def minhash(s):                                       # K random affine hashes, keep the minimum of each
    x = (s[None, :] % np.uint64(P)).astype(object)
    h = (A[:, None].astype(object) * x + C[:, None].astype(object)) % P
    return np.array([min(row) for row in h], dtype=object)
sig = [minhash(s) for s in S]
buckets = defaultdict(list)
for di, sgn in enumerate(sig):
    for b in range(B):
        buckets[(b, tuple(sgn[b * R:(b + 1) * R]))].append(di)
cand = set()
for members in buckets.values():
    for x in range(len(members)):
        for y in range(x + 1, len(members)): cand.add((members[x], members[y]))

print(f"{len(docs)} documents, {len(cand)} candidate pairs found by LSH  ({time.time()-t0:.0f}s)")
print("edit fraction | mean Jaccard | detected (LSH) | theory 1-(1-J^8)^14 | exact-hash dedup")
for p in (0.02, 0.05, 0.1, 0.2, 0.3, 0.5):
    rows = [(i, j) for i, j, q in pairs if q == p]
    J = np.array([jaccard(S[i], S[j]) for i, j in rows])
    det = np.mean([(min(i, j), max(i, j)) in cand for i, j in rows])
    theory = np.mean(1 - (1 - J ** R) ** B)
    print(f"     {p:4.2f}     |    {J.mean():.3f}     |     {det:5.0%}      |       {theory:5.0%}        |      0%")
injected = {(min(i, j), max(i, j)) for i, j, _ in pairs}
others = [c for c in cand if c not in injected]
print(f"other candidate pairs (not injected): {len(others)}", end="")
if others: print(f", their Jaccard: {[round(jaccard(S[a], S[b]), 2) for a, b in others[:5]]}")
else: print()
print(f"LSH threshold (1/b)^(1/r) = {(1 / B) ** (1 / R):.3f}")
