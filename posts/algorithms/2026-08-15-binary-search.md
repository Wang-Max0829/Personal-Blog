---
title: 二分查找：模板、边界与常见坑
date: 2026-08-15
category: 算法
tags: [二分, 查找, 复杂度, 模板]
summary: 二分查找看似简单，却在边界处理上极易出错。本文给出一套不易写错的通用模板，并讨论几种典型变体。
---

二分查找的核心思想是：**在有序区间上，每次用中点把搜索空间砍掉一半**。时间复杂度稳定为 $O(\log n)$，是「在有序结构中定位目标」的首选武器。

## 最朴素的版本

在「无重复、找等于 target 的下标」时：

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

## 为什么总写错？

出错几乎都集中在三点：

1. **循环条件**用 `lo < hi` 还是 `lo <= hi`？
2. **更新边界**时用 `mid` 还是 `mid ± 1`？
3. **返回值**该返回 `lo`、`hi` 还是 `mid`？

一个不容易错的统一思路是：**维护「答案一定在 [lo, hi] 内」的不变量**。

## 通用模板（找下界 / 左边界）

当我们要找「第一个 ≥ target 的位置」（lower_bound）时：

```python
def lower_bound(arr, target):
    lo, hi = 0, len(arr)          # 注意 hi 取 n，表示「可取到末尾之后」
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

这里的关键变化：

- 区间定义为 `[lo, hi)`（左闭右开），`hi = n` 是合理的；
- 循环条件为 `lo < hi`，退出时 `lo == hi`，即为答案；
- `arr[mid] < target` 时答案不可能在 `mid`，故 `lo = mid + 1`；否则答案可能在 `mid`，故 `hi = mid`。

## 复杂度

| 操作 | 复杂度 |
| --- | --- |
| 查找 | $O(\log n)$ |
| 空间 | $O(1)$ |

## 小结

- 写二分前先想清：**要找的是哪个边界**（下界 / 上界 / 精确值）。
- 固定用「左闭右开 + `lo < hi`」模板，能覆盖绝大多数变体。
- 边界更新务必保证**每次循环区间至少缩小 1**，避免死循环。
