# SPARK Interface Specification Template

This is a planning template, not a description of implemented firmware. Replace bracketed fields only from current design records or measured evidence.

## Status and scope

- Status: [proposal / implemented / bench-verified]
- Evidence reference and date: [path or record]
- In scope: [specific interface boundary]
- Out of scope: [unimplemented transport, sensor, model, or deployment work]

## Data contract

| Field | Value | Evidence status |
|---|---|---|
| Sampling rate | [value and unit] | [target / measured] |
| Window length | [samples and duration] | [target / measured] |
| Channels and order | [list] | [specified / verified] |
| Encoding and units | [format] | [specified / verified] |
| Transport | [name or not implemented] | [status] |

Document timing, buffering, and failure behavior as requirements until a trace demonstrates them. SPARK's thesis convention currently documents 100 Hz and 200 samples over 2 seconds; do not substitute the planned 200 Hz logger target as implemented behavior.

## Verification plan

Name the test fixture, captured artifact, acceptance threshold, and failure response. Do not include firmware snippets as runnable code unless they were compiled against the current repository.
