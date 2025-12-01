# Part 1: Foundations

[Back to Home](Home)

## Overview

This part establishes the biological inspiration for neural networks and introduces the fundamental computation performed by a single artificial neuron.

**Key Question:** How do biological neurons inspire artificial intelligence?

---

## Topics

### Topic 01: Biological vs Artificial Neuron

**Key Concept:** Artificial neurons mimic biological neurons mathematically.

| Biological | Artificial |
|------------|------------|
| Dendrites receive signals | Inputs (x1, x2, ...) |
| Synaptic strengths | Weights (w1, w2, ...) |
| Soma integrates signals | Weighted sum (Sigma wi*xi) |
| Axon firing decision | Activation function f() |

**Core Formula:** y = f(w1*x1 + w2*x2 + ... + b)

---

### Topic 02: Single Neuron Computation

**Key Concept:** A neuron performs two operations: weighted sum, then activation.

**Step 1 - Weighted Sum:**
```
z = w1*x1 + w2*x2 + w3*x3 + b
```

**Step 2 - Sigmoid Activation:**
```
y = 1 / (1 + e^(-z))
```

**Example:**
- Inputs: Price=100, Volume=0.85, Sentiment=0.6
- Weights: w1=0.5, w2=0.3, w3=0.4, b=-0.5
- z = 0.5(100/100) + 0.3(0.85) + 0.4(0.6) - 0.5 = 0.745
- y = sigmoid(0.745) = 0.678 (67.8% confidence -> BUY)

---

### Topic 11: Problem Visualization

**Key Concept:** Real market data is not linearly separable.

When plotting features (returns vs volume, sentiment vs volatility), "up" and "down" days are intermixed. No single straight line can separate them cleanly.

**Why simple rules fail:**
- "Buy when volume is high" - high volume includes both winners and losers
- "Buy when sentiment is positive" - sentiment doesn't guarantee direction
- Relationships are **non-linear** - combinations matter

---

### Topic 12: Decision Boundary Concept

**Key Concept:** A decision boundary separates classes in feature space.

| Type | Shape | Created By |
|------|-------|------------|
| Linear | Straight line/plane | Single neuron |
| Curved | Flexible shape | Multiple neurons in hidden layers |

Linear boundaries work when classes are cleanly separated. Curved boundaries are needed when classes are interleaved (XOR pattern).

---

### Topic 13: Neuron Decision Maker

**Key Concept:** Neurons make binary decisions by comparing output to a threshold.

**Decision Rule:**
- If output > 0.5: Predict UP (BUY)
- If output <= 0.5: Predict DOWN (SELL)

The threshold can be adjusted:
- Higher threshold (0.7): More conservative, fewer trades
- Lower threshold (0.3): More aggressive, more trades

---

## Discussion Questions

1. What real-world processes benefit from learning vs explicit rules? (Think: spam filtering, image recognition, medical diagnosis)

2. How is the "all-or-nothing" firing of biological neurons different from the smooth sigmoid output?

3. Can you think of a business problem that is clearly linearly separable vs one that is not?

---

## Summary

| Topic | Key Takeaway |
|-------|--------------|
| 01 | Biological neurons inspire artificial neuron structure |
| 02 | Two-step computation: weighted sum, then activation |
| 11 | Real data is messy - simple rules fail |
| 12 | Linear vs curved boundaries determine what's solvable |
| 13 | Threshold converts probability to decision |

**Next:** [[Part 2: Building Blocks|Part-2-Building-Blocks]] - Activation functions and why we need them
