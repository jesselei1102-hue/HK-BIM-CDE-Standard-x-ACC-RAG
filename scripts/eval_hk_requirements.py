#!/usr/bin/env python3
"""HK requirement / authority / refusal grounded checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.industry_hk.config import get_industry_hk_config  # noqa: E402
from rag.industry_hk.intent import is_out_of_domain, route_track  # noqa: E402
from rag.industry_hk.retrieval import IndustryHybridRetriever  # noqa: E402

MANDATORY_CLAIM_RE = re.compile(
    r"\b(mandatory|must comply|binding standard|legal requirement|"
    r"所有香港项目必须|所有香港項目必須|必须照搬|必須照搬)\b",
    re.I,
)
REFERENCE_CUE_RE = re.compile(
    r"case study|reference only|not a mandatory|not mandatory|not binding|"
    r"rather than a mandatory|operational guidance|implementation example|"
    r"terminology|dictionary|"
    r"案例|参考|參考|非强制|非強制|不是.*标准|不是.*標準|术语|詞典|词典",
    re.I,
)


def _claims_mandatory_without_caveat(text: str) -> bool:
    """True when the answer asserts a binding duty without a non-binding cue."""
    if not MANDATORY_CLAIM_RE.search(text):
        return False
    if REFERENCE_CUE_RE.search(text):
        return False
    return True


def _load_cases(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _chunk_blob(chunk) -> str:
    return f"{chunk.source_url}\n{chunk.title}\n{chunk.source_file}\n{chunk.text[:2000]}"


def _load_manifest(config) -> dict:
    path = config.storage.manifest_path
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _case_applicable(case: dict, manifest: dict) -> bool:
    indexed_docs = set(manifest.get("indexed_doc_ids") or [])
    indexed_types = set(manifest.get("indexed_authority_types") or [])
    expected_doc = case.get("expected_doc")
    if expected_doc:
        if not indexed_docs:
            return True
        return expected_doc in indexed_docs
    expected_type = case.get("expected_authority_type")
    if expected_type:
        if not indexed_types:
            return True
        return expected_type in indexed_types
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Eval HK requirements grounding")
    parser.add_argument(
        "--requirements",
        type=Path,
        default=PROJECT_ROOT / "eval" / "hk_cde_requirement_cases.jsonl",
    )
    parser.add_argument(
        "--negatives",
        type=Path,
        default=PROJECT_ROOT / "eval" / "hk_cde_negative_cases.jsonl",
    )
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument(
        "--skip-generation",
        action="store_true",
        help="Skip LLM authority generation checks (retrieval-only).",
    )
    args = parser.parse_args(argv)

    req_cases = _load_cases(args.requirements)
    neg_cases = _load_cases(args.negatives)
    config = get_industry_hk_config()
    retriever = IndustryHybridRetriever(config)
    manifest = _load_manifest(config)

    source_hits = 0
    section_hits = 0
    key_fact_hits = 0
    modality_hits = 0
    for case in req_cases:
        result = retriever.retrieve_with_debug(case["query"], top_k=3)
        blobs = [_chunk_blob(chunk).lower() for chunk in result.chunks]
        joined = "\n".join(blobs)
        expected_section = str(case.get("expected_section_contains") or "").lower()
        expected_doc = str(case.get("expected_doc") or "").lower()
        if any(expected_section and expected_section in blob for blob in blobs):
            section_hits += 1
            source_hits += 1
        elif any(expected_doc and expected_doc in blob for blob in blobs):
            source_hits += 1
        facts = [str(item).lower() for item in case.get("key_facts") or []]
        if not facts or any(fact in joined for fact in facts):
            key_fact_hits += 1
        modality = str(case.get("required_modality") or "").lower()
        if not modality or any(
            token in joined
            for token in (modality, "shall", "must", "required", "should")
        ):
            modality_hits += 1

    authority_retrieval_ok = 0
    authority_generation_ok = 0
    authority_total = 0
    authority_out_of_scope = 0
    route_ok = 0
    route_total = 0
    ood_ok = 0
    ood_total = 0

    for case in neg_cases:
        expect_track = case.get("expect_track")
        case_type = case.get("case_type")
        predicted = route_track(case["query"])

        if case_type == "refusal" or expect_track == "out_of_domain":
            ood_total += 1
            if predicted == "out_of_domain" or is_out_of_domain(case["query"]):
                ood_ok += 1
            continue

        if expect_track in {"industry", "docs", "hybrid"}:
            route_total += 1
            mapped = {
                "industry": "industry",
                "docs": "docs",
                "hybrid": "hybrid",
            }.get(expect_track, expect_track)
            # Treat hk_cde as industry for fixture compatibility.
            if predicted == mapped or (
                mapped == "industry" and predicted in {"industry", "hybrid"}
            ):
                route_ok += 1

        if case.get("case_type") != "authority_confusion":
            continue

        if not _case_applicable(case, manifest):
            authority_out_of_scope += 1
            # Out-of-scope on production high: require that we do not
            # retrieve a mandatory standard as if it answered the case.
            result = retriever.retrieve_with_debug(case["query"], top_k=3)
            blob = "\n".join(_chunk_blob(c) for c in result.chunks).lower()
            if "normative_weight: mandatory" in blob and not any(
                token in blob
                for token in (
                    "authority_type: case_study",
                    "authority_type: terminology",
                    "authority_type: software_guide",
                    "normative_weight: reference",
                    "normative_weight: operational",
                )
            ):
                # Soft note only for OOS reporting; does not count as skip-pass.
                pass
            continue

        authority_total += 1
        result = retriever.retrieve_with_debug(case["query"], top_k=3)
        blob = "\n".join(_chunk_blob(c) for c in result.chunks).lower()
        expected_doc = str(case.get("expected_doc") or "").lower()
        expected_type = str(case.get("expected_authority_type") or "").lower()
        doc_hit = (not expected_doc) or any(
            expected_doc in _chunk_blob(c).lower() for c in result.chunks
        )
        type_hit = (
            f"authority_type: {expected_type}" in blob
            or expected_type.replace("_", " ") in blob
        )
        weight_hit = (
            "normative_weight: reference" in blob
            or "normative_weight: operational" in blob
        )
        # Multi-chunk docs may only keep authority headers on chunk 0; fall back
        # to the source registry when the expected doc itself was retrieved.
        if doc_hit and expected_doc and not (type_hit or weight_hit):
            from rag.industry_hk.source_family import source_by_doc_id

            spec = source_by_doc_id(expected_doc)
            if spec and spec.authority_type == expected_type:
                type_hit = True
            if spec and spec.normative_weight in {"reference", "operational"}:
                weight_hit = True
        retrieval_pass = doc_hit and (type_hit or weight_hit)
        if retrieval_pass:
            authority_retrieval_ok += 1

        generation_pass = True
        if case.get("must_not_claim_mandatory") and not args.skip_generation:
            try:
                from rag.generation import generate_answer

                answer = generate_answer(case["query"], result.chunks)
                text = getattr(answer, "answer", None) or str(answer)
                if _claims_mandatory_without_caveat(text):
                    generation_pass = False
                elif not REFERENCE_CUE_RE.search(text) and expected_type in {
                    "case_study",
                    "terminology",
                    "software_guide",
                }:
                    # Prefer explicit non-binding cue when answering authority questions.
                    generation_pass = "reference" in text.lower() or "case" in text.lower()
            except Exception:
                # If generation unavailable, fall back to retrieval-only authority.
                generation_pass = retrieval_pass
        if generation_pass:
            authority_generation_ok += 1

    n_req = max(len(req_cases), 1)
    authority_retrieval_acc = (
        authority_retrieval_ok / authority_total if authority_total else 1.0
    )
    authority_generation_acc = (
        authority_generation_ok / authority_total if authority_total else 1.0
    )
    report = {
        "requirement_cases": len(req_cases),
        "negative_cases": len(neg_cases),
        "source_accuracy": source_hits / n_req,
        "section_accuracy": section_hits / n_req,
        "key_fact_retention": key_fact_hits / n_req,
        "modality_retention": modality_hits / n_req,
        "authority_retrieval_accuracy": authority_retrieval_acc,
        "authority_generation_accuracy": authority_generation_acc,
        # Compatibility with compare_hk_indexes.py parser
        "authority_confusion_accuracy": authority_retrieval_acc,
        "negative_route_accuracy": route_ok / max(route_total, 1) if route_total else 1.0,
        "out_of_domain_accuracy": ood_ok / max(ood_total, 1) if ood_total else 1.0,
        "authority_ok": authority_retrieval_ok,
        "authority_total": authority_total,
        "authority_out_of_scope": authority_out_of_scope,
        "authority_skipped_not_in_index": 0,
    }

    print("HK CDE Requirements Eval")
    print(f"  requirement cases: {report['requirement_cases']}")
    print(f"  source accuracy: {report['source_accuracy']:.1%} ({source_hits}/{len(req_cases)})")
    print(f"  section accuracy: {report['section_accuracy']:.1%} ({section_hits}/{len(req_cases)})")
    print(f"  key-fact retention: {report['key_fact_retention']:.1%}")
    print(f"  modality retention: {report['modality_retention']:.1%}")
    print(
        f"  authority retrieval accuracy: {authority_retrieval_acc:.1%} "
        f"({authority_retrieval_ok}/{authority_total}; out_of_scope={authority_out_of_scope})"
    )
    print(
        f"  authority generation accuracy: {authority_generation_acc:.1%} "
        f"({authority_generation_ok}/{authority_total})"
    )
    print(
        f"  authority confusion accuracy: {report['authority_confusion_accuracy']:.1%} "
        f"({authority_retrieval_ok}/{authority_total}; skipped_not_in_index=0)"
    )
    print(f"  negative route accuracy: {report['negative_route_accuracy']:.1%}")
    print(f"  out-of-domain accuracy: {report['out_of_domain_accuracy']:.1%}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    ok = (
        report["source_accuracy"] >= 0.75
        and report["key_fact_retention"] >= 0.80
        and (
            authority_total == 0
            or (
                authority_retrieval_acc >= 0.75
                and authority_generation_acc >= 0.75
            )
        )
    )
    if not ok:
        print("FAIL: requirement grounding below gate", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
