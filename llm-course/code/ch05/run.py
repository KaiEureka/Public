import sys, json, time
from collections import Counter
sys.path.insert(0, ".")
from bpe import BPE, pretokenize
T0 = time.time()
text = open(sys.argv[1], encoding="utf-8").read(); n = int(0.9 * len(text)); tr, va = text[:n], text[n:]
zdir = sys.argv[2]
zh_train = "\n".join(p for f in ("tang0.json", "tang1000.json") for poem in json.load(open(f"{zdir}/{f}", encoding="utf-8")) for p in poem["paragraphs"])
zh_test = "\n".join(p for ch in json.load(open(f"{zdir}/mengzi.json", encoding="utf-8")) for p in ch["paragraphs"])

print("pre-tokenization example:", pretokenize("First Citizen:\nWe know't, we know't. Price: 12345 dollars!"))

print("\n[1] train byte-level BPE on Shakespeare (train split), first merges:")
tok = BPE(); tok.train(tr, 8192, verbose_first=15)
print(f"  ({time.time()-T0:.0f}s)")

print("\n[2] compression on Shakespeare validation split vs vocab size")
vb = len(va.encode("utf-8"))
for V in (256, 512, 1024, 2048, 4096, 8192):
    t = BPE(); t.merges = {p: i for p, i in tok.merges.items() if i < V}; t.vocab = {i: b for i, b in tok.vocab.items() if i < V}
    ids = t.encode(va)
    print(f"  V={V:5d}: {len(ids):7,d} tokens, {vb/len(ids):.2f} bytes/token")
    if V in (512, 8192):
        for s in ["To be, or not to be: that is the question.", "Methinks the lady doth protest too much."]:
            print(f"      {t.show(s)}")

ids = tok.encode(tr); freq = Counter(ids)
rare = sum(1 for i in range(8192) if freq[i] < 10)
print(f"\n[3] V=8192 on its own training text: {rare} of 8192 tokens appear fewer than 10 times")
print("  some long tokens:", [tok.vocab[i].decode() for i in sorted(range(256, 8192), key=lambda i: -len(tok.vocab[i]))[:8]])

print("\n[4] spelling / numbers with the V=8192 tokenizer")
for s in [" strawberry", " Strawberry", " STRAWBERRY", " 1234567", " 3.14159"]:
    print(f"  {s!r:15s} -> {tok.show(s)}")

print("\n[5] Chinese")
print("  UTF-8 bytes of '孟子見梁惠王':", " ".join(f"{b:02X}" for b in "孟子見梁惠王".encode("utf-8")))
nchar = len(zh_test)
ids_en = tok.encode(zh_test)
print(f"  English-trained tokenizer on Mengzi: {len(ids_en)/nchar:.2f} tokens per Chinese char")
print(f"     {tok.show('孟子見梁惠王。')}")
mix = BPE(); mix.train(tr + "\n" + zh_train, 8192)
ids_mix = mix.encode(zh_test); ids_mix_en = mix.encode(va)
print(f"  mixed (Shakespeare + Tang poems) tokenizer, V=8192: {len(ids_mix)/nchar:.2f} tokens per Chinese char on Mengzi;"
      f" English: {vb/len(ids_mix_en):.2f} bytes/token (was {vb/len(tok.encode(va)):.2f})")
print(f"     {mix.show('孟子見梁惠王。')}")
print(f"total {time.time()-T0:.0f}s")
