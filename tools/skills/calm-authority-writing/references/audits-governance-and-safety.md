# Consolidated Empirical Audits, Governance & Safety Dossiers (Tier L5)

This reference consolidates formal system card architectures, algorithmic fairness evaluations, and regulatory safety disclosures modeled after the **Claude Haiku 5.5 System Card** (144 pages) and grounded in **BiasAperture** (`AaradhyaDT/BiasAperture`).

---

## 1. System Card & Technical Audit Hierarchy

Every formal system card, safety disclosure, or algorithmic audit must follow this 6-part hierarchy:

```
Section 1: Provenance, Dataset Governance & Methodology
Section 2: Statistical Sample Size Guards & Suppression Rules (n < 30)
Section 3: Headline Evaluation Metrics & Controlled Baselines
Section 4: Intersectional Subgroup Disparity Analysis
Section 5: Threat Modeling, Boundary Compliance & Failure Modes
Section 6: Actionable Conformity Checklists & Verification Commands
```

---

## 2. Statistical Reliability Invariants: $n < 30$ Sample Suppression

`[FORMALLY_PROVEN]` In accordance with central limit theorem bounds and statistical reliability standards:
- **Never display point estimates for cohorts where $n < 30$**. Small sample groups exhibit high variance that leads to noisy or misleading disparity claims.
- **Isolate suppressed cohorts** within collapsible `<details>` blocks tagged with `.badge-guard`:
  ```html
  <details class="insufficient-block">
    <summary><span class="badge-guard">INSUFFICIENT SAMPLE (n &lt; 30)</span> [Cohort Name] (n = 14)</summary>
    <p>Point metrics suppressed to prevent statistical distortion. Bootstrap 95% CI exceeds reliability thresholds.</p>
  </details>
  ```
- Calculate 95% bootstrap confidence intervals for all reported headline metrics.

---

## 3. Regulatory Alignment Standards

When authoring formal compliance dossiers (such as EU AI Act conformity or NIST AI RMF assessments):

1. **EU AI Act Article 10 (Data & Data Governance)**:
   - Audit training, validation, and testing datasets for historical biases.
   - Document mitigation strategies (e.g. re-weighting, threshold optimization via Fairlearn).
2. **NIST AI Risk Management Framework (AI RMF 1.0)**:
   - Map quantitative metrics to MAP 1.1 (identifying context) and MEASURE 2.3 (evaluating bias and fairness).
3. **Calibrated Regulatory Terminology**:
   - Strictly employ the calibrated vocabulary: *Harmonized, Standardized, Uniform, Interoperable, Cohesive*.

---

## 4. Threat Modeling & Boundary Enforcement

When documenting AI safety or agent execution boundaries:

1. **Sandbox Boundaries**: Explicitly test and report whether autonomous agents attempt unauthorized file access or out-of-bounds network probes.
2. **Refusal vs. Over-Refusal Curves**: Measure both the harmful request refusal rate and the false refusal rate on benign educational prompts.
3. **Grader Awareness**: Test whether the system alters behavior when evaluation harnesses or scoring rubrics are detected in the context window.
