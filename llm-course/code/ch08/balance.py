"""Toy simulation of DeepSeek-V3-style auxiliary-loss-free load balancing (router only, no training)."""
import numpy as np
rng = np.random.default_rng(0)
E, k, d, N = 16, 2, 32, 8192                       # experts, top-k, hidden dim, tokens per batch
centroids = rng.normal(0, 1, (E, d)) * np.linspace(0.6, 1.6, E)[:, None]   # some experts naturally "louder"
def batch(): return rng.normal(0, 1, (N, d)) / np.sqrt(d) * 3

def route(x, bias):
    s = 1 / (1 + np.exp(-(x @ centroids.T)))       # affinity scores (sigmoid), shape (N, E)
    top = np.argsort(-(s + bias), axis=1)[:, :k]   # bias only affects WHICH experts are chosen
    g = np.take_along_axis(s, top, 1); g /= g.sum(1, keepdims=True)   # gate weights use raw scores
    load = np.bincount(top.ravel(), minlength=E)
    return load, g

ideal = N * k / E
bias, gamma = np.zeros(E), 0.002
load, _ = route(batch(), bias)
print(f"without balancing: max load / ideal = {load.max()/ideal:.2f}, min = {load.min()/ideal:.2f}")
print("   load per expert:", load.tolist())
for step in range(1, 1001):
    load, g = route(batch(), bias)
    bias -= gamma * np.sign(load - ideal)          # overloaded -> lower bias, underloaded -> raise bias
    if step in (10, 100, 300, 1000):
        print(f"step {step:4d}: max load / ideal = {load.max()/ideal:.2f}, min = {load.min()/ideal:.2f}")
print("   load per expert:", load.tolist())
print("   learned bias:", np.round(bias, 3).tolist())
