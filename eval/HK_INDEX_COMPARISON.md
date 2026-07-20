# HK Index Comparison

Source-grounded engineering benchmark (not customer acceptance).

## Gates (substantive promotion)

- `baseline_recall_ok`: **PASS**
- `docs_fp_zero`: **PASS**
- `coverage_r3_ok`: **PASS**
- `source_acc_ok`: **PASS**
- `no_major_regression`: **PASS**
- `substantive_suite_pass`: **PASS**

- `promote_substantive`: **YES**
- `promote_expanded_high`: **YES**
- **Accepted scope: `high_with_routed_shadow`**

## Metrics

| Mode | Baseline R@1 | Coverage R@1 | Coverage R@3 | Source Acc |
|------|--------------|--------------|--------------|------------|
| high | 100.0% | 77.0% | 91.0% | 97.5% |
| substantive | 100.0% | 77.0% | 91.0% | 97.5% |

## Decision notes

- After retrieval hardening, keep production on **`high`** and merge case_study / terminology / software_guide hits from the substantive shadow on explicit family intent.
- Flat promotion of `substantive` may be gate-green for diagnostics, but is not the preferred production swap while everyday CDE queries should stay on the curated high pool.
- Software-specific statutory appendices remain deferred from `substantive` and available via `--scope all`.
- This is a source-grounded engineering benchmark, not customer acceptance or legal interpretation validation.

