# SPARK Model Evaluation Report Template

This template contains no measured benchmark results. The archived SPARK report describes offline evaluation; it does not establish on-device latency, power, memory, or clinical performance.

## Evaluation record

- Dataset and frozen split: [artifact path, counts, subject separation]
- Model artifact and hash: [path and SHA-256]
- Runtime and device: [offline environment or measured device]
- Input convention: [sampling rate, window length, channels]
- Evaluation date and command: [record]

## Results

| Variant | Evaluation location | Metric | Estimate | Evidence |
|---|---|---|---:|---|
| [FP32] | [offline / device] | [metric] | [value or not measured] | [artifact] |
| [INT8] | [offline / device] | [metric] | [value or not measured] | [artifact] |

Include confidence intervals or uncertainty where available. Keep offline predictive metrics separate from hardware measurements. Mark missing matching reports as unavailable; do not infer them from model size or simulation.

## Limitations and next measurement

State the cohort limits, threshold provenance, and any discrepancy between configuration and logs. A device benchmark requires a reproducible device, runtime, input, timing method, repeated trials, and raw trace.
