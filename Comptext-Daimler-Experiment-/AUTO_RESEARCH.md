# CompText V6 – Autonomous Research & Validation

This project follows the **Autonomous Iteration** paradigm. The goal is to maximize the **Quality Score** through continuous, AI-driven validation and optimization.

## Quality Metrics

| Metric | Target | Weight |
| :--- | :--- | :--- |
| **Unit Test Pass Rate** | 100% | 40% |
| **Code Coverage (src/)** | > 90% | 40% |
| **Security (Bandit)** | 0 Issues | 20% |
| **Latency (P95)** | < 100ms | Pass/Fail |

## Autonomous Loop

1.  **Execute**: Run `python scripts/auto_validator.py`.
2.  **Analyze**: Review `validation_report.json`.
3.  **Optimize**: Identify failing tests or coverage gaps and fix code/tests.
4.  **Verify**: Re-run validation.

## Research Goals

- **KVTC Efficiency**: Increase token reduction without losing diagnostic semantics.
- **NLA Fidelity**: Ensure unsupervised explanations align with ground-truth industrial codes.
- **Context-Aware Triage**: Minimize P1 false-positives while maintaining zero false-negatives.
