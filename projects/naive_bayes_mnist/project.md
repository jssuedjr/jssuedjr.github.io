
---
title: "Handwritten Digit Recognition with Bernoulli Naive Bayes"
date: 2024-12-13
summary: "Implemented a Bernoulli Naive Bayes classifier from scratch for handwritten digit recognition, achieving 84.16% test accuracy on MNIST and developing an interactive application for classifying user-drawn digits."
thumbnail: "images/thumbnail.png"
tools:
  - Python
  - NumPy
  - scikit-learn
  - Pygame
  - Matplotlib
paper_title: "CIS662 Final Project: Naive Bayes Digit Classifier"
pdf: "papers/paper.pdf"
thumbnail: "thumbnail/naive.png"
---

## Overview

This project was completed for CIS662 in December 2024. Its objective was to develop a probabilistic classifier capable of recognizing handwritten digits from the MNIST dataset and classifying new digits drawn by users in an interactive application.

I implemented a **Bernoulli Naive Bayes classifier from scratch** using Python and NumPy, trained it on the MNIST dataset, and developed a Pygame application that allows users to draw digits and receive predictions from the trained model.

The project explored Bayesian classification, conditional independence assumptions, numerical computation of likelihoods, and the challenges of applying a statistical model to data collected under different conditions.

## GitHub Repository

[View the source code on GitHub](https://github.com/jssuedjr/CIS662_finalproject)

## What I Did

### Bernoulli Naive Bayes Implementation

I implemented a Naive Bayes classifier using a Bernoulli observation model, representing each pixel as a binary random variable.

The classifier was trained using the MNIST dataset, consisting of 60,000 training images and 10,000 testing images, each with a resolution of 28 × 28 pixels.

I estimated the class-conditional probability of each pixel being active for each digit class and used a uniform prior over the ten possible digits.

The implementation also incorporated additive smoothing to avoid zero-valued probability estimates.

### Interactive Handwritten Digit Recognition

In addition to evaluating the classifier on MNIST, I developed an interactive drawing application using Pygame.

The application allows users to draw handwritten digits with their mouse, clear the canvas, and request a prediction from the trained classifier.

Because the drawing canvas had a different resolution from MNIST, I implemented a preprocessing procedure to transform user-drawn images into binary 28 × 28 representations.

This component allowed me to investigate how the classifier generalized beyond the original MNIST test dataset.

## Mathematical Approach

### Bayesian Classification

Let $C_k$ denote the class corresponding to digit $k$, and let $I=(x_1,\ldots,x_n)$ denote a binarized image containing $n=784$ pixels.

Using Bayes' theorem, the posterior probability of a digit class is

$$
P(C_k\mid I)
=
\frac{P(I\mid C_k)P(C_k)}{P(I)}.
$$

Under the Naive Bayes conditional independence assumption, the likelihood factors into individual pixel probabilities:

$$
P(I\mid C_k)
=
\prod_{i=1}^{n}P(x_i\mid C_k).
$$

For Bernoulli-distributed pixels, define

$$
\theta_{ki}=P(x_i=1\mid C_k).
$$

Then the class-conditional likelihood is

$$
P(I\mid C_k)
=
\prod_{i=1}^{n}
\theta_{ki}^{x_i}
(1-\theta_{ki})^{1-x_i}.
$$

I used a uniform class prior,

$$
P(C_k)=\frac{1}{10},
$$

and estimated the Bernoulli parameters from the training images belonging to each digit class.

### Log-Likelihood Computation

Directly multiplying hundreds of pixel probabilities can lead to numerical underflow. To address this, I performed classification using log-probabilities.

The predicted class is

$$
\hat{C}(I)
=
\argmax_{C_k}
\left[
\log P(C_k)
+
\sum_{i=1}^{784}
\left(
x_i\log\theta_{ki}
+
(1-x_i)\log(1-\theta_{ki})
\right)
\right].
$$

This formulation converts products into sums and can be implemented efficiently using NumPy matrix operations.

### Image Preprocessing

The MNIST images were binarized to make their pixel representations compatible with the binary observation model and the user-drawing application.

For new user-drawn inputs, I implemented a block-based downsampling procedure to transform the larger drawing canvas into a 28 × 28 binary image.

The resulting image was flattened into a vector and passed to the trained classifier.

## Results

The model achieved the following performance on the MNIST dataset:

| Dataset | Classification Accuracy |
|---|---|
| Training set | 83.15% |
| Testing set | 84.16% |

I evaluated classification performance using scikit-learn metrics, including a classification report and confusion matrix.

The results showed that the classifier correctly identified a substantial proportion of handwritten digits, although performance varied between classes.

In particular, the model encountered difficulties distinguishing certain digits, including 4, 5, and 9.

Performance on newly drawn digits was considerably less reliable than performance on the MNIST test set. This suggested that the preprocessing pipeline and differences between the training and application data distributions were important limitations.

## Limitations and Discussion

Several limitations became apparent during the project.

**Conditional independence assumption:** Naive Bayes assumes that pixel values are conditionally independent given the digit class. In handwritten images, neighboring pixels are spatially correlated, so this assumption is generally violated.

**Information loss from binarization:** Converting grayscale MNIST images into binary representations removes intensity information that may be useful for classification.

**Preprocessing of user-drawn inputs:** Resizing and binarizing drawings from the Pygame canvas can change digit shapes and produce inputs that differ substantially from the MNIST training distribution.

**Generalization:** Although the model achieved reasonable performance on the MNIST test set, its accuracy on new user-drawn inputs was lower. This highlighted the importance of considering how data collection and preprocessing affect the deployment of statistical models.

## Future Improvements

Possible extensions of this project include:

- Improving the preprocessing pipeline for user-drawn digits, particularly resizing, centering, and preserving digit geometry.
- Comparing Bernoulli Naive Bayes with alternative observation models, such as Gaussian Naive Bayes.
- Investigating the effect of different class priors and smoothing parameters.
- Performing a more systematic evaluation of performance on user-generated digits.
- Comparing the probabilistic classifier with models that can capture spatial relationships between pixels.

## Conclusion

This project provided practical experience implementing a probabilistic machine learning model, deriving its prediction rule from Bayesian principles, and evaluating its performance on both benchmark data and user-generated inputs.

It also demonstrated how assumptions that simplify statistical inference, particularly conditional independence, can limit predictive performance when applied to structured data such as images.
