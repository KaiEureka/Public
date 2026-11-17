"""Byte-level BPE tokenizer from scratch (GPT-4-style pre-tokenization)."""
import heapq
from collections import Counter, defaultdict
import regex

# GPT-4 (cl100k) pre-tokenization pattern; Llama 3 uses the same one
PAT = regex.compile(r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+""")

def pretokenize(text):
    return PAT.findall(text)

class BPE:
    def __init__(self):
        self.merges = {}                                   # (a, b) -> new token id, in learned order
        self.vocab = {i: bytes([i]) for i in range(256)}   # token id -> bytes

    def train(self, text, vocab_size, verbose_first=0):
        words = Counter(tuple(w.encode("utf-8")) for w in pretokenize(text))
        words = [[list(w), c] for w, c in words.items()]
        pair_count, where = Counter(), defaultdict(set)
        for wi, (sym, c) in enumerate(words):
            for p in zip(sym, sym[1:]):
                pair_count[p] += c; where[p].add(wi)
        heap = [(-c, p) for p, c in pair_count.items()]; heapq.heapify(heap)
        new_id = 256
        while new_id < vocab_size and heap:
            negc, p = heapq.heappop(heap)
            if pair_count.get(p, 0) != -negc or -negc < 2:   # stale heap entry
                if pair_count.get(p, 0) >= 2: heapq.heappush(heap, (-pair_count[p], p))
                continue
            self.merges[p] = new_id; self.vocab[new_id] = self.vocab[p[0]] + self.vocab[p[1]]
            if new_id - 256 < verbose_first:
                print(f"  merge {new_id - 255:3d}: {self.vocab[p[0]]!r:>10} + {self.vocab[p[1]]!r:<10} -> {self.vocab[new_id]!r}  (count {-negc})")
            changed = set()
            for wi in list(where[p]):
                sym, c = words[wi]
                for q in zip(sym, sym[1:]):                    # remove old pairs of this word
                    pair_count[q] -= c; where[q].discard(wi)
                out, i = [], 0
                while i < len(sym):
                    if i + 1 < len(sym) and (sym[i], sym[i + 1]) == p:
                        out.append(new_id); i += 2
                    else:
                        out.append(sym[i]); i += 1
                words[wi][0] = out
                for q in zip(out, out[1:]):                    # add new pairs
                    pair_count[q] += c; where[q].add(wi); changed.add(q)
            for q in changed:
                heapq.heappush(heap, (-pair_count[q], q))
            new_id += 1

    def encode_word(self, b):
        sym = list(b)
        while len(sym) > 1:
            pairs = [(self.merges.get(q, 1 << 30), i) for i, q in enumerate(zip(sym, sym[1:]))]
            rank, i = min(pairs)
            if rank == 1 << 30: break                       # no learned merge applies
            sym[i:i + 2] = [rank]
        return sym

    def encode(self, text):
        cache, out = {}, []
        for w in pretokenize(text):
            if w not in cache: cache[w] = self.encode_word(w.encode("utf-8"))
            out.extend(cache[w])
        return out

    def decode(self, ids):
        return b"".join(self.vocab[i] for i in ids).decode("utf-8", errors="replace")

    def show(self, text):
        return "|".join(self.vocab[i].decode("utf-8", errors="replace") for i in self.encode(text))
