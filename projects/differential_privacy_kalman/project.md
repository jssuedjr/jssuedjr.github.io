
---
title: "Differential Privacy and Kalman Filtering for IoT State Estimation"
date: 2026-05-01
summary: "Investigated the privacy–utility tradeoff in IoT sensor data using Laplace noise and Cubature Kalman filtering, comparing state estimation performance on synthetic and real-world datasets."
thumbnail: "thumbnail/graph.png"
tools:
  - Python
  - NumPy
  - Stone Soup
  - Matplotlib
paper_title: "Accurate and Private Device State Monitoring with Kalman Filters"
pdf: "papers/paper.pdf"
presentation_title: "CIS600 IoT Project Presentation"
presentation_preview: "presentations/presentation.pdf"
---

## Overview

This project was completed as part of CIS600 at Syracuse University, in collaboration with Alex Duly and Mia Kerchen.

The objective was to investigate whether **Kalman filtering could improve the utility of sensor data perturbed by local differential privacy (LDP)**, while preserving the motivation for privacy protection at the source.

In Internet of Things (IoT) systems, sensors continuously collect and transmit measurements that may contain sensitive information. Local differential privacy aims to protect these measurements by adding noise before transmission. However, this introduces a tradeoff: increasing the amount of privacy noise can reduce the usefulness of the measurements for downstream applications.

We investigated whether a **Cubature Kalman Filter (CKF)** could estimate the original states of a nonlinear system from measurements perturbed by Laplace noise.

The project involved simulation, probabilistic state estimation, experimental evaluation, and analysis of the privacy–utility tradeoff using synthetic and real-world industrial IoT data.

## GitHub Repository

[View the source code on GitHub](https://github.com/jssuedjr/CIS600IoTProject)

## What We Did

### IoT State Estimation Simulation

We developed a simulation representing an industrial IoT monitoring system with four state variables:

- Temperature
- Pressure
- Humidity
- Oxygen level

The system state at time $t$ was represented as

$$
x_t =
\begin{bmatrix}
T_t & P_t & H_t & O_{2,t}
\end{bmatrix}^{\top}.
$$

We used the Stone Soup Python library to configure a Cubature Kalman Filter for estimating these states from noisy sensor measurements.

The simulation incorporated a nonlinear transition model, process uncertainty, measurement uncertainty, and intermittent sensor observations.

### Differential Privacy Noise

We simulated local differential privacy by adding Laplace-distributed noise to individual sensor measurements before they were processed by the filter.

The noise magnitude was controlled using a parameter $\varepsilon$, with smaller values corresponding to larger noise scales in our experiments.

We investigated three settings:

$$
\varepsilon \in \{0.5,\ 2.0,\ 4.0\}.
$$

These settings allowed us to examine how changing the amount of injected noise affected the filter's estimation accuracy.

### Synthetic and Real-World Data

We evaluated the system using two types of data.

**Synthetic data:** We generated nonlinear state trajectories with statistical correlations between variables, introduced through the process-noise covariance matrix.

**Real-world data:** We used a subset of the *Smart Manufacturing IoT-Cloud Monitoring Dataset*, containing industrial process measurements.

Because the real-world dataset did not include oxygen measurements, we generated an additional oxygen state for the experiments.

We compared the filter's estimates with the original, unperturbed data using error metrics and visualizations.

## Mathematical Approach

### Local Differential Privacy Mechanism

Let $x_t$ represent the underlying system state and let $z_t$ represent the sensor measurement before privacy perturbation.

We modeled the privacy-perturbed measurement as

$$
z_t^{\mathrm{DP}} = z_t + \eta_t,
$$

where $\eta_t$ represents independently generated Laplace noise.

For a scalar Laplace random variable,

$$
\eta \sim \operatorname{Laplace}(0,b),
$$

the variance is

$$
\operatorname{Var}(\eta)=2b^2.
$$

In our experiments, the noise scale was chosen as

$$
b=\frac{1}{\varepsilon}.
$$

Consequently, the additional variance associated with each perturbed measurement was

$$
\sigma_{\mathrm{DP}}^2=\frac{2}{\varepsilon^2}.
$$

This gave us a controlled way to vary the magnitude of privacy noise.

The experiments were intended to investigate a local differential privacy mechanism, but a formal audit of the achieved privacy guarantees was outside the scope of the project.

### Cubature Kalman Filtering

We used a Cubature Kalman Filter to estimate the system states from noisy measurements.

The state-space formulation can be represented as

$$
x_{t+1}=f(x_t)+w_t,
$$

$$
z_t=h(x_t)+v_t,
$$

where:

- $f$ represents the state transition model.
- $h$ represents the measurement model.
- $w_t$ represents process noise.
- $v_t$ represents measurement noise.

The CKF uses numerical integration based on cubature points to approximate the moments required for nonlinear Bayesian state estimation.

A central consideration was how to account for the additional uncertainty introduced by the privacy mechanism.

We modified the measurement-noise covariance used by the filter:

$$
R_{\mathrm{eff}}=R+R_{\mathrm{DP}},
$$

where $R$ is the original measurement-noise covariance and $R_{\mathrm{DP}}$ represents the additional covariance associated with Laplace perturbations.

For the four-state system with equal privacy-noise scales, we used

$$
R_{\mathrm{DP}}
=
\frac{2}{\varepsilon^2}I_4.
$$

This allowed the filter to account for the increased measurement uncertainty.

However, the CKF's Gaussian approximation does not exactly represent Laplace-distributed measurement noise. This approximation was an important limitation of the approach.

### Experimental Evaluation

We evaluated estimation accuracy by comparing the CKF estimates $\hat{x}_t$ with the unperturbed states $x_t$.

For each state variable, the root mean squared error was calculated as

$$
\operatorname{RMSE}
=
\sqrt{
\frac{1}{N}
\sum_{t=1}^{N}
(x_t-\hat{x}_t)^2
}.
$$

We also examined moving-average behavior to assess how well the filter preserved trends in the underlying data.

The experimental procedure was:

1. Generate synthetic data or preprocess the real-world dataset.
2. Simulate sensor measurements.
3. Add Laplace-distributed privacy noise.
4. Run the Cubature Kalman Filter.
5. Compare estimated states with the original data.
6. Repeat the experiment for different values of $\varepsilon$.

## Results

### Synthetic Data

The CKF generally performed well on the synthetic dataset when the privacy noise was relatively small.

For example, with $\varepsilon=4.0$, the reported RMSE values were:

| State Variable | RMSE |
|---|---:|
| Temperature | 1.7928 |
| Pressure | 2.1849 |
| Humidity | 2.2898 |
| Oxygen | 0.6751 |

As the privacy-noise scale increased, estimation generally became less accurate.

At $\varepsilon=0.5$, the RMSE values increased to:

| State Variable | RMSE |
|---|---:|
| Temperature | 3.2123 |
| Pressure | 3.6262 |
| Humidity | 3.0387 |
| Oxygen | 4.9376 |

These results suggested that the filter could partially recover the underlying synthetic states despite privacy perturbations, but its performance deteriorated as the amount of injected noise increased.

### Real-World Data

The results using real-world industrial data were substantially less successful.

The CKF often produced estimates that were overly smooth or poorly matched to the underlying measurements.

An important reason was **model mismatch**: the filter used the same assumed transition model developed for the synthetic data, even though the real-world measurements followed different dynamics.

The real-world experiments also included a synthetically generated oxygen variable because the dataset did not provide oxygen readings.

These limitations made the real-world results less reliable and highlighted the importance of choosing an appropriate dynamical model.

### Main Findings

The experiments illustrated several important observations:

- Kalman filtering can reduce the impact of added measurement noise when the assumed system dynamics are sufficiently accurate.
- Increasing the amount of privacy noise generally makes state estimation more difficult.
- Estimation performance depends strongly on the accuracy of the assumed transition and measurement models.
- A filter that performs well on synthetic data may generalize poorly to real-world measurements.
- Gaussian approximations of non-Gaussian privacy noise introduce additional modeling limitations.

Our experiments were limited in scope and did not establish a formal differential privacy guarantee or demonstrate universally improved performance.

## Limitations and Discussion

### Privacy Guarantees

Although we simulated a Laplace-based local differential privacy mechanism, the project did not formally audit the privacy guarantees of the complete system.

The relationship between the privacy parameter, measurement sensitivity, and the resulting privacy guarantees requires careful consideration.

Furthermore, reconstructing individual measurements from privacy-perturbed observations raises important questions about the relationship between statistical estimation and the intended privacy protection.

### Model Mismatch

The synthetic experiments benefited from using an assumed transition model closely related to the model that generated the data.

The real-world experiments did not have this advantage.

This demonstrated the importance of accurately modeling system dynamics when applying Bayesian state estimation to unfamiliar data.

### Non-Gaussian Noise

The CKF was configured using a Gaussian approximation to the Laplace noise introduced by the privacy mechanism.

Although the covariance could be adjusted to account for the additional uncertainty, the underlying noise distribution was not Gaussian.

More robust filtering methods may be better suited to such settings.

### Experimental Scope

The project was conducted entirely through simulation and did not include a physical IoT sensor network.

Additional experiments, repeated simulation trials, and more extensive model calibration would be necessary to make stronger conclusions about practical deployment.

## Future Directions

Potential extensions of this work include:

- Investigating robust Bayesian filters that explicitly accommodate non-Gaussian measurement noise.
- Developing transition models calibrated to the dynamics of real-world IoT measurements.
- Conducting repeated Monte Carlo experiments to quantify the variability of estimation performance.
- Studying the relationship between formal differential privacy guarantees and sequential state estimation.
- Comparing CKF estimates against alternative filtering and smoothing methods.
- Implementing a physical IoT sensor network to investigate communication loss, sensor reliability, and real-time computational constraints.

## Conclusion

This project explored the interaction between **differential privacy and Bayesian state estimation** in an industrial IoT setting.

The synthetic experiments demonstrated that a Cubature Kalman Filter could partially reconstruct underlying system states from measurements perturbed by Laplace noise. However, the less successful real-world experiments highlighted the sensitivity of filtering methods to model mismatch and the challenges of applying theoretical assumptions to real data.

The project provided experience with nonlinear filtering, probabilistic modeling, numerical simulation, and experimental evaluation, while motivating further questions about the relationship between privacy, uncertainty, and statistical estimation.

## Collaborators

- Alex Duly
- Mia Kerchen
- Jaime Sued
