"""Compute-optimal allocation from the Chinchilla parametric fit L(N,D) = E + A/N^a + B/D^b.
Constants: Epoch AI's corrected re-fit of Hoffmann et al. (2022) data (Besiroglu et al., 2024)."""
import numpy as np
E, A, B, a, b = 1.8172, 482.01, 2085.43, 0.3478, 0.3658
L = lambda N, D: E + A / N**a + B / D**b

def optimal(C):                       # minimize L subject to C = 6 N D (grid search over N)
    Ns = np.logspace(7, 14, 20001); Ds = C / (6 * Ns)
    i = np.argmin(L(Ns, Ds)); return Ns[i], Ds[i], L(Ns[i], Ds[i])

print("compute-optimal allocation:")
for C in (1e21, 1e22, 1e23, 1e24, 1e25, 1e26):
    N, D, l = optimal(C)
    print(f"  C={C:.0e}: N={N/1e9:8.2f}B  D={D/1e12:7.2f}T tokens  D/N={D/N:5.1f}  loss={l:.4f}")

C = 1e24; N0, D0, l0 = optimal(C)
print(f"\nfixed C=1e24: moving away from the optimum (N0={N0/1e9:.1f}B)")
for f in (1/16, 1/8, 1/4, 1/2, 1, 2, 4):
    N = N0 * f; D = C / (6 * N)
    print(f"  N = {f:>6.4g} x N0 = {N/1e9:7.2f}B, D = {D/1e12:6.2f}T, D/N = {D/N:7.1f}: loss {L(N, D):.4f} (+{L(N, D)-l0:.4f})")

print("\nLlama-3-8B-like overtraining: N=8B, D=15T")
C8 = 6 * 8e9 * 15e12; Nopt, Dopt, lopt = optimal(C8)
print(f"  C={C8:.2e}, loss(8B,15T)={L(8e9, 15e12):.4f}; optimal for this C: N={Nopt/1e9:.1f}B D={Dopt/1e12:.2f}T loss={lopt:.4f}")
# how much compute would the optimal path need to reach the 8B@15T loss?
target = L(8e9, 15e12)
Cs = np.logspace(22, 25, 3001); ls = np.array([optimal(c)[2] for c in Cs[::10]])
c_match = Cs[::10][np.argmin(np.abs(ls - target))]
print(f"  compute-optimal model reaches the same loss at C~{c_match:.2e} ({C8/c_match:.1f}x less training compute)")
n_m, d_m, _ = optimal(c_match)
print(f"     that model: N={n_m/1e9:.1f}B, D={d_m/1e12:.2f}T  -> but inference costs {n_m/8e9:.1f}x more per token")
