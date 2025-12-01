# Glossary

[Back to Home](Home)

A comprehensive list of key terms used throughout this course.

---

## A

**Accuracy**
The proportion of correct predictions out of total predictions.
Formula: (TP + TN) / (TP + TN + FP + FN)

**Activation Function**
A non-linear function applied to the weighted sum of a neuron's inputs. Common types: sigmoid, ReLU, tanh. Essential for enabling networks to learn complex patterns.

**Adam**
An adaptive learning rate optimization algorithm that combines momentum and RMSprop. Adjusts learning rate per-parameter automatically.

**Axon**
In biological neurons, the long fiber that transmits output signals to other neurons. Analogous to the output of an artificial neuron.

---

## B

**Backpropagation**
Algorithm for computing gradients of the loss function with respect to all weights in a network. Uses the chain rule to propagate error backward through layers.

**Batch**
A subset of training data used to compute one gradient update. Smaller batches are noisier but faster; larger batches are more accurate but slower.

**Bias**
A learnable parameter added to the weighted sum before activation. Allows the neuron to shift its activation threshold.

**Binary Classification**
Prediction task with two possible outcomes (e.g., UP/DOWN, spam/not-spam).

**Buy-and-Hold**
Benchmark investment strategy: buy an asset and hold it regardless of market movements.

---

## C

**Confusion Matrix**
A table showing the four possible outcomes of binary classification: True Positives, False Positives, True Negatives, False Negatives.

**Convergence**
When training metrics (loss, accuracy) stabilize and stop improving significantly.

**Cross-Entropy Loss**
Loss function for classification: L = -[y*log(p) + (1-y)*log(1-p)]. Penalizes confident wrong predictions heavily.

---

## D

**Decision Boundary**
The surface in feature space where the classifier's prediction changes from one class to another.

**Deep Learning**
Machine learning using neural networks with multiple hidden layers. "Deep" refers to the many layers.

**Dendrites**
In biological neurons, the branching structures that receive signals from other neurons. Analogous to inputs in artificial neurons.

**Divergence**
When training fails and loss increases instead of decreasing, often due to learning rate too high.

---

## E

**Early Stopping**
Technique to prevent overfitting: stop training when validation loss starts increasing.

**Epoch**
One complete pass through the entire training dataset.

---

## F

**F1 Score**
Harmonic mean of precision and recall: 2 * (Precision * Recall) / (Precision + Recall). Balances both metrics.

**False Negative (FN)**
Predicted negative (DOWN/SELL) when actually positive (UP). A missed opportunity.

**False Positive (FP)**
Predicted positive (UP/BUY) when actually negative (DOWN). A wrong trade.

**Feature**
An input variable to the neural network (e.g., price, volume, sentiment).

**Feature Engineering**
The process of creating and transforming input features for better model performance.

**Forward Propagation**
Computing the network output by passing inputs through all layers sequentially.

---

## G

**Gradient**
The derivative of the loss function with respect to a weight. Indicates the direction and magnitude of steepest increase.

**Gradient Descent**
Optimization algorithm that updates weights in the opposite direction of the gradient to minimize loss.

---

## H

**Hidden Layer**
Any layer between input and output layers. Learns intermediate representations.

**Hyperparameter**
Parameters set before training begins (learning rate, number of layers, neurons per layer) vs parameters learned during training (weights, biases).

---

## L

**Learning Rate (eta)**
Controls the step size in gradient descent. Too small = slow; too large = unstable.

**Linear Boundary**
A straight line (2D) or hyperplane (higher dimensions) separating classes. Created by single neurons.

**Loss Function**
Measures how wrong predictions are. Training minimizes this function.

**Loss Landscape**
The surface created by plotting loss as a function of weights.

---

## M

**Maximum Drawdown**
The largest peak-to-trough decline in portfolio value during a period.

---

## N

**Neuron**
The basic computational unit in a neural network. Computes weighted sum of inputs, adds bias, and applies activation.

**Normalization**
Scaling features to similar ranges (e.g., 0-1 or mean=0, std=1) to prevent some features from dominating.

---

## O

**Overfitting**
When a model memorizes training data rather than learning generalizable patterns. Low training error, high test error.

---

## P

**Parameter**
A learnable value in the network (weights and biases).

**Precision**
When the model predicts positive, how often is it correct? TP / (TP + FP)

---

## R

**Recall**
Of all actual positive cases, how many did the model catch? TP / (TP + FN)

**ReLU (Rectified Linear Unit)**
Activation function: f(z) = max(0, z). Popular for hidden layers due to non-vanishing gradients.

---

## S

**Sharpe Ratio**
Risk-adjusted return: (mean return - risk-free rate) / standard deviation of returns.

**Sigmoid**
Activation function: f(z) = 1/(1+e^-z). Outputs in range (0,1), useful for probabilities.

**Soma**
In biological neurons, the cell body that integrates signals. Analogous to the summation in artificial neurons.

**Synapse**
In biological neurons, the connection between neurons with variable strength. Analogous to weights.

---

## T

**Tanh**
Activation function: f(z) = (e^z - e^-z)/(e^z + e^-z). Outputs in range (-1,1), zero-centered.

**True Negative (TN)**
Correctly predicted negative (DOWN/SELL when actually DOWN).

**True Positive (TP)**
Correctly predicted positive (UP/BUY when actually UP).

---

## U

**Underfitting**
When a model is too simple to capture patterns. High training and test error.

**Universal Approximation Theorem**
A single hidden layer with enough neurons can approximate any continuous function.

---

## V

**Vanishing Gradient**
When gradients become very small in deep networks, preventing early layers from learning. Caused by saturating activations like sigmoid.

---

## W

**Weight**
Learnable parameter that multiplies an input, determining its influence on the output.

---

## X

**XOR Problem**
Classic example of a non-linearly separable problem that single neurons cannot solve.

---

[Back to Home](Home)
