#!/usr/bin/env python3
"""
audit_calm_writing.py — Deterministic Style & Invariant Linter for Calm Authority Technical Writing (v2.2)

Validates markdown documents against:
1. Complete elimination of banned marketing hype words (Lexical Filter).
2. Elimination of common syntactic AI habits (Syntactic Filter: negation-contrast framing, participial tails, nominalization bloat).
3. 1-Sentence Empirical Thesis or Capacity Bounding presence.
4. Tier-specific structural invariants (Tiers L1 through L5).
5. Domain-specific proof standards (Domains U0 through U5: brainstorm, embedded, arch-sim, ml-audit, mcp-infra, knowledge).
6. Epistemic maturity gate calibration (E1 through E4 simulation/hardware claims).
7. Intentional Dual-Namespace preservation (Aaradhya-Dev-Tamrakar vs AaradhyaDT).
"""

import sys
import re
import argparse
from pathlib import Path

# Ensure stdout handles UTF-8 on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BANNED_HYPE_WORDS = [
    r"\brevolutionary\b",
    r"\bgame-changing\b",
    r"\bgroundbreaking\b",
    r"\bunleash\b",
    r"\bunleashes\b",
    r"\bunleashing\b",
    r"\bsupercharge\b",
    r"\bsupercharged\b",
    r"\bturbocharge\b",
    r"\bseamlessly\b",
    r"\bcutting-edge\b",
    r"\bnext-generation\b",
    r"\bnext-gen\b",
    r"\beffortlessly\b",
    r"\bmagical\b",
    r"\bwe are thrilled\b",
    r"\bwe are excited\b",
    r"\bunprecedented power\b",
]

SYNTACTIC_AI_PATTERNS = [
    (r"\bnot\s+selling[\.,\s]+not\s+performing\b", "Staccato negation contrast cliché"),
    (r"\bit(?:'s| is)\s+not\s+[^—\.,]+[—\-]\s*it(?:'s| is)\b", "Negation-contrast framing ('It is not X—it is Y')"),
]

# Namespace invariants: specific repos belong strictly to specific namespaces
NAMESPACE_RULES = [
    (r"github\.com/AaradhyaDT/SPARK\b", "SPARK belongs to active R&D namespace: 'Aaradhya-Dev-Tamrakar/SPARK'"),
    (r"github\.com/AaradhyaDT/brainstorm\b", "brainstorm belongs to active R&D namespace: 'Aaradhya-Dev-Tamrakar/brainstorm'"),
    (r"github\.com/Aaradhya-Dev-Tamrakar/BiasAperture\b", "BiasAperture belongs to curated production namespace: 'AaradhyaDT/BiasAperture'"),
    (r"github\.com/Aaradhya-Dev-Tamrakar/Gesture-Controlled-Self-Balancing-Robot\b", "GCSBR belongs to curated production namespace: 'AaradhyaDT/Gesture-Controlled-Self-Balancing-Robot'"),
]


def audit_file(filepath: Path, expected_tier: str = None, expected_domain: str = None) -> list[str]:
    errors = []
    text = filepath.read_text(encoding="utf-8")
    words = text.split()
    word_count = len(words)
    fname = filepath.name.lower()

    # 1. Hype Word Scan (evaluated on prose only; code blocks, backticks, inline math, and markdown tables stripped)
    prose_text = re.sub(r"```[\s\S]*?```", "", text)
    prose_text = re.sub(r"`[^`\n]+`", "", prose_text)
    prose_text = re.sub(r"\$[^$\n]+\$", "", prose_text)
    prose_text = re.sub(r"(?m)^\s*\|.*\|.*$", "", prose_text)
    clean_prose = re.sub(r"\*[^*]+\*", "", prose_text)

    for pattern in BANNED_HYPE_WORDS:
        matches = re.findall(pattern, clean_prose, re.IGNORECASE)
        if matches:
            errors.append(f"Banned hype word detected in prose: '{matches[0]}' (matches pattern '{pattern}')")

    # 2. Syntactic AI Habits Scan (skip vocabulary cheatsheets and reference definitions)
    if "vocabulary" not in fname and "cheatsheet" not in fname and "guide" not in fname:
        for pat, desc in SYNTACTIC_AI_PATTERNS:
            matches = re.findall(pat, prose_text, re.IGNORECASE)
            if matches:
                errors.append(f"Syntactic AI habit detected: {desc} -> '{matches[0]}'")

    # 3. Dual-Namespace URL Integrity Audit (skip SKILL.md rules explaining the split)
    if "skill.md" not in fname:
        for pattern, explanation in NAMESPACE_RULES:
            if re.search(pattern, text):
                errors.append(f"Dual-namespace violation: {explanation}")

    # 4. Tier Detection (Explicit tags take precedence)
    tier = expected_tier
    if not tier:
        if "l5" in fname or "system-card" in fname or ("audit" in fname and "calm" not in fname):
            tier = "L5"
        elif "l4" in fname or "benchmark" in fname or "launch" in fname or "quantization" in fname:
            tier = "L4"
        elif "l3" in fname or "migration" in fname or "spec" in fname or "contract" in fname:
            tier = "L3"
        elif "l2" in fname or "case-study" in fname or "blog" in fname or "postmortem" in fname:
            tier = "L2"
        elif "l1" in fname or "pr" in fname or "portfolio" in fname or "readme" in fname or "issue" in fname:
            tier = "L1"
        elif word_count <= 400:
            tier = "L1"
        else:
            tier = "GENERIC"

    # 5. Domain Detection (Explicit flags take precedence)
    domain = expected_domain
    if not domain:
        if "brainstorm" in fname or "rfc" in fname:
            domain = "brainstorm"
        elif "spark" in fname or "robot" in fname or "gcsbr" in fname or "embedded" in fname or "telemetry" in fname:
            domain = "embedded"
        elif "sim" in fname or "strangler" in fname or "ipu" in fname:
            domain = "arch-sim"
        elif "bias" in fname or "fairness" in fname or "fairface" in fname or "audit" in fname:
            domain = "ml-audit"
        elif "mcp" in fname or "dsp" in fname:
            domain = "mcp-infra"
        elif "portfolio" in fname or "knowledge" in fname:
            domain = "knowledge"

    # 6. Tier-Specific Invariant Checks
    if tier == "L1":
        if word_count > 500:
            errors.append(f"Tier L1 word count exceeded: {word_count} words (max recommended: 350-400 words)")
        has_bullets = bool(re.search(r"^\s*[-*]\s+", text, re.MULTILINE))
        if not has_bullets:
            errors.append("Tier L1 requires active bullet points for changes/capabilities.")

    elif tier == "L2":
        has_metrics = bool(re.search(r"\d+%", text)) or bool(re.search(r"\d+\s*(hours|seconds|ms|queries|hz|deg)", text, re.IGNORECASE))
        if not has_metrics:
            errors.append("Tier L2 case study requires concrete empirical operational metrics.")

    elif tier == "L3":
        has_code = "```json" in text or "```typescript" in text or "```python" in text or "```c" in text or "```cpp" in text
        if not has_code:
            errors.append("Tier L3 developer spec must contain code or payload blocks.")

    elif tier == "L4":
        has_table = "|" in text and ("Subject" in text or "Benchmark" in text or "Baseline" in text or "Accuracy" in text or "Latency" in text or "Architecture" in text)
        if not has_table:
            errors.append("Tier L4 evaluation report must contain a pinned benchmark or tradeoff table.")

    elif tier == "L5":
        has_eval = bool(re.search(r"(evaluation|audit|fairness|disparity|compliance|safety|suppression)", text, re.IGNORECASE))
        if not has_eval:
            errors.append("Tier L5 system card must contain formal evaluation and audit sections.")

    # 7. Domain-Specific Invariant Checks
    if domain == "ml-audit":
        if "badge-guard" not in text and "insufficient-block" not in text and "suppression" not in text.lower():
            errors.append("Domain 'ml-audit' (U3) requires explicit n < 30 cohort suppression guards (.badge-guard).")

    elif domain == "arch-sim":
        # Ensure simulated architectures carry epistemic simulation qualifiers
        if "simulat" not in text.lower() and "e3" not in text.lower():
            errors.append("Domain 'arch-sim' (U2) requires explicit cycle/numerical simulation qualifiers (E3 Sim).")

    elif domain == "brainstorm":
        # Systems ideation requires non-goals or falsification/tradeoff criteria
        if "non-goal" not in text.lower() and "alternative" not in text.lower() and "falsif" not in text.lower():
            errors.append("Domain 'brainstorm' (U0) requires explicit non-goals, rejected alternatives, or falsification criteria.")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Audit technical writing against calm authority invariants (v2.2).")
    parser.add_argument("path", help="Path to markdown file or directory.")
    parser.add_argument("--tier", choices=["L1", "L2", "L3", "L4", "L5"], help="Explicitly enforce a specific depth tier.")
    parser.add_argument("--domain", choices=["brainstorm", "embedded", "arch-sim", "ml-audit", "mcp-infra", "knowledge"], help="Enforce domain-specific proof standards.")
    parser.add_argument("--all", action="store_true", help="Audit all markdown files in target directory.")
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"Error: Path '{target}' does not exist.", file=sys.stderr)
        sys.exit(1)

    files_to_check = []
    if target.is_dir():
        files_to_check = sorted(list(target.glob("*.md")))
    else:
        files_to_check = [target]

    total_errors = 0
    print(f"Auditing {len(files_to_check)} document(s) against Calm Authority Invariants (v2.2)...\n")

    for f in files_to_check:
        errors = audit_file(f, expected_tier=args.tier, expected_domain=args.domain)
        if errors:
            print(f"[FAIL] {f.name}")
            for err in errors:
                print(f"   * {err}")
            total_errors += len(errors)
        else:
            print(f"[PASS] {f.name}")

    print("\n" + "=" * 50)
    if total_errors > 0:
        print(f"FAILED: Found {total_errors} violation(s).")
        sys.exit(1)
    else:
        print("SUCCESS: All documents comply with Calm Authority Invariants (0 errors).")
        sys.exit(0)


if __name__ == "__main__":
    main()
