# Part 4: Learning Process

[Back to Home](Home)

## Overview

This part explains how neural networks learn from data through gradient descent optimization.

**Key Question:** How do networks improve their predictions?

---

## Topics

### Topic 07: Loss Landscape

**Key Concept:** The loss function creates a surface we navigate to find optimal weights.

**Loss Function (Binary Cross-Entropy):**
```
L = -[y*log(p) + (1-y)*log(1-p)]
```

**Landscape Characteristics:**
- Higher altitude = higher error
- Global minimum = best possible weights
- Local minima = good but not optimal solutions
- Goal: Navigate to the lowest point

**Key Insight:** With millions of weights, the landscape exists in millions of dimensions - but the math is the same.

---

### Topic 08: Gradient Descent

**Key Concept:** We learn by iteratively stepping "downhill" on the loss surface.

**Update Rule:**
```
w_new = w_old - learning_rate * gradient
```

**Learning Rate Effects:**
| Rate | Result |
|------|--------|
| Too small (0.0001) | Very slow convergence |
| Just right (0.001-0.01) | Steady progress |
| Too large (1.0) | Overshoots, diverges |

**Signs of Good Training:**
- Loss decreases each epoch
- Diminishing improvements (approaching minimum)
- Training and validation loss converge

---

### Topic 17: Overfitting vs Underfitting

**Key Concept:** Diagnose training problems using learning curves.

| Problem | Training Loss | Validation Loss | Solution |
|---------|--------------|-----------------|----------|
| Underfitting | High | High | More capacity, train longer |
| Just Right | Low | Low (similar) | Keep this model |
| Overfitting | Very low | High (gap) | Regularize, more data |

**Early Stopping:** Stop training when validation loss starts increasing.

---

### Topic 18: Learning Rate Comparison

**Key Concept:** Learning rate is critical for successful training.

**Observable Patterns:**

*Too Small:*
- Loss decreases very slowly
- May never reach good solution in reasonable time

*Just Right:*
- Rapid early progress
- Gradual slowdown as minimum approaches
- Stable convergence

*Too Large:*
- Loss oscillates or increases
- May explode to NaN (overflow)
- Training fails completely

**Modern Solution:** Adaptive optimizers (Adam) adjust rate automatically.

---

## Discussion Questions

1. How is gradient descent like optimizing a business process? What would be the "loss function" for your business?

2. Why might starting training from different random weights lead to different final solutions?

3. In what situations would you prefer a simpler model that slightly underfits over a complex model with perfect training accuracy?

---

## Summary

| Topic | Key Takeaway |
|-------|--------------|
| 07 | Loss measures prediction error; we minimize it |
| 08 | Gradient descent: step opposite to gradient direction |
| 17 | Watch train vs validation gap to detect overfitting |
| 18 | Learning rate: too small = slow, too large = unstable |

**Next:** [[Part 5: Application|Part-5-Application]] - Putting it all together for market prediction
