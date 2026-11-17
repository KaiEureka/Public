import math

class Value:
    """一个标量节点：记住自己的值、梯度、由谁算出来、以及如何把梯度传回去。"""
    def __init__(self, data, parents=(), op=""):
        self.data, self.grad = data, 0.0
        self._parents, self._op = parents, op
        self._backward = lambda: None

    def __add__(self, other):
        out = Value(self.data + other.data, (self, other), "+")
        def _backward():                      # d(a+b)/da = 1, d(a+b)/db = 1
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        out = Value(self.data * other.data, (self, other), "*")
        def _backward():                      # d(ab)/da = b, d(ab)/db = a
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,), "tanh")
        def _backward():                      # d tanh(x)/dx = 1 - tanh(x)^2
            self.grad += (1 - t * t) * out.grad
        out._backward = _backward
        return out

    def backward(self):
        order, seen = [], set()
        def visit(v):                         # 拓扑排序：保证处理一个节点前，它的所有下游都已处理完
            if v not in seen:
                seen.add(v)
                for p in v._parents:
                    visit(p)
                order.append(v)
        visit(self)
        self.grad = 1.0                       # dL/dL = 1
        for v in reversed(order):
            v._backward()

# 课上的手算例子
a, b, c, f = Value(3.0), Value(-2.0), Value(5.0), Value(4.0)
e = a * b
d = e + c
L = d * f
L.backward()
print(f"L = {L.data}")
for name, v in [("a", a), ("b", b), ("c", c), ("f", f), ("e", e), ("d", d)]:
    print(f"dL/d{name} = {v.grad}")

# 数值验证：把 a 增加一点点，看 L 变多少
h = 1e-6
L2 = ((Value(3.0 + h) * b) + c) * f
print(f"numerical dL/da = {(L2.data - L.data) / h:.6f}")

# 一个变量被用了两次：梯度要相加
x = Value(3.0)
y = x * x            # y = x^2, dy/dx = 2x = 6
y.backward()
print(f"y = x*x, dy/dx = {x.grad}")
