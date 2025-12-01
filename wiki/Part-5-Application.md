# Part 5: Application

[Back to Home](Home)

## Overview

This part applies neural networks to a real business problem: predicting stock price direction.

**Key Question:** Can neural networks provide value in financial prediction?

---

## Topics

### Topic 09: Market Prediction Data

**Key Concept:** Feature engineering prepares data for neural network input.

**Common Features:**
| Feature | Description | Normalization |
|---------|-------------|---------------|
| Price | Historical prices/returns | Min-max or z-score |
| Volume | Trading activity | Divide by average |
| Sentiment | News/social sentiment | Already 0-1 |
| Volatility | Price variability | Z-score |

**Data Leakage Warning:** Never use future information as features. Only use data available at prediction time.

**Target Variable:** Binary (1 = price went up, 0 = price went down)

---

### Topic 10: Prediction Results

**Key Concept:** Training transforms random guessing into informed prediction.

| Metric | Before Training | After Training |
|--------|----------------|----------------|
| Accuracy | ~50% (random) | ~70% |
| Improvement | - | +20 percentage points |

**Important:** Evaluate on held-out test data, not training data.

**Even modest improvement matters:** In finance, 55-60% accuracy can be highly profitable over many trades.

---

### Topic 19: Confusion Matrix

**Key Concept:** Break down predictions beyond simple accuracy.

**Four Outcomes:**
| | Predicted UP | Predicted DOWN |
|---|---|---|
| **Actually UP** | True Positive (TP) | False Negative (FN) |
| **Actually DOWN** | False Positive (FP) | True Negative (TN) |

**Key Metrics:**
```
Precision = TP / (TP + FP)  "When I say BUY, am I right?"
Recall = TP / (TP + FN)     "Do I catch all the UP days?"
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

**Business Context:** Different errors have different costs.
- False BUY (FP): Lose money on wrong trade
- Missed opportunity (FN): Foregone profit

---

### Topic 20: Trading Backtest

**Key Concept:** Simulate strategy performance on historical data.

**Comparison:**
- **Buy-and-hold**: Buy at start, hold throughout (benchmark)
- **NN Strategy**: Trade based on predictions (BUY when confidence > 50%)

**Key Metrics:**
```
Cumulative Return = Product of (1 + daily_return) - 1
Sharpe Ratio = Mean Return / Std Dev of Returns
Max Drawdown = Largest peak-to-trough decline
```

**Reality Check:** Transaction costs (0.1% per trade) can eliminate edge. 200 trades/year = 20% cost drag.

---

## Discussion Questions

1. What customer behavior in your industry would you want to predict? What features would you use?

2. Why might a model with 70% accuracy still lose money in trading?

3. How would you decide between a high-precision (fewer but more confident trades) vs high-recall (more trades, some wrong) strategy?

---

## Summary

| Topic | Key Takeaway |
|-------|--------------|
| 09 | Normalize features; avoid data leakage |
| 10 | Training improves beyond random baseline |
| 19 | Confusion matrix reveals error types |
| 20 | Backtest against benchmark with realistic costs |

---

## Course Conclusion

**What We Learned:**
1. Neural networks are inspired by biological neurons
2. Single neurons compute weighted sums with activation
3. Hidden layers enable non-linear decision boundaries
4. Networks learn through gradient descent optimization
5. Overfitting and learning rate are key challenges
6. Performance evaluation requires multiple metrics
7. Real-world application requires careful backtesting

**Next Steps:**
- Practice with the [Exercise Bank](https://digital-ai-finance.github.io/neural-networks/exercises.html)
- Explore the [GitHub Repository](https://github.com/Digital-AI-Finance/neural-networks) for code examples
- Check [Additional Resources](https://digital-ai-finance.github.io/neural-networks/resources.html) for further learning

**Thank you for completing this course!**
