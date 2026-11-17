"""What Muon's Newton-Schulz step does to a gradient-like matrix's singular values."""
import torch
torch.manual_seed(0)

def newton_schulz(G, steps=5):
    a, b, c = 3.4445, -4.7750, 2.0315            # quintic coefficients from Keller Jordan's Muon
    X = G / (G.norm() + 1e-7)                     # scale so every singular value is <= 1
    T = G.shape[0] > G.shape[1]
    if T: X = X.T
    for _ in range(steps):
        A = X @ X.T
        X = a * X + (b * A + c * A @ A) @ X       # odd polynomial in X: acts on singular values only
    return X.T if T else X

m, n = 256, 512
U, _ = torch.linalg.qr(torch.randn(m, m)); V, _ = torch.linalg.qr(torch.randn(n, m))
s = torch.cat([torch.tensor([50., 20., 8.]), torch.logspace(0, -3, m - 3)])   # a few dominant directions
G = U @ torch.diag(s) @ V.T                                                     # "gradient-like" matrix
O = newton_schulz(G)
sv_in = torch.linalg.svdvals(G); sv_out = torch.linalg.svdvals(O)
pick = [0, 1, 2, 10, 50, 128, 255]
print("singular value index:  " + " ".join(f"{i:>8d}" for i in pick))
print("gradient G:            " + " ".join(f"{sv_in[i]:8.3f}" for i in pick))
print("after Newton-Schulz:   " + " ".join(f"{sv_out[i]:8.3f}" for i in pick))
exact = U @ V.T
cos = (O * exact).sum() / (O.norm() * exact.norm())
print(f"cosine similarity with exact U V^T: {cos:.3f}")
print(f"share of update norm in top-3 directions: G {(sv_in[:3]**2).sum()/(sv_in**2).sum():.1%}  ->  NS {(sv_out[:3]**2).sum()/(sv_out**2).sum():.1%}")
