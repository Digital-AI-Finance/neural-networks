# Part 2: Building Blocks

[Back to Home](Home)

## Overview

This part explores activation functions - the non-linear transformations that give neural networks their power - and their limitations.

**Key Question:** Why do we need non-linear activation functions?

---

## Topics

### Topic 03: Activation Functions

**Key Concept:** Activation functions add non-linearity, enabling complex pattern learning.

| Function | Formula | Range | Use Case |
|----------|---------|-------|----------|
| Sigmoid | 1/(1+e^-z) | (0,1) | Output probabilities |
| ReLU | max(0,z) | [0,inf) | Hidden layers (modern) |
| Tanh | (e^z-e^-z)/(e^z+e^-z) | (-1,1) | Zero-centered outputs |

**Why non-linearity matters:**
Without activation functions, stacking layers just produces another linear function. Non-linearity allows networks to approximate any continuous function.

---

### Topic 04: Linear Limitation (XOR Problem)

**Key Concept:** A single neuron can only create linear decision boundaries.

**XOR Truth Table:**
| x1 | x2 | Output |
|----|----|----|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

**Problem:** Class 1 points (0,1) and (1,0) are diagonal to Class 0 points. No single line separates them.

**Solution:** Use hidden layers. Two neurons can create two lines whose intersection solves XOR.

---

### Topic 14: Sigmoid Saturation

**Key Concept:** Sigmoid gradients vanish at extreme values, slowing learning.

**Saturation Zones:**
- z < -3: sigmoid approaches 0, gradient near 0
- z > +3: sigmoid approaches 1, gradient near 0
- Maximum gradient: 0.25 (at z=0)

**Impact:** In deep networks, small gradients multiply, causing vanishing gradients. Early layers barely learn.

**Solution:** Use ReLU (gradient = 1 for positive inputs).

---

### Topic 15: Boundary Evolution

**Key Concept:** More neurons = more flexible decision boundaries.

| Hidden Neurons | Boundary Shape | Accuracy |
|---------------|----------------|----------|
| 1 | Straight line | ~50% (XOR fails) |
| 2 | Piecewise linear | Better |
| 4 | Multiple bends | Good |
| 10 | Smooth curves | ~100% on XOR |

**Universal Approximation Theorem:** A single hidden layer with enough neurons can approximate any continuous function.

**Caution:** More neurons also increases overfitting risk.

---

## Discussion Questions

1. Name a business metric that shows "diminishing returns" similar to sigmoid saturation.

2. Why might ReLU's "dead zone" (gradient=0 for negative inputs) be both a problem and a feature?

3. If you could visualize the decision boundary of a successful trading algorithm, what shape would you expect?

---

## Summary

| Topic | Key Takeaway |
|-------|--------------|
| 03 | Non-linear activations enable complex patterns |
| 04 | Single neuron = linear boundary (XOR fails) |
| 14 | Sigmoid saturates; ReLU solves vanishing gradients |
| 15 | More neurons = more expressive power |

**Next:** [[Part 3: Architecture|Part-3-Architecture]] - Building multi-layer networks
