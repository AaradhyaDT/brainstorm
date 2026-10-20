# Evidence-Labelled SPARK Issue and Portfolio Patterns

These are patterns only. The bracketed fields must be filled from current SPARK repository evidence; targets must be labelled as targets.

## Issue pattern

```markdown
### Summary
[Observed behavior and evidence reference, or clearly labelled hypothesis.]

### Constraints and target
- Current behavior: [source path / trace / unknown]
- Desired behavior: [measurable target]
- Scope: [files and subsystem]

### Acceptance criteria
- [ ] [Implementation result]
- [ ] [Verification artifact and acceptance threshold]

### Non-goals
[Related behavior that this task does not implement.]
```

## Pull request pattern

```markdown
## Summary
[What changed, stated without claiming an unmeasured outcome.]

## Verification
[Exact command and observed result, or "not run". Link logs or artifacts.]

## Limitations
[Hardware, data, or integration work not covered by this change.]
```

## Portfolio pattern

Describe the thesis as a research prototype and separate offline evaluation from hardware validation. Do not claim on-device inference, sensor acquisition, telemetry, clinical validation, or performance unless current artifacts demonstrate each claim.
