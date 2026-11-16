# The Oracle's Weight

| | |
|---|---|
| **Section** | wave 5 |
| **Category** | reverse engineering |
| **Solves** | 116 |

## Overview

The oracle is an ONNX neural network that accepts an 8-element vector in `[0,1]` and returns a scalar near 1 only for the team's 8-byte key, normalized by dividing each byte by 255.

## Solve

The model is a three-layer MLP, `8 → 64 → 64 → 1`, with LeakyReLU (slope 0.1) on both hidden layers. I reimplemented the forward pass in NumPy, derived the analytic gradient, and ran Adam gradient ascent on the input, clipping to `[0,1]`.

Thirty random seeds were optimized for 3000 steps; the best continuous result was rounded to bytes and refined with a ±1 grid search over all eight components. The best input scored `0.9605`, above the required 0.75. The challenge asks for the 16 lowercase hex characters of the resulting 8 bytes.

The submitted flag was `████████████████` and it was accepted.
