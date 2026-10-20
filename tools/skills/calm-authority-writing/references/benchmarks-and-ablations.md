# Empirical Evaluations, Benchmarks & Ablation Reporting (Tier L4)

This reference defines reporting standards for benchmark evaluations, quantization studies, controlled ablations, and Pareto tradeoff analyses across embedded systems, robotics, and machine learning models.

---

## 1. Pinned Benchmark Comparison Grid Standard

Every empirical evaluation report must feature a standardized comparative hierarchy pinning the evaluated subject against established baselines:

1. **The Evaluated Subject (Pinned Column)**: Displayed first, bolded, and prominently styled.
2. **The Direct Predecessor or Unmitigated Baseline**: The previous version, unquantized model, or baseline control (*e.g. FP32 baseline, V6.8 firmware*).
3. **The Leading Alternative / Competitor**: The direct alternative in the same class (*e.g. GRU TinyML model, competitive controller*).
4. **The Frontier / Theoretical Reference**: The upper-bound reference (*e.g. Cloud ResNet-18, Ideal MATLAB simulation*), annotated: **"For reference"**.

### Standard Benchmark Schema:

| Architecture / System | Precision / Mode | Runtime Target | Memory / Footprint | Latency (ms) | Primary Metric | Secondary Metric |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **[Evaluated subject]** | [mode] | [device or offline] | [value / not measured] | [value / not measured] | [estimate and uncertainty] | [estimate and uncertainty] |
| [Controlled baseline] | [mode] | [device or offline] | [value / not measured] | [value / not measured] | [estimate and uncertainty] | [estimate and uncertainty] |
| [Alternative, if evaluated] | [mode] | [device or offline] | [value / not measured] | [value / not measured] | [estimate and uncertainty] | [estimate and uncertainty] |
| [Reference, clearly labelled] | [mode] | [device or offline] | [value / not measured] | [value / not measured] | [estimate and uncertainty] | [estimate and uncertainty] |

---

## 2. Mandatory Evaluation Qualifiers

Never report a bare evaluation percentage without its exact operational condition qualifier and evidence reference:
- `(INT8 quantized)` vs. `(FP32 baseline)`
- `(ESP-NN SIMD enabled)` vs. `(standard scalar math)`
- `(5-fold cross-validation)` vs. `(holdout test split)`
- `(offline evaluation)` vs. `(hardware-in-the-loop)`
- `not measured` or `not reported`: Indicates that the benchmark was un-run or un-reported. Never substitute an estimate or illustrative number without labelling it clearly.

---

## 3. Multi-Objective Tradeoff & Pareto Frontier Disclosure

System capabilities cannot be evaluated in isolation from computational, memory, or battery costs:

1. **Dual-Axis Tradeoffs**: Plot primary accuracy or sensitivity against operational cost (latency in ms, SRAM in KB, energy in mJ).
2. **Controlled Ablations**: When introducing an architectural fix (such as integrator bleed or differential ramping in robotics), report an ablation table showing outcomes with each component enabled and disabled.
3. **Compute Budget Curves**: If systems feature scalable effort parameters (`low`, `medium`, `high`, `max`), report accuracy and latency progression across each setting.
