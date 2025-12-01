# Formula Reference

[Back to Home](Home)

Quick reference for all formulas used in this course.

---

## Neuron Computation

### Weighted Sum
```
z = w1*x1 + w2*x2 + ... + wn*xn + b
```
or in vector form:
```
z = W^T * x + b
```

### Full Neuron Output
```
y = f(z) = f(W^T * x + b)
```
where f is the activation function.

---

## Activation Functions

### Sigmoid
```
sigma(z) = 1 / (1 + e^(-z))

Range: (0, 1)
Derivative: sigma(z) * (1 - sigma(z))
Max derivative: 0.25 at z=0
```

### ReLU (Rectified Linear Unit)
```
ReLU(z) = max(0, z)

Range: [0, infinity)
Derivative: 1 if z > 0, else 0
```

### Tanh
```
tanh(z) = (e^z - e^(-z)) / (e^z + e^(-z))

Range: (-1, 1)
Derivative: 1 - tanh^2(z)
```

---

## Network Architecture

### Parameter Count (per layer)
```
Parameters = (inputs * outputs) + outputs
           = weights + biases
```

### Total Parameters
```
Total = Sum over all layers of [(n_prev * n_current) + n_current]
```

Example [10, 8, 6, 1]:
- Layer 1: (10 * 8) + 8 = 88
- Layer 2: (8 * 6) + 6 = 54
- Layer 3: (6 * 1) + 1 = 7
- Total: 149

---

## Forward Propagation

### Layer-by-layer
```
a^[0] = x                        (input)
z^[l] = W^[l] * a^[l-1] + b^[l]  (linear)
a^[l] = f(z^[l])                 (activation)
y_hat = a^[L]                    (output)
```

---

## Loss Functions

### Binary Cross-Entropy
```
L = -[y * log(y_hat) + (1-y) * log(1 - y_hat)]

Average over N samples:
L = -(1/N) * Sum[y_i * log(y_hat_i) + (1-y_i) * log(1 - y_hat_i)]
```

### Mean Squared Error
```
L = (1/N) * Sum[(y_i - y_hat_i)^2]
```

---

## Gradient Descent

### Weight Update
```
w_new = w_old - eta * (dL/dw)
```

### Bias Update
```
b_new = b_old - eta * (dL/db)
```

### Learning Rate Schedule (Exponential Decay)
```
eta_t = eta_0 * e^(-lambda * t)
```

---

## Normalization

### Min-Max Scaling
```
x_norm = (x - x_min) / (x_max - x_min)

Result range: [0, 1]
```

### Z-Score (Standardization)
```
x_norm = (x - mu) / sigma

Result: mean=0, std=1
```

---

## Evaluation Metrics

### Accuracy
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

### Precision
```
Precision = TP / (TP + FP)

"When I predict positive, how often am I right?"
```

### Recall (Sensitivity)
```
Recall = TP / (TP + FN)

"Of all actual positives, how many did I catch?"
```

### F1 Score
```
F1 = 2 * (Precision * Recall) / (Precision + Recall)

Harmonic mean of precision and recall
```

### Specificity
```
Specificity = TN / (TN + FP)

"Of all actual negatives, how many did I identify?"
```

---

## Financial Metrics

### Cumulative Return
```
R_total = Product(1 + r_t) - 1

where r_t is the return at time t
```

### Sharpe Ratio
```
Sharpe = (mean_return - risk_free_rate) / std_return
```

### Maximum Drawdown
```
MDD = max[(Peak_t - Value_t) / Peak_t]

Largest percentage drop from peak
```

### Recovery Factor
```
Recovery = Total_Return / Max_Drawdown
```

---

## Decision Rules

### Binary Classification (sigmoid output)
```
Prediction = 1 (UP/BUY) if y_hat > threshold
           = 0 (DOWN/SELL) if y_hat <= threshold

Default threshold: 0.5
```

### Decision Boundary (linear)
```
w1*x1 + w2*x2 + b = 0

Points where z = 0 and y_hat = 0.5
```

---

## Gradient Formulas (for reference)

### Sigmoid Gradient
```
d(sigma)/dz = sigma(z) * (1 - sigma(z))
```

### ReLU Gradient
```
d(ReLU)/dz = 1 if z > 0, else 0
```

### Cross-Entropy Gradient (w.r.t. output)
```
dL/d(y_hat) = -y/y_hat + (1-y)/(1-y_hat)
```

### Combined (sigmoid + cross-entropy)
```
dL/dz = y_hat - y

Elegant simplification!
```

---

[Back to Home](Home)
