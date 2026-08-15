---
title: 反向传播到底在算什么
date: 2026-08-15
category: 深度学习
tags: [反向传播, 梯度, 链式法则, 基础]
summary: 反向传播只是链式法则的工程化实现。本文从单神经元出发，把梯度是怎么一层层传回来的讲清楚。
---

反向传播（Backpropagation）听起来高深，本质就是**链式法则**在计算图上的系统化应用：为了更新参数，我们需要损失函数对每个参数的梯度，而梯度可以顺着计算图从输出反向一路乘回来。

## 一个神经元

考虑单神经元 $z = w x + b$，经过激活 $\sigma$ 得到输出 $a = \sigma(z)$，损失记为 $L$。

我们要算的是 $\frac{\partial L}{\partial w}$ 与 $\frac{\partial L}{\partial b}$。

## 链式法则

先对 $z$ 求梯度（「误差项」）：

$$
\delta = \frac{\partial L}{\partial z}
       = \frac{\partial L}{\partial a} \cdot \sigma'(z)
$$

再往参数回传：

$$
\frac{\partial L}{\partial w} = \delta \cdot x, \qquad
\frac{\partial L}{\partial b} = \delta
$$

## 多层网络

对第 $l$ 层，误差项层层递推：

$$
\delta^{(l)} = \big((W^{(l+1)})^\top \delta^{(l+1)}\big) \odot \sigma'(z^{(l)})
$$

于是任意参数梯度：

$$
\frac{\partial L}{\partial W^{(l)}} = \delta^{(l)} (a^{(l-1)})^\top
$$

## 用 NumPy 感受一下

```python
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# 前向
z1 = W1 @ x + b1
a1 = sigmoid(z1)
z2 = W2 @ a1 + b2
a2 = sigmoid(z2)

# 反向（二分类交叉熵 + sigmoid 的简化梯度）
delta2 = (a2 - y)                 # 输出层误差项
dW2 = np.outer(delta2, a1)
db2 = delta2
delta1 = (W2.T @ delta2) * a1 * (1 - a1)
dW1 = np.outer(delta1, x)
db1 = delta1
```

## 关键直觉

- **前向算值，反向算梯度**，两者共用同一张计算图。
- 每一层的「误差项」$\delta$ 就是梯度继续往前传的「货币」。
- 框架（PyTorch/TensorFlow）帮我们自动建图、自动求导，但你理解链式法则，才能在梯度消失、形状对不上时知道去哪排查。

> 提醒：激活函数导数 $\sigma'$ 在饱和区接近 0，会导致梯度消失——这正是 ReLU 被广泛采用的原因。
