#!/usr/bin/env python3
"""HK CDE coverage eval: strict SectionRecall vs DocumentRecall + failure dump."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.industry_hk.config import get_industry_hk_config  # noqa: E402
from rag.industry_hk.retrieval import IndustryHybridRetriever  # noqa: E402
from rag.industry_hk.source_family import doc_id_from_url  # noqa: E402


def _load_cases(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _load_manifest_doc_ids(config) -> set[str] | None:
    path = config.storage.manifest_path
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    ids = payload.get("indexed_doc_ids")
    if isinstance(ids, list):
        return {str(item) for item in ids}
    return None


def _hay(chunk) -> str:
    return f"{chunk.source_url} {chunk.title} {chunk.source_file}".lower()


def _section_hit(chunk, case: dict) -> bool:
    expected = str(
        case.get("expected_section_contains") or case.get("expected_section") or ""
    ).lower()
    if not expected:
        return False
    return expected in _hay(chunk)


def _doc_hit(chunk, case: dict) -> bool:
    doc = str(case.get("expected_doc") or "").lower()
    if not doc:
        return False
    hay = f"{chunk.source_url} {chunk.source_file}".lower()
    return doc in hay


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Eval HK coverage SectionRecall")
    parser.add_argument(
        "--cases",
        type=Path,
        default=PROJECT_ROOT / "eval" / "hk_cde_coverage_cases.jsonl",
    )
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument(
        "--failures-out",
        type=Path,
        default=PROJECT_ROOT / "eval" / "results" / "hk_coverage_failures.json",
    )
    args = parser.parse_args(argv)

    cases = _load_cases(args.cases)
    config = get_industry_hk_config()
    retriever = IndustryHybridRetriever(config)
    indexed_docs = _load_manifest_doc_ids(config)

    section_r1 = section_r3 = doc_r1 = doc_r3 = 0
    in_scope = 0
    out_of_scope = 0
    by_doc: dict[str, dict[str, int]] = defaultdict(
        lambda: {"n": 0, "sr1": 0, "sr3": 0, "dr1": 0, "dr3": 0}
    )
    failures: list[dict] = []

    for case in cases:
        doc_id = str(case.get("expected_doc") or "unknown")
        if indexed_docs is not None and doc_id not in indexed_docs:
            out_of_scope += 1
            continue
        in_scope += 1
        result = retriever.retrieve_with_debug(case["query"], top_k=args.top_k)
        chunks = result.chunks
        by_doc[doc_id]["n"] += 1

        top_section = bool(chunks and _section_hit(chunks[0], case))
        any_section = any(_section_hit(chunk, case) for chunk in chunks[: args.top_k])
        top_doc = bool(chunks and _doc_hit(chunks[0], case))
        any_doc = any(_doc_hit(chunk, case) for chunk in chunks[: args.top_k])

        if top_section:
            section_r1 += 1
            by_doc[doc_id]["sr1"] += 1
        if any_section:
            section_r3 += 1
            by_doc[doc_id]["sr3"] += 1
        if top_doc:
            doc_r1 += 1
            by_doc[doc_id]["dr1"] += 1
        if any_doc:
            doc_r3 += 1
            by_doc[doc_id]["dr3"] += 1

        if not top_section:
            top3 = []
            for chunk in chunks[: args.top_k]:
                top3.append(
                    {
                        "title": chunk.title,
                        "source_url": chunk.source_url,
                        "doc_id": doc_id_from_url(chunk.source_url),
                        "score": chunk.score,
                    }
                )
            failure_kind = "section_not_in_index"
            if any_section:
                failure_kind = "within_doc_rank" if top_doc else "cross_doc_rank"
            elif any_doc:
                failure_kind = "wrong_section_same_doc"
            elif top3:
                failure_kind = "doc_routing_miss"
            failures.append(
                {
                    "id": case.get("id"),
                    "query": case["query"],
                    "expected_doc": doc_id,
                    "expected_section": case.get("expected_section"),
                    "failure_kind": failure_kind,
                    "top3": top3,
                }
            )

    n = max(in_scope, 1)
    report = {
        "cases": len(cases),
        "in_scope_cases": in_scope,
        "out_of_scope_cases": out_of_scope,
        "section_recall_at_1": section_r1 / n,
        "section_recall_at_3": section_r3 / n,
        "document_recall_at_1": doc_r1 / n,
        "document_recall_at_3": doc_r3 / n,
        # Backward-compatible alias used by compare_hk_indexes.py
        "document_accuracy_at_1": doc_r1 / n,
        "by_doc": {
            key: {
                "cases": val["n"],
                "section_recall_at_1": val["sr1"] / max(val["n"], 1),
                "section_recall_at_3": val["sr3"] / max(val["n"], 1),
                "document_recall_at_1": val["dr1"] / max(val["n"], 1),
                "document_recall_at_3": val["dr3"] / max(val["n"], 1),
                # aliases for older printers
                "recall_at_1": val["sr1"] / max(val["n"], 1),
                "recall_at_3": val["sr3"] / max(val["n"], 1),
            }
            for key, val in sorted(by_doc.items())
        },
        "failures": len(failures),
    }

    print("HK CDE Coverage Eval")
    print(f"  cases: {report['cases']} (in_scope={in_scope}, out_of_scope={out_of_scope})")
    print(
        f"  SectionRecall@1: {report['section_recall_at_1']:.1%} ({section_r1}/{in_scope})"
    )
    print(
        f"  SectionRecall@3: {report['section_recall_at_3']:.1%} ({section_r3}/{in_scope})"
    )
    print(
        f"  DocumentRecall@1: {report['document_recall_at_1']:.1%} ({doc_r1}/{in_scope})"
    )
    print(
        f"  DocumentRecall@3: {report['document_recall_at_3']:.1%} ({doc_r3}/{in_scope})"
    )
    for doc_id, stats in report["by_doc"].items():
        print(
            f"  [{doc_id}] n={stats['cases']} "
            f"R@1={stats['section_recall_at_1']:.1%} "
            f"R@3={stats['section_recall_at_3']:.1%} "
            f"Doc@1={stats['document_recall_at_1']:.1%}"
        )

    args.failures_out.parent.mkdir(parents=True, exist_ok=True)
    args.failures_out.write_text(
        json.dumps(failures, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    ok = report["section_recall_at_3"] >= 0.70
    if not ok:
        print("FAIL: SectionRecall@3 < 70%", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
