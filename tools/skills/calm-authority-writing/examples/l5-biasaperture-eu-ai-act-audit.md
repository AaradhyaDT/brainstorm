# BiasAperture Diagnostic Audit Template

This template is for a research diagnostic report. It is not a conformity assessment, legal opinion, or claim of regulatory compliance. Populate it from a current run and cite each generated artifact.

## Run provenance

- Run identifier and timestamp: [value]
- Dataset/version and split: [value]
- Model artifact/hash and interface: [value]
- Prediction file and row count: [path and count]
- Code revision and configuration: [SHA and paths]

## Metric results

| Metric | Definition/version | Cohort n | Estimate | Significance test | 95% CI method, B | Evidence |
|---|---|---:|---:|---|---|---|
| [metric] | [definition] | [n] | [value / suppressed] | [test and p] | [method and resamples] | [artifact] |

Suppress scored values for groups below the configured minimum sample size. Report the method and actual resample budget used for each metric path; do not transfer guarantees from a separate function or backend. Label unavailable intervals as unavailable.

## Interpretation and limits

Describe surrogate attribution only as associations learned from demographic labels and inputs. Do not present it as image-level SHAP, causal attribution, or a decomposition of disparity. UTKFace is outside the current project scope; verify dataset lineage and subgroup totals before interpretation.

## Regulatory context

List relevant framework provisions as contextual references with source and date. Do not translate technical metric outputs into a pass/fail compliance conclusion. Seek qualified legal review for legal interpretations.
