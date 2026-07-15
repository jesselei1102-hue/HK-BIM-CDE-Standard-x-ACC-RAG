#!/usr/bin/env python3
"""三轨编排：分类 → 单轨或并行检索 → 生成。"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from rag.config import AppConfig, get_config
from rag.generation import Answer, generate_answer, generate_hybrid_answer
from rag.industry_hk.config import IndustryHKConfig, get_industry_hk_config
from rag.industry_hk.retrieval import IndustryHybridRetriever
from rag.orchestrator.classify import (
    CAPABILITY_PLAYBOOK_URL_PREFIX,
    IntentDecision,
    classify_intent,
    detect_capability,
    is_folder_question,
)
from rag.orchestrator.merge import MergedContexts, merge_triple_contexts
from rag.playbook_acc_hk.config import PlaybookConfig, get_playbook_config
from rag.playbook_acc_hk.retrieval import PlaybookHybridRetriever, playbook_to_app_config
from rag.retrieval import HybridRetriever, RetrievalDebugInfo, RetrievalResult


@dataclass
class OrchestratorDebug:
    intent: IntentDecision
    docs_debug: RetrievalDebugInfo | None = None
    industry_debug: RetrievalDebugInfo | None = None
    playbook_debug: RetrievalDebugInfo | None = None
    merged: MergedContexts | None = None
    validation_warnings: list[str] | None = None
    validation_retried: bool = False


@dataclass
class OrchestratorResult:
    track: str
    answer: Answer | None
    chunks_docs: list
    chunks_industry: list
    chunks_playbook: list
    merged: MergedContexts | None
    debug: OrchestratorDebug
    retrieval: RetrievalResult | None = None
    validation_ok: bool | None = None


class HybridOrchestrator:
    def __init__(
        self,
        *,
        docs_config: AppConfig | None = None,
        industry_config: IndustryHKConfig | None = None,
        playbook_config: PlaybookConfig | None = None,
    ) -> None:
        self.docs_config = docs_config or get_config()
        self.industry_config = industry_config or get_industry_hk_config()
        self.playbook_config = playbook_config or get_playbook_config()
        self._docs_retriever: HybridRetriever | None = None
        self._industry_retriever: IndustryHybridRetriever | None = None
        self._playbook_retriever: PlaybookHybridRetriever | None = None

    @property
    def docs_retriever(self) -> HybridRetriever:
        if self._docs_retriever is None:
            self._docs_retriever = HybridRetriever(self.docs_config)
        return self._docs_retriever

    @property
    def industry_retriever(self) -> IndustryHybridRetriever:
        if self._industry_retriever is None:
            self._industry_retriever = IndustryHybridRetriever(self.industry_config)
        return self._industry_retriever

    @property
    def playbook_retriever(self) -> PlaybookHybridRetriever:
        if self._playbook_retriever is None:
            self._playbook_retriever = PlaybookHybridRetriever(self.playbook_config)
        return self._playbook_retriever

    def _pick_playbook_chunks(
        self,
        *,
        question: str,
        decision: IntentDecision,
        playbook_query: str,
        playbook_top: int,
        playbook_boost: str | None,
    ) -> list:
        folderish = is_folder_question(question, decision.capability)
        if folderish:
            from rag.orchestrator.playbook_pin import load_wip_folder_chunk

            hard = load_wip_folder_chunk(self.playbook_config.storage.chunks_path)
            if hard is not None:
                return [hard]

            wider = self.playbook_retriever.retrieve_with_debug(
                "01_WIP 02_Shared 03_Published 04_Archive folder tree structure",
                max(playbook_top, 6),
                boost_url_prefix=playbook_boost
                or CAPABILITY_PLAYBOOK_URL_PREFIX["folder"],
            ).chunks
            # 只接受明确 WIP 目录树证据；找不到则退回正常检索
            for chunk in wider:
                if "2_wip" in chunk.source_url or "Central_Models" in chunk.text:
                    return [chunk]
            for chunk in wider:
                if "`01_WIP`" in chunk.text and "`02_Shared`" in chunk.text:
                    return [chunk]

        result = self.playbook_retriever.retrieve_with_debug(
            playbook_query,
            playbook_top,
            boost_url_prefix=playbook_boost,
        )
        return list(result.chunks)

    def classify(self, question: str) -> IntentDecision:
        return classify_intent(question)

    def retrieve_hybrid(
        self,
        question: str,
        intent: IntentDecision | None = None,
        *,
        top_k: int | None = None,
    ) -> OrchestratorResult:
        decision = intent or classify_intent(question)
        # hybrid 默认：Docs 2、行业/手册各 1；显式 top_k 时三轨同用该值
        if top_k is None:
            docs_top = 2
            industry_top = 1
            playbook_top = 1
        else:
            docs_top = top_k
            industry_top = top_k
            playbook_top = top_k

        product_query = decision.product_query or question
        industry_query = decision.industry_query or question
        playbook_query = decision.playbook_query or question
        playbook_boost = CAPABILITY_PLAYBOOK_URL_PREFIX.get(
            decision.capability or ""
        )
        if is_folder_question(question, decision.capability):
            playbook_boost = CAPABILITY_PLAYBOOK_URL_PREFIX["folder"]

        with ThreadPoolExecutor(max_workers=2) as pool:
            docs_future = pool.submit(
                self.docs_retriever.retrieve_with_debug,
                product_query,
                docs_top,
            )
            industry_future = pool.submit(
                self.industry_retriever.retrieve_with_debug,
                industry_query,
                industry_top,
            )
            docs_result = docs_future.result()
            industry_result = industry_future.result()

        folderish = is_folder_question(question, decision.capability)
        docs_chunks = list(docs_result.chunks)
        if folderish:
            from rag.orchestrator.chunk_pin import load_docs_folder_chunks

            pinned_docs = load_docs_folder_chunks(
                self.docs_config.storage.chunks_path,
                limit=docs_top,
            )
            if pinned_docs:
                docs_chunks = pinned_docs
        elif decision.capability == "naming":
            from rag.orchestrator.chunk_pin import load_docs_naming_chunks

            pinned_docs = load_docs_naming_chunks(
                self.docs_config.storage.chunks_path,
                limit=docs_top,
            )
            if pinned_docs:
                docs_chunks = pinned_docs
        elif decision.capability == "model_viewer":
            from rag.orchestrator.chunk_pin import load_docs_model_viewer_chunks

            pinned_docs = load_docs_model_viewer_chunks(
                self.docs_config.storage.chunks_path,
                limit=docs_top,
            )
            if pinned_docs:
                docs_chunks = pinned_docs
        elif decision.capability in {
            "permissions",
            "project_create",
            "project_template",
            "workflow",
        }:
            from rag.orchestrator.chunk_pin import prefer_docs_for_capability

            docs_chunks = prefer_docs_for_capability(
                decision.capability,
                docs_chunks,
                chunks_path=self.docs_config.storage.chunks_path,
                limit=docs_top,
            )

        playbook_chunks = self._pick_playbook_chunks(
            question=question,
            decision=decision,
            playbook_query=playbook_query,
            playbook_top=playbook_top,
            playbook_boost=playbook_boost,
        )
        playbook_result_debug = self.playbook_retriever.last_debug

        merged = merge_triple_contexts(
            docs_chunks=docs_chunks,
            industry_chunks=industry_result.chunks,
            playbook_chunks=playbook_chunks,
            docs_top_k=docs_top,
            industry_top_k=industry_top,
            playbook_top_k=playbook_top,
            maximum_context_tokens=self.docs_config.retrieval.maximum_context_tokens,
        )
        merged, pin_warnings = self._ensure_folder_hybrid_merged(
            merged,
            question=question,
            capability=decision.capability,
            docs_top_k=docs_top,
        )
        naming_warnings: list[str] = []
        if decision.capability == "naming":
            merged, naming_warnings = self._ensure_naming_hybrid_merged(
                merged,
                capability=decision.capability,
                docs_top_k=docs_top,
            )
        viewer_warnings: list[str] = []
        if decision.capability == "model_viewer":
            merged, viewer_warnings = self._ensure_model_viewer_hybrid_merged(
                merged,
                capability=decision.capability,
                docs_top_k=docs_top,
            )
        all_pin_warnings = (pin_warnings or []) + naming_warnings + viewer_warnings
        debug = OrchestratorDebug(
            intent=decision,
            docs_debug=docs_result.debug,
            industry_debug=industry_result.debug,
            playbook_debug=playbook_result_debug,
            merged=merged,
            validation_warnings=all_pin_warnings or None,
        )
        return OrchestratorResult(
            track="hybrid",
            answer=None,
            chunks_docs=merged.docs_chunks,
            chunks_industry=merged.industry_chunks,
            chunks_playbook=merged.playbook_chunks,
            merged=merged,
            debug=debug,
        )

    def _ensure_naming_hybrid_merged(
        self,
        merged: MergedContexts,
        *,
        capability: str | None,
        docs_top_k: int,
    ) -> tuple[MergedContexts, list[str]]:
        from rag.orchestrator.chunk_pin import ensure_naming_hybrid_merged

        return ensure_naming_hybrid_merged(
            merged,
            capability=capability,
            playbook_chunks_path=self.playbook_config.storage.chunks_path,
            docs_chunks_path=self.docs_config.storage.chunks_path,
            industry_chunks_path=self.industry_config.storage.chunks_path,
            docs_top_k=docs_top_k,
        )

    def _ensure_model_viewer_hybrid_merged(
        self,
        merged: MergedContexts,
        *,
        capability: str | None,
        docs_top_k: int,
    ) -> tuple[MergedContexts, list[str]]:
        from rag.orchestrator.chunk_pin import ensure_model_viewer_hybrid_merged

        return ensure_model_viewer_hybrid_merged(
            merged,
            capability=capability,
            docs_chunks_path=self.docs_config.storage.chunks_path,
            docs_top_k=docs_top_k,
        )

    def _ensure_folder_hybrid_merged(
        self,
        merged: MergedContexts,
        *,
        question: str,
        capability: str | None,
        docs_top_k: int,
    ) -> tuple[MergedContexts, list[str]]:
        from rag.orchestrator.chunk_pin import ensure_folder_hybrid_merged

        return ensure_folder_hybrid_merged(
            merged,
            question=question,
            capability=capability,
            playbook_chunks_path=self.playbook_config.storage.chunks_path,
            docs_chunks_path=self.docs_config.storage.chunks_path,
            docs_top_k=docs_top_k,
        )

    def _generate_hybrid_with_validation(
        self,
        question: str,
        result: OrchestratorResult,
        *,
        answer_lang: str = "auto",
    ) -> OrchestratorResult:
        from rag.orchestrator.validate import (
            collect_drop_indices,
            drop_docs_indices,
            prefilter_docs_for_capability,
            validate_hybrid_answer,
        )

        merged = result.merged
        assert merged is not None
        capability = result.debug.intent.capability

        merged, pin_warnings = self._ensure_folder_hybrid_merged(
            merged,
            question=question,
            capability=capability,
            docs_top_k=len(merged.docs_chunks) or 2,
        )
        if pin_warnings:
            result.merged = merged
            result.chunks_playbook = merged.playbook_chunks
            result.chunks_docs = merged.docs_chunks
            result.chunks_industry = merged.industry_chunks
            warnings = list(result.debug.validation_warnings or [])
            warnings.extend(pin_warnings)
            result.debug.validation_warnings = warnings

        if capability == "naming":
            merged, naming_warnings = self._ensure_naming_hybrid_merged(
                merged,
                capability=capability,
                docs_top_k=len(merged.docs_chunks) or 2,
            )
            if naming_warnings:
                result.merged = merged
                result.chunks_playbook = merged.playbook_chunks
                result.chunks_docs = merged.docs_chunks
                result.chunks_industry = merged.industry_chunks
                warnings = list(result.debug.validation_warnings or [])
                warnings.extend(naming_warnings)
                result.debug.validation_warnings = warnings

        if capability == "model_viewer":
            merged, viewer_warnings = self._ensure_model_viewer_hybrid_merged(
                merged,
                capability=capability,
                docs_top_k=len(merged.docs_chunks) or 2,
            )
            if viewer_warnings:
                result.merged = merged
                result.chunks_playbook = merged.playbook_chunks
                result.chunks_docs = merged.docs_chunks
                result.chunks_industry = merged.industry_chunks
                warnings = list(result.debug.validation_warnings or [])
                warnings.extend(viewer_warnings)
                result.debug.validation_warnings = warnings

        pre_merged, pre_drops = prefilter_docs_for_capability(merged, capability)
        if pre_drops:
            result.debug.validation_warnings = [
                f"[soft] prefilter_docs: dropped indices {sorted(pre_drops)}"
            ]
            merged = pre_merged
            result.merged = pre_merged
            result.chunks_docs = pre_merged.docs_chunks
            result.chunks_industry = pre_merged.industry_chunks
            result.chunks_playbook = pre_merged.playbook_chunks
            result.debug.merged = pre_merged

        from rag.answer_language import polish_hybrid_answer, resolve_answer_language
        from rag.orchestrator.structured_compose import try_compose_structured_hybrid

        structured_text = try_compose_structured_hybrid(
            merged, capability, question=question, answer_lang=answer_lang
        )
        if structured_text:
            lang = resolve_answer_language(question, answer_lang)
            structured_text = polish_hybrid_answer(structured_text, lang=lang)
            structured_validation = validate_hybrid_answer(
                structured_text, merged, capability=capability
            )
            warnings = list(result.debug.validation_warnings or [])
            warnings.extend(structured_validation.warnings)
            warnings.append("[soft] structured_compose: used rule-based hybrid answer")
            result.debug.validation_warnings = warnings
            result.validation_ok = structured_validation.ok
            if structured_validation.ok:
                contexts = [item.chunk for item in merged.tracked]
                result.answer = Answer(
                    question=question,
                    answer=structured_text,
                    contexts=contexts,
                    model="structured_compose",
                    context_tokens=sum(
                        int(getattr(c, "token_count", 0) or 0) for c in contexts
                    ),
                )
                return result

        if is_folder_question(question, capability):
            from rag.orchestrator.chunk_pin import playbook_chunk_is_concept

            playbook_items = [t for t in merged.tracked if t.track == "playbook"]
            if playbook_items and playbook_chunk_is_concept(playbook_items[0].chunk):
                hint = (
                    "无法生成可靠答案：Playbook 仍停留在「四容器概念回顧」段，"
                    "缺少 WIP 目录树与 ACC 配置步骤。\n\n"
                    "请确认已保存最新代码，并在项目根目录执行：\n"
                    "  python scripts/ingest_playbook_acc_hk.py --rebuild\n"
                    "  python ask.py --corpus hybrid --no-generate "
                    "\"怎么按港标在 ACC 配置文件夹结构\"\n"
                    "确认来源 [2] 为「2. WIP 容器配置」后再提问。"
                )
                result.answer = Answer(
                    question=question,
                    answer=hint,
                    contexts=[item.chunk for item in merged.tracked],
                    model="blocked_bad_retrieval",
                    context_tokens=sum(
                        int(getattr(t.chunk, "token_count", 0) or 0)
                        for t in merged.tracked
                    ),
                )
                result.validation_ok = False
                warnings = list(result.debug.validation_warnings or [])
                warnings.append("[hard] blocked_llm: playbook concept chunk only")
                result.debug.validation_warnings = warnings
                return result

        answer = generate_hybrid_answer(question, merged, self.docs_config, answer_lang=answer_lang)
        validation = validate_hybrid_answer(
            answer.answer, merged, capability=capability
        )
        warnings = list(result.debug.validation_warnings or [])
        warnings.extend(validation.warnings)
        result.debug.validation_warnings = warnings
        result.validation_ok = validation.ok

        if validation.ok:
            result.answer = answer
            return result

        drops = collect_drop_indices(validation)
        if not drops:
            result.answer = answer
            return result

        retry_merged = drop_docs_indices(merged, drops)
        if not retry_merged.tracked:
            result.answer = answer
            return result

        retry_answer = generate_hybrid_answer(
            question, retry_merged, self.docs_config, answer_lang=answer_lang
        )
        retry_validation = validate_hybrid_answer(
            retry_answer.answer,
            retry_merged,
            capability=capability,
        )
        result.debug.validation_retried = True
        result.debug.merged = retry_merged
        result.debug.validation_warnings = (
            warnings
            + ["--- after retry ---"]
            + retry_validation.warnings
        )
        result.merged = retry_merged
        result.chunks_docs = retry_merged.docs_chunks
        result.chunks_industry = retry_merged.industry_chunks
        result.chunks_playbook = retry_merged.playbook_chunks
        result.answer = retry_answer
        result.validation_ok = retry_validation.ok
        return result

    def ask(
        self,
        question: str,
        *,
        force_track: str | None = None,
        top_k: int | None = None,
        no_generate: bool = False,
        answer_lang: str = "auto",
    ) -> OrchestratorResult:
        from rag.generation import Answer
        from rag.orchestrator.capabilities_help import (
            build_capabilities_help,
            is_capabilities_help_question,
        )

        if is_capabilities_help_question(question):
            decision = IntentDecision(
                track="meta",
                capability=None,
                product_query=None,
                industry_query=None,
                playbook_query=None,
                has_product_signal=False,
                has_industry_signal=False,
                has_playbook_signal=False,
                reason="capabilities_help",
            )
            text = (
                "(仅检索模式，未调用生成模型)\n\n"
                + build_capabilities_help(question=question, answer_lang=answer_lang)
                if no_generate
                else build_capabilities_help(question=question, answer_lang=answer_lang)
            )
            return OrchestratorResult(
                track="meta",
                answer=Answer(
                    question=question,
                    answer=text,
                    contexts=[],
                    model="capabilities_help",
                ),
                chunks_docs=[],
                chunks_industry=[],
                chunks_playbook=[],
                merged=None,
                debug=OrchestratorDebug(intent=decision),
                validation_ok=True,
            )

        if force_track == "docs":
            capability = detect_capability(question)
            decision = IntentDecision(
                track="docs",
                capability=capability.key if capability else None,
                product_query=(
                    capability.product_query if capability else question
                ),
                industry_query=None,
                playbook_query=None,
                has_product_signal=True,
                has_industry_signal=False,
                has_playbook_signal=False,
                reason="forced_docs",
            )
        elif force_track == "hk_cde":
            capability = detect_capability(question)
            decision = IntentDecision(
                track="hk_cde",
                capability=capability.key if capability else None,
                product_query=None,
                industry_query=(
                    capability.industry_query if capability else question
                ),
                playbook_query=None,
                has_product_signal=False,
                has_industry_signal=True,
                has_playbook_signal=False,
                reason="forced_hk_cde",
            )
        elif force_track == "playbook":
            capability = detect_capability(question)
            decision = IntentDecision(
                track="playbook",
                capability=capability.key if capability else None,
                product_query=None,
                industry_query=None,
                playbook_query=(
                    capability.playbook_query if capability else question
                ),
                has_product_signal=False,
                has_industry_signal=False,
                has_playbook_signal=True,
                reason="forced_playbook",
            )
        elif force_track == "hybrid":
            decision = classify_intent(question)
            if decision.track != "hybrid":
                from rag.orchestrator.classify import (
                    _fallback_queries,
                    capability_template_by_key,
                )

                capability = detect_capability(question) or (
                    capability_template_by_key(decision.capability)
                )
                if capability is not None:
                    decision = IntentDecision(
                        track="hybrid",
                        capability=capability.key,
                        product_query=capability.product_query,
                        industry_query=capability.industry_query,
                        playbook_query=capability.playbook_query,
                        has_product_signal=True,
                        has_industry_signal=True,
                        has_playbook_signal=True,
                        reason=f"forced_hybrid_capability_{capability.key}",
                    )
                else:
                    product_query, industry_query, playbook_query = _fallback_queries(
                        question
                    )
                    decision = IntentDecision(
                        track="hybrid",
                        capability=decision.capability,
                        product_query=product_query,
                        industry_query=industry_query,
                        playbook_query=playbook_query,
                        has_product_signal=True,
                        has_industry_signal=True,
                        has_playbook_signal=True,
                        reason="forced_hybrid",
                    )
        else:
            decision = classify_intent(question)

        if decision.track == "hybrid":
            result = self.retrieve_hybrid(question, decision, top_k=top_k)
            if no_generate:
                return result
            return self._generate_hybrid_with_validation(
                question, result, answer_lang=answer_lang
            )

        if decision.track == "hk_cde":
            retrieval = self.industry_retriever.retrieve_with_debug(
                decision.industry_query or question, top_k=top_k
            )
            debug = OrchestratorDebug(
                intent=decision,
                industry_debug=retrieval.debug,
            )
            answer = None
            if not no_generate:
                answer = generate_answer(
                    question, retrieval.chunks, self.industry_config,  # type: ignore[arg-type]
                    answer_lang=answer_lang,
                )
            return OrchestratorResult(
                track="hk_cde",
                answer=answer,
                chunks_docs=[],
                chunks_industry=retrieval.chunks,
                chunks_playbook=[],
                merged=None,
                debug=debug,
                retrieval=retrieval,
            )

        if decision.track == "playbook":
            playbook_boost = CAPABILITY_PLAYBOOK_URL_PREFIX.get(
                decision.capability or ""
            )
            retrieval = self.playbook_retriever.retrieve_with_debug(
                decision.playbook_query or question,
                top_k=top_k,
                boost_url_prefix=playbook_boost,
            )
            debug = OrchestratorDebug(
                intent=decision,
                playbook_debug=retrieval.debug,
            )
            answer = None
            if not no_generate:
                answer = generate_answer(
                    question,
                    retrieval.chunks,
                    playbook_to_app_config(self.playbook_config),
                    answer_lang=answer_lang,
                )
            return OrchestratorResult(
                track="playbook",
                answer=answer,
                chunks_docs=[],
                chunks_industry=[],
                chunks_playbook=retrieval.chunks,
                merged=None,
                debug=debug,
                retrieval=retrieval,
            )

        docs_query = decision.product_query or question
        retrieval = self.docs_retriever.retrieve_with_debug(docs_query, top_k=top_k)
        docs_chunks = list(retrieval.chunks)
        if decision.capability in {
            "permissions",
            "project_create",
            "project_template",
            "workflow",
            "naming",
            "model_viewer",
            "folder",
        }:
            from rag.orchestrator.chunk_pin import (
                load_docs_folder_chunks,
                load_docs_model_viewer_chunks,
                load_docs_naming_chunks,
                prefer_docs_for_capability,
            )

            limit = top_k or len(docs_chunks) or 3
            if decision.capability == "folder":
                preferred = load_docs_folder_chunks(
                    self.docs_config.storage.chunks_path, limit=limit
                )
                if preferred:
                    docs_chunks = preferred
            elif decision.capability == "naming":
                preferred = load_docs_naming_chunks(
                    self.docs_config.storage.chunks_path, limit=limit
                )
                if preferred:
                    docs_chunks = preferred
            elif decision.capability == "model_viewer":
                preferred = load_docs_model_viewer_chunks(
                    self.docs_config.storage.chunks_path, limit=limit
                )
                if preferred:
                    docs_chunks = preferred
            else:
                docs_chunks = prefer_docs_for_capability(
                    decision.capability,
                    docs_chunks,
                    chunks_path=self.docs_config.storage.chunks_path,
                    limit=limit,
                )
            retrieval = RetrievalResult(
                chunks=docs_chunks,
                debug=retrieval.debug,
            )
        debug = OrchestratorDebug(intent=decision, docs_debug=retrieval.debug)
        answer = None
        if not no_generate:
            answer = generate_answer(
                question, docs_chunks, self.docs_config, answer_lang=answer_lang
            )
        return OrchestratorResult(
            track="docs",
            answer=answer,
            chunks_docs=docs_chunks,
            chunks_industry=[],
            chunks_playbook=[],
            merged=None,
            debug=debug,
            retrieval=retrieval,
        )


def format_orchestrator_debug(debug: OrchestratorDebug) -> str:
    intent = debug.intent
    lines = [
        f"intent_track: {intent.track}",
        f"intent_reason: {intent.reason}",
        f"capability: {intent.capability or '-'}",
        f"product_query: {intent.product_query or '-'}",
        f"industry_query: {intent.industry_query or '-'}",
        f"playbook_query: {intent.playbook_query or '-'}",
    ]
    if debug.docs_debug:
        lines.append("--- docs retrieval ---")
        lines.append(f"original_query: {debug.docs_debug.original_query}")
        lines.append(f"adopted_path: {debug.docs_debug.adopted_path}")
        lines.append(f"original_top1_sim: {debug.docs_debug.original_top1_sim}")
    if debug.industry_debug:
        lines.append("--- industry retrieval ---")
        lines.append(f"original_query: {debug.industry_debug.original_query}")
        lines.append(f"adopted_path: {debug.industry_debug.adopted_path}")
        lines.append(f"original_top1_sim: {debug.industry_debug.original_top1_sim}")
    if debug.playbook_debug:
        lines.append("--- playbook retrieval ---")
        lines.append(f"original_query: {debug.playbook_debug.original_query}")
        lines.append(f"adopted_path: {debug.playbook_debug.adopted_path}")
        lines.append(f"original_top1_sim: {debug.playbook_debug.original_top1_sim}")
    if debug.merged:
        lines.append(
            f"merged: hk={len(debug.merged.industry_chunks)} "
            f"playbook={len(debug.merged.playbook_chunks)} "
            f"docs={len(debug.merged.docs_chunks)}"
        )
    if debug.validation_retried:
        lines.append("validation_retried: True")
    if debug.validation_warnings:
        lines.append("--- validation ---")
        lines.extend(debug.validation_warnings)
    return "\n".join(lines)
