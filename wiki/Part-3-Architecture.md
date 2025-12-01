# Part 3: Network Architecture

[Back to Home](Home)

## Overview

This part covers how to structure multi-layer networks and understand information flow from input to output.

**Key Question:** How do we organize neurons into effective networks?

---

## Topics

### Topic 05: Network Architecture

**Key Concept:** Networks have input, hidden, and output layers with learnable parameters.

**Example Architecture [5, 6, 1]:**
- Input layer: 5 features (price, volume, sentiment, volatility, interest rate)
- Hidden layer: 6 neurons
- Output layer: 1 neuron (probability of price increase)

**Parameter Count:**
```
Input to Hidden: 5 * 6 = 30 weights + 6 biases = 36
Hidden to Output: 6 * 1 = 6 weights + 1 bias = 7
Total: 43 parameters
```

**Rule of Thumb:** Keep parameters < training samples to avoid overfitting.

---

### Topic 06: Forward Propagation

**Key Concept:** Data flows forward through layers to produce predictions.

**Algorithm:**
1. Input features enter the network
2. Each layer computes: z = Wx + b, then a = f(z)
3. Output of one layer becomes input to next
4. Final layer produces prediction

**Example Computation:**
```
Input: x = [105.2, 0.75, 0.62]
Hidden: z1 = W1*x + b1, a1 = sigmoid(z1)
Output: z2 = W2*a1 + b2, y = sigmoid(z2)
Result: 0.742 (74.2% probability -> BUY)
```

---

### Topic 16: Feature Hierarchy

**Key Concept:** Layers learn increasingly abstract representations.

| Layer | What It Learns |
|-------|---------------|
| Input | Raw features (price, volume, sentiment) |
| Hidden 1 | Simple patterns (uptrend, volume spike) |
| Hidden 2 | Complex patterns (momentum + volume = bullish) |
| Output | Final decision (BUY 68%, SELL 32%) |

**Key Insight:** We don't program these representations - the network discovers them through training. This is the "representation learning" that makes deep learning powerful.

---

## Discussion Questions

1. For your industry, what would be the input features and output prediction for a useful neural network?

2. Why are hidden layer representations often not human-interpretable?

3. When would you use 2 hidden layers instead of 1?

---

## Summary

| Topic | Key Takeaway |
|-------|--------------|
| 05 | Count parameters: (inputs * outputs) + outputs per layer |
| 06 | Forward pass: layer-by-layer computation to prediction |
| 16 | Deeper layers learn more abstract concepts |

**Next:** [[Part 4: Learning Process|Part-4-Learning-Process]] - How networks learn from data
