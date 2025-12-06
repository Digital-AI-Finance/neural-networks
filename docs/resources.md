---
layout: page
title: Resources
---

![Loss Landscape]({{ site.baseurl }}/assets/images/loss_landscape.png){: style="float: right; max-width: 180px; margin-left: 15px;"}

## Topic PDFs (Extended - 10 slides each)

Download individual topic presentations with full content (Learning Goal, Key Concept, Formulas, Practice Problems, Takeaways):

| Part 1: Foundations | Part 2: Building Blocks | Part 3: Architecture | Part 4: Learning | Part 5: Application |
|---------------------|-------------------------|----------------------|------------------|---------------------|
| [01. Biological Neuron](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_01_extended.pdf) | [05. Activation Functions](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_05_extended.pdf) | [09. Network Architecture](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_09_extended.pdf) | [13. Loss Landscape](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_13_extended.pdf) | [17. Market Data](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_17_extended.pdf) |
| [02. Single Neuron](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_02_extended.pdf) | [06. Linear Limitation](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_06_extended.pdf) | [10. Forward Propagation](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_10_extended.pdf) | [14. Gradient Descent](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_14_extended.pdf) | [18. Prediction Results](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_18_extended.pdf) |
| [03. Problem Visualization](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_03_extended.pdf) | [07. Sigmoid Saturation](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_07_extended.pdf) | [11. Decision Boundary](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_11_extended.pdf) | [15. Overfitting](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_15_extended.pdf) | [19. Confusion Matrix](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_19_extended.pdf) |
| [04. Neuron Decision Maker](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_04_extended.pdf) | [08. Boundary Evolution](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_08_extended.pdf) | [12. Feature Hierarchy](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_12_extended.pdf) | [16. Learning Rate](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_16_extended.pdf) | [20. Trading Backtest](https://github.com/Digital-AI-Finance/neural-networks/raw/main/topic_pdfs/topic_20_extended.pdf) |

[Download Complete Presentation (PDF)](https://github.com/Digital-AI-Finance/neural-networks/raw/main/20251128_0825_quantlet_branding.pdf)

---

## Books

### Introductory
- **"Neural Networks and Deep Learning"** by Michael Nielsen - Free online book with interactive visualizations
- **"Deep Learning"** by Goodfellow, Bengio, Courville - Comprehensive textbook (free online)
- **"Hands-On Machine Learning"** by Aurelien Geron - Practical approach with code examples

### Finance Applications
- **"Advances in Financial Machine Learning"** by Marcos Lopez de Prado - Practical ML for finance
- **"Machine Learning for Asset Managers"** by Marcos Lopez de Prado - Focused on portfolio management
- **"Deep Learning for Finance"** by Jannes Klaas - Neural networks in financial applications

---

## Online Courses

### Free
- **3Blue1Brown Neural Networks** - Excellent visual explanations on YouTube
- **Stanford CS229** - Machine learning course materials online
- **Fast.ai** - Practical deep learning for coders

### Paid/Certificate
- **Coursera: Deep Learning Specialization** by Andrew Ng
- **Coursera: Machine Learning for Trading** by Georgia Tech
- **edX: Principles of Machine Learning** by Microsoft

---

## Tools and Libraries

### Python Libraries
- **NumPy** - Numerical computing foundation
- **scikit-learn** - Classic machine learning, including MLPClassifier
- **TensorFlow/Keras** - Industry-standard deep learning
- **PyTorch** - Research-focused deep learning

### Visualization
- **Matplotlib** - Python plotting library
- **TensorBoard** - Training visualization for TensorFlow
- **Weights & Biases** - Experiment tracking

### Financial Data
- **yfinance** - Yahoo Finance data API
- **Alpha Vantage** - Stock data API
- **Quandl** - Financial and economic data

---

![Trading Backtest]({{ site.baseurl }}/assets/images/trading_backtest.png){: style="float: right; max-width: 180px; margin-left: 15px;"}

## Interactive Tools

### Neural Network Playgrounds
- **TensorFlow Playground** (playground.tensorflow.org) - Visualize neural network training
- **ConvNetJS** - Neural network demo in browser
- **NN-SVG** - Draw neural network diagrams

### Mathematics
- **Desmos** - Graphing calculator for activation functions
- **WolframAlpha** - Compute derivatives and integrals

---

## Key Formulas Reference

### Activation Functions

| Function | Formula | Range | Derivative Max |
|----------|---------|-------|----------------|
| Sigmoid | 1/(1+e^-z) | (0,1) | 0.25 |
| ReLU | max(0,z) | [0,inf) | 1 |
| Tanh | (e^z-e^-z)/(e^z+e^-z) | (-1,1) | 1 |

### Training

| Concept | Formula |
|---------|---------|
| Weighted sum | z = Wx + b |
| Gradient descent | w := w - eta * dL/dw |
| Binary cross-entropy | L = -[y*log(p) + (1-y)*log(1-p)] |

### Evaluation

| Metric | Formula |
|--------|---------|
| Accuracy | (TP+TN)/(TP+TN+FP+FN) |
| Precision | TP/(TP+FP) |
| Recall | TP/(TP+FN) |
| F1 Score | 2*Precision*Recall/(Precision+Recall) |

---

## Glossary of Terms

| Term | Definition |
|------|------------|
| Activation function | Non-linear transformation applied after weighted sum |
| Backpropagation | Algorithm to compute gradients for all weights |
| Batch | Subset of training data used in one update |
| Bias | Learnable offset term in neuron computation |
| Cross-entropy | Loss function for classification |
| Epoch | One complete pass through training data |
| Gradient | Derivative indicating direction of steepest increase |
| Hidden layer | Layer between input and output |
| Learning rate | Step size for gradient descent |
| Loss | Measure of prediction error |
| Neuron | Basic computational unit |
| Overfitting | Memorizing training data, poor generalization |
| ReLU | Rectified Linear Unit activation |
| Sigmoid | S-shaped activation mapping to (0,1) |
| Softmax | Multi-class probability output |
| Underfitting | Model too simple to capture patterns |
| Weight | Learnable parameter controlling input influence |

---

## Getting Help

- **GitHub Issues**: [Report problems or ask questions](https://github.com/Digital-AI-Finance/neural-networks/issues)
- **Stack Overflow**: Tag questions with [neural-network] and [machine-learning]
- **Reddit**: r/learnmachinelearning, r/MachineLearning

---

## Attribution

This course material is provided by [Digital-AI-Finance](https://github.com/Digital-AI-Finance) under the MIT License.

All charts and visualizations are original works created with matplotlib.
