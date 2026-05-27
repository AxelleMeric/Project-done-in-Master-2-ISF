# Deep Reinforcement Learning for Atari BasicMath: A Comparative Study

## 📌 Project Overview
This repository contains the codebase and research report for a comprehensive comparative analysis of Deep Reinforcement Learning (DRL) algorithms applied to the `Atari BasicMath-v5` environment. 

The primary objective was to evaluate whether standard Deep RL architectures could bridge the gap between simple spatial navigation and cognitive mathematical reasoning by extracting logic purely from the console's 128-byte RAM state.

## 🧠 Algorithms Implemented
I implemented and heavily optimized three distinct agents from scratch using PyTorch:
- **Deep Q-Network (DQN)** - *Off-Policy Temporal Difference*
- **Deep SARSA** - *On-Policy Temporal Difference*
- **Deep Monte Carlo** - *On-Policy Episodic*

**Optimizations include:** Frame Skipping, Reward Shaping (Action Penalties), and epsilon-greedy decay scheduling.

## 📊 Key Findings
Through extensive training and methodical root-cause analysis (Live Visual Diagnostics, Penalty Ablation Studies, and Forced-Action Mechanisms), this study highlights:
1. **The "Fear of FIRE" Phenomenon:** Standard TD/MC methods developed severe risk-averse policies (policy collapse), exploiting time-limit truncations to avoid action penalties rather than solving the math equations.
2. **The Curse of Dimensionality:** The empirical evidence strongly suggests that standard Multi-Layer Perceptrons (MLPs) are fundamentally incapable of extracting semantic logic purely from highly non-linear 128-byte RAM integer arrays.

*For full graphical analysis and methodology, please refer to the attached PDF Research Report (`MERIC.pdf`).*

## 📂 Repository Structure
- `MERIC.ipynb`: Main Jupyter Notebook containing the source code, training loops, and visualizations.
- `MERIC.pdf`: The final two-column academic research paper detailing the methodology and conclusions.
- **Data Logs (.json):**
  - `overnight_results.json`: Reward and action tracking for the baseline comparative analysis.
  - `penalty_hyp.json`: Data for the penalty ablation study.
  - `forced-MC_0.01.json`: Data for the forced-action diagnostic test.
- **Trained Models (.pth):**
  - `DQN_basicmath_2000.pth`: Weights for the Deep Q-Network.
  - `MonteCarlo_basicmath_1500.pth`: Weights for the baseline MC agent.
  - `0.0_penalty_hyp_800.pth` & `-0.01_penalty_hyp_800.pth`: Weights from the penalty ablation study.
  - `forced-MC_0.01.pth`: Weights from the forced FIRE experiment.

## 🚀 How to Run
To review the findings, simply open `MERIC.ipynb`. The notebook is structured to run analysis on the provided `.json` logs and `.pth` models, allowing instant visualization without needing to rerun the computationally expensive training loops (which took several hours).