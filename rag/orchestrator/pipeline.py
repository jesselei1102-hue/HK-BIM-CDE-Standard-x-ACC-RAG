#!/usr/bin/env python3
"""三轨编排：分类 → 单轨或并行检索 → 生成。"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from time import perf_counter

from rag.config import AppConfig, get_config
from rag.conversation import ConversationSession, ConversationTurn
from rag.generation import Answer, generate_answer, generate_hybrid_answer
from rag.industry_hk.config import IndustryHKConfig, get_industry_hk_config
from rag.industry_hk.retrieval import IndustryHybridRetriever
from rag.orchestrator.classify import (
    CAPABILITY_PLAYBOOK_URL_PREFIX,
    playbook_url_prefix_for,
    IntentDecision,
    classify_intent,
    classify_intent_legacy,
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
    original_question: str | None = None
    rewritten_query: str | None = None
    is_follow_up: bool = False
    track_hint: str | None = None
    source_hints: list[str] = field(default_factory=list)
    rewrite_reason: str | None = None
    latency_ms: dict[str, float] = field(default_factory=dict)
    semantic_route: dict | None = None
    routing_ab: dict | None = None

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
    suggested_followups: list[str] = field(default_factory=list)


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

    def _retrieval_query(self, question: str, decision: IntentDecision, track_query: str | None) -> str:
        """原问句主导；行业 overview 改写或语义 hint 例外。"""
        if track_query and "overview_rewrite" in decision.reason:
            return track_query
        if decision.semantic_hint and decision.semantic_hint.casefold() not in question.casefold():
            return f"{question.strip()} ({decision.semantic_hint.strip()})"
        if decision.routing_source in {"semantic", "semantic_fallback"} and track_query:
            return track_query
        return question.strip()

    def _retrieval_quality_low(
        self,
        chunks: list,
        *,
        min_sim: float,
    ) -> bool:
        if not chunks:
            return True
        top_sim = getattr(chunks[0], "vector_similarity", None)
        if top_sim is None:
            return False
        return float(top_sim) < min_sim

    def _pick_playbook_chunks(
        self,
        *,
        question: str,
        decision: IntentDecision,
        playbook_query: str,
        playbook_top: int,
        playbook_boost: str | None,
        source_hint_urls: list[str] | None = None,
    ) -> list:
        folderish = is_folder_question(question, decision.capability)
        pin_threshold = self.docs_config.semantic_router.pin_min_top1_sim

        result = self.playbook_retriever.retrieve_with_debug(
            playbook_query,
            playbook_top,
            boost_url_prefix=playbook_boost,
            source_hint_urls=source_hint_urls,
        )
        chunks = list(result.chunks)
        self._last_playbook_debug = result.debug

        if not folderish:
            return chunks

        needs_pin = self._retrieval_quality_low(chunks, min_sim=pin_threshold)
        if chunks:
            from rag.orchestrator.playbook_pin import playbook_chunk_needs_folder_pin

            needs_pin = needs_pin or playbook_chunk_needs_folder_pin(chunks[0])

        if not needs_pin:
            return chunks

        from rag.orchestrator.playbook_pin import load_wip_folder_chunk

        hard = load_wip_folder_chunk(self.playbook_config.storage.chunks_path)
        if hard is not None:
            return [hard]

        wider = self.playbook_retriever.retrieve_with_debug(
            f"{question.strip()} 01_WIP 02_Shared folder tree",
            max(playbook_top, 6),
            boost_url_prefix=playbook_boost
            or CAPABILITY_PLAYBOOK_URL_PREFIX["folder"],
            source_hint_urls=source_hint_urls,
        ).chunks
        for chunk in wider:
            if any(
                marker in chunk.source_url
                for marker in (
                    "11_buildings_folders_permissions",
                    "21_civil_folders_permissions",
                )
            ) and ("01_WIP" in chunk.text or "Team_" in chunk.text):
                return [chunk]
        for chunk in wider:
            if "01_WIP" in chunk.text and (
                "02_SHARED" in chunk.text or "02_Shared" in chunk.text
            ):
                return [chunk]
        return chunks

    def classify(self, question: str) -> IntentDecision:
        return classify_intent(question)

    def retrieve_hybrid(
        self,
        question: str,
        intent: IntentDecision | None = None,
        *,
        top_k: int | None = None,
        source_hint_urls: list[str] | None = None,
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

        product_query = self._retrieval_query(
            question, decision, decision.product_query
        )
        industry_query = self._retrieval_query(
            question, decision, decision.industry_query
        )
        playbook_query = self._retrieval_query(
            question, decision, decision.playbook_query
        )
        pin_threshold = self.docs_config.semantic_router.pin_min_top1_sim
        playbook_boost = playbook_url_prefix_for(
            decision.capability, question
        )
        if is_folder_question(question, decision.capability):
            playbook_boost = playbook_url_prefix_for("folder", question)

        with ThreadPoolExecutor(max_workers=3) as pool:
            docs_future = pool.submit(
                self.docs_retriever.retrieve_with_debug,
                product_query,
                docs_top,
                source_hint_urls=source_hint_urls,
            )
            industry_future = pool.submit(
                self.industry_retriever.retrieve_with_debug,
                industry_query,
                industry_top,
                source_hint_urls=source_hint_urls,
            )
            playbook_future = pool.submit(
                self._pick_playbook_chunks,
                question=question,
                decision=decision,
                playbook_query=playbook_query,
                playbook_top=playbook_top,
                playbook_boost=playbook_boost,
                source_hint_urls=source_hint_urls,
            )
            docs_result = docs_future.result()
            industry_result = industry_future.result()
            playbook_chunks = playbook_future.result()

        folderish = is_folder_question(question, decision.capability)
        docs_chunks = list(docs_result.chunks)
        docs_low = self._retrieval_quality_low(docs_chunks, min_sim=pin_threshold)

        if folderish and docs_low:
            from rag.orchestrator.chunk_pin import load_docs_folder_chunks

            pinned_docs = load_docs_folder_chunks(
                self.docs_config.storage.chunks_path,
                limit=docs_top,
            )
            if pinned_docs:
                docs_chunks = pinned_docs
        elif decision.capability == "naming" and docs_low:
            from rag.orchestrator.chunk_pin import load_docs_naming_chunks

            pinned_docs = load_docs_naming_chunks(
                self.docs_config.storage.chunks_path,
                limit=docs_top,
            )
            if pinned_docs:
                docs_chunks = pinned_docs
        elif decision.capability == "model_viewer" and docs_low:
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
        } and docs_low:
            from rag.orchestrator.chunk_pin import prefer_docs_for_capability

            docs_chunks = prefer_docs_for_capability(
                decision.capability,
                docs_chunks,
                chunks_path=self.docs_config.storage.chunks_path,
                limit=docs_top,
            )

        playbook_result_debug = getattr(
            self, "_last_playbook_debug", None
        ) or self.playbook_retriever.last_debug

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

    def _attach_guidance_warning(
        self,
        question: str,
        answer: Answer | None,
        debug: OrchestratorDebug,
        *,
        capability: str | None = None,
    ) -> None:
        if answer is None:
            return
        from rag.orchestrator.validate import check_answer_guidance

        issue = check_answer_guidance(
            question,
            answer.answer,
            require_howto=True if capability else None,
        )
        if issue is None:
            return
        warnings = list(debug.validation_warnings or [])
        warnings.append(f"[{issue.severity}] {issue.code}: {issue.message}")
        debug.validation_warnings = warnings

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
        rewritten_query: str | None = None,
        conversation_context: str | None = None,
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
                structured_text,
                merged,
                capability=capability,
                question=question,
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

        answer = generate_hybrid_answer(
            question,
            merged,
            self.docs_config,
            answer_lang=answer_lang,
            rewritten_query=rewritten_query,
            conversation_context=conversation_context,
        )
        validation = validate_hybrid_answer(
            answer.answer,
            merged,
            capability=capability,
            question=question,
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
            question,
            retry_merged,
            self.docs_config,
            answer_lang=answer_lang,
            rewritten_query=rewritten_query,
            conversation_context=conversation_context,
        )
        retry_validation = validate_hybrid_answer(
            retry_answer.answer,
            retry_merged,
            capability=capability,
            question=question,
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
        session: ConversationSession | None = None,
        record_turn: bool = True,
    ) -> OrchestratorResult:
        from rag.generation import Answer
        from rag.orchestrator.capabilities_help import (
            build_capabilities_help,
            is_capabilities_help_question,
        )
        from rag.orchestrator.followup import (
            rewrite_followup_query,
            turns_as_untrusted_context,
        )

        original_question = (question or "").strip()
        latency_ms: dict[str, float] = {}
        routing_ab: dict | None = None
        semantic_route: dict | None = None
        t_all = perf_counter()
        t0 = perf_counter()
        standalone = rewrite_followup_query(
            original_question,
            session,
            config=self.docs_config,
        )
        latency_ms["rewrite"] = (perf_counter() - t0) * 1000.0
        retrieval_question = (standalone.query or original_question).strip()
        source_hints = list(standalone.source_hints or [])
        conversation_context = ""
        if session is not None and not session.empty:
            conversation_context = turns_as_untrusted_context(session.recent_turns())

        def _annotate(debug: OrchestratorDebug) -> OrchestratorDebug:
            debug.original_question = original_question
            debug.rewritten_query = retrieval_question
            debug.is_follow_up = bool(standalone.is_follow_up)
            debug.track_hint = standalone.track_hint
            debug.source_hints = list(source_hints)
            debug.rewrite_reason = standalone.rewrite_reason
            merged_latency = dict(latency_ms)
            merged_latency.update(debug.latency_ms or {})
            if "total" not in merged_latency:
                merged_latency["total"] = (perf_counter() - t_all) * 1000.0
            debug.latency_ms = merged_latency
            debug.routing_ab = routing_ab
            debug.semantic_route = semantic_route
            return debug

        def _finish(result: OrchestratorResult) -> OrchestratorResult:
            _annotate(result.debug)
            if (
                result.track not in {"meta", "out_of_domain"}
                and getattr(self.docs_config, "suggest_followups", True)
            ):
                from rag.orchestrator.suggest_followups import suggest_followups

                suggestions = suggest_followups(
                    question=original_question,
                    answer=result.answer.answer if result.answer else None,
                    track=result.track,
                    capability=result.debug.intent.capability,
                    chunks_docs=result.chunks_docs,
                    chunks_industry=result.chunks_industry,
                    chunks_playbook=result.chunks_playbook,
                    merged=result.merged,
                    limit=getattr(self.docs_config, "suggest_followups_count", 3),
                    answer_lang=answer_lang,
                )
                result.suggested_followups = list(suggestions.questions)
            if (
                record_turn
                and session is not None
                and not no_generate
                and result.track != "meta"
            ):
                self._record_conversation_turn(
                    session,
                    original_question=original_question,
                    rewritten_query=retrieval_question,
                    result=result,
                )
            return result

        if is_capabilities_help_question(original_question):
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
                + build_capabilities_help(
                    question=original_question, answer_lang=answer_lang
                )
                if no_generate
                else build_capabilities_help(
                    question=original_question, answer_lang=answer_lang
                )
            )
            return _finish(
                OrchestratorResult(
                    track="meta",
                    answer=Answer(
                        question=original_question,
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
            )

        # Classify / force-track against the standalone retrieval question.
        q = retrieval_question
        from rag.orchestrator.semantic_router import get_semantic_router

        semantic_result = get_semantic_router(self.docs_config).route(q)
        legacy_decision = classify_intent_legacy(q)
        semantic_route = {
            "capability": semantic_result.capability,
            "capability_confident": semantic_result.capability_confident,
            "capability_score": semantic_result.capability_score,
            "capability_margin": semantic_result.capability_margin,
            "track": semantic_result.track,
            "track_confident": semantic_result.track_confident,
            "product_score": semantic_result.product_score,
            "industry_score": semantic_result.industry_score,
            "playbook_score": semantic_result.playbook_score,
            "latency_ms": semantic_result.latency_ms,
            "index_available": semantic_result.index_available,
            "fallback_reason": semantic_result.fallback_reason,
        }
        routing_ab = {
            "mode": self.docs_config.semantic_router.mode,
            "semantic_track": semantic_result.track,
            "semantic_capability": semantic_result.capability,
            "legacy_track": legacy_decision.track,
            "legacy_capability": legacy_decision.capability,
        }
        if force_track == "docs":
            capability = detect_capability(q)
            decision = IntentDecision(
                track="docs",
                capability=capability.key if capability else None,
                product_query=(capability.product_query if capability else q),
                industry_query=None,
                playbook_query=None,
                has_product_signal=True,
                has_industry_signal=False,
                has_playbook_signal=False,
                reason="forced_docs",
            )
        elif force_track == "hk_cde":
            from rag.orchestrator.classify import rewrite_industry_overview_query

            capability = detect_capability(q)
            rewritten = rewrite_industry_overview_query(q)
            decision = IntentDecision(
                track="hk_cde",
                capability=capability.key if capability else None,
                product_query=None,
                industry_query=(
                    capability.industry_query if capability else (rewritten or q)
                ),
                playbook_query=None,
                has_product_signal=False,
                has_industry_signal=True,
                has_playbook_signal=False,
                reason="forced_hk_cde",
            )
        elif force_track == "playbook":
            capability = detect_capability(q)
            decision = IntentDecision(
                track="playbook",
                capability=capability.key if capability else None,
                product_query=None,
                industry_query=None,
                playbook_query=(capability.playbook_query if capability else q),
                has_product_signal=False,
                has_industry_signal=False,
                has_playbook_signal=True,
                reason="forced_playbook",
            )
        elif force_track == "hybrid":
            decision = classify_intent(q)
            if decision.track != "hybrid":
                from rag.orchestrator.classify import (
                    _fallback_queries,
                    capability_template_by_key,
                )

                capability = detect_capability(q) or (
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
                    product_query, industry_query, playbook_query = _fallback_queries(q)
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
            decision = classify_intent(q)
            # Soft track hint from follow-up rewriter:
            # ambiguous / same-topic follow-up without clear new-domain signals.
            if (
                standalone.is_follow_up
                and standalone.track_hint
                and decision.track in {"docs", "hk_cde", "playbook"}
                and standalone.track_hint != decision.track
                and standalone.track_hint in {"docs", "hk_cde", "playbook", "hybrid"}
            ):
                # Keep classifier result when it has strong opposing signals.
                pass

        gen_kwargs = {
            "answer_lang": answer_lang,
            "rewritten_query": retrieval_question,
            "conversation_context": conversation_context or None,
        }

        if decision.track == "hybrid":
            t_ret = perf_counter()
            result = self.retrieve_hybrid(
                q,
                decision,
                top_k=top_k,
                source_hint_urls=source_hints or None,
            )
            latency_ms["retrieve"] = (perf_counter() - t_ret) * 1000.0
            if no_generate:
                return _finish(result)
            t_gen = perf_counter()
            finished = self._generate_hybrid_with_validation(
                original_question,
                result,
                **gen_kwargs,
            )
            latency_ms["generate"] = (perf_counter() - t_gen) * 1000.0
            return _finish(finished)

        if decision.track == "hk_cde":
            t_ret = perf_counter()
            retrieval = self.industry_retriever.retrieve_with_debug(
                decision.industry_query or q,
                top_k=top_k,
                source_hint_urls=source_hints or None,
            )
            latency_ms["retrieve"] = (perf_counter() - t_ret) * 1000.0
            debug = OrchestratorDebug(
                intent=decision,
                industry_debug=retrieval.debug,
            )
            answer = None
            if not no_generate:
                t_gen = perf_counter()
                answer = generate_answer(
                    original_question,
                    retrieval.chunks,
                    self.industry_config,  # type: ignore[arg-type]
                    **gen_kwargs,
                )
                latency_ms["generate"] = (perf_counter() - t_gen) * 1000.0
                self._attach_guidance_warning(
                    original_question,
                    answer,
                    debug,
                    capability=decision.capability,
                )
            return _finish(
                OrchestratorResult(
                    track="hk_cde",
                    answer=answer,
                    chunks_docs=[],
                    chunks_industry=retrieval.chunks,
                    chunks_playbook=[],
                    merged=None,
                    debug=debug,
                    retrieval=retrieval,
                )
            )

        if decision.track == "playbook":
            playbook_boost = playbook_url_prefix_for(
                decision.capability, q
            )
            t_ret = perf_counter()
            retrieval = self.playbook_retriever.retrieve_with_debug(
                decision.playbook_query or q,
                top_k=top_k,
                boost_url_prefix=playbook_boost,
                source_hint_urls=source_hints or None,
            )
            latency_ms["retrieve"] = (perf_counter() - t_ret) * 1000.0
            debug = OrchestratorDebug(
                intent=decision,
                playbook_debug=retrieval.debug,
            )
            answer = None
            if not no_generate:
                t_gen = perf_counter()
                answer = generate_answer(
                    original_question,
                    retrieval.chunks,
                    playbook_to_app_config(self.playbook_config),
                    **gen_kwargs,
                )
                latency_ms["generate"] = (perf_counter() - t_gen) * 1000.0
                self._attach_guidance_warning(
                    original_question,
                    answer,
                    debug,
                    capability=decision.capability,
                )
            return _finish(
                OrchestratorResult(
                    track="playbook",
                    answer=answer,
                    chunks_docs=[],
                    chunks_industry=[],
                    chunks_playbook=retrieval.chunks,
                    merged=None,
                    debug=debug,
                    retrieval=retrieval,
                )
            )

        docs_query = decision.product_query or q
        t_ret = perf_counter()
        retrieval = self.docs_retriever.retrieve_with_debug(
            docs_query,
            top_k=top_k,
            source_hint_urls=source_hints or None,
        )
        latency_ms["retrieve"] = (perf_counter() - t_ret) * 1000.0
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
            t_gen = perf_counter()
            answer = generate_answer(
                original_question,
                docs_chunks,
                self.docs_config,
                **gen_kwargs,
            )
            latency_ms["generate"] = (perf_counter() - t_gen) * 1000.0
            self._attach_guidance_warning(
                original_question,
                answer,
                debug,
                capability=decision.capability,
            )
        return _finish(
            OrchestratorResult(
                track="docs",
                answer=answer,
                chunks_docs=docs_chunks,
                chunks_industry=[],
                chunks_playbook=[],
                merged=None,
                debug=debug,
                retrieval=retrieval,
            )
        )

    @staticmethod
    def _collect_turn_sources(
        result: OrchestratorResult,
    ) -> tuple[list[str], list[str]]:
        urls: list[str] = []
        titles: list[str] = []
        seen: set[str] = set()

        def _add(url: str, title: str) -> None:
            if not url or url in seen:
                return
            seen.add(url)
            urls.append(url)
            titles.append(title or url)

        if result.merged is not None:
            for item in result.merged.tracked:
                _add(item.chunk.source_url, item.chunk.title)
        else:
            for chunk in (
                list(result.chunks_docs)
                + list(result.chunks_industry)
                + list(result.chunks_playbook)
            ):
                _add(getattr(chunk, "source_url", ""), getattr(chunk, "title", ""))
        return urls, titles

    def _record_conversation_turn(
        self,
        session: ConversationSession,
        *,
        original_question: str,
        rewritten_query: str,
        result: OrchestratorResult,
    ) -> None:
        answer_text = ""
        if result.answer is not None:
            answer_text = result.answer.answer or ""
        urls, titles = self._collect_turn_sources(result)
        session.append(
            ConversationTurn(
                user_question=original_question,
                rewritten_query=rewritten_query,
                answer=answer_text,
                track=result.track,
                source_urls=urls,
                source_titles=titles,
            )
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
    if debug.original_question or debug.rewritten_query:
        lines.append(f"original_question: {debug.original_question or '-'}")
        lines.append(f"rewritten_query: {debug.rewritten_query or '-'}")
        lines.append(f"is_follow_up: {debug.is_follow_up}")
        lines.append(f"rewrite_reason: {debug.rewrite_reason or '-'}")
        lines.append(f"track_hint: {debug.track_hint or '-'}")
        lines.append(
            "source_hints: "
            + (", ".join(debug.source_hints) if debug.source_hints else "-")
        )
    if debug.latency_ms:
        parts = [
            f"{key}={value:.0f}ms"
            for key, value in sorted(debug.latency_ms.items())
        ]
        lines.append("latency: " + ", ".join(parts))
    if debug.docs_debug:
        lines.append("--- docs retrieval ---")
        lines.append(f"original_query: {debug.docs_debug.original_query}")
        lines.append(f"adopted_path: {debug.docs_debug.adopted_path}")
        lines.append(f"original_top1_sim: {debug.docs_debug.original_top1_sim}")
        if debug.docs_debug.source_hint_hits:
            lines.append(
                "source_hint_hits: " + ", ".join(debug.docs_debug.source_hint_hits)
            )
    if debug.industry_debug:
        lines.append("--- industry retrieval ---")
        lines.append(f"original_query: {debug.industry_debug.original_query}")
        lines.append(f"adopted_path: {debug.industry_debug.adopted_path}")
        lines.append(f"original_top1_sim: {debug.industry_debug.original_top1_sim}")
        if debug.industry_debug.source_hint_hits:
            lines.append(
                "source_hint_hits: "
                + ", ".join(debug.industry_debug.source_hint_hits)
            )
    if debug.playbook_debug:
        lines.append("--- playbook retrieval ---")
        lines.append(f"original_query: {debug.playbook_debug.original_query}")
        lines.append(f"adopted_path: {debug.playbook_debug.adopted_path}")
        lines.append(f"original_top1_sim: {debug.playbook_debug.original_top1_sim}")
        if debug.playbook_debug.source_hint_hits:
            lines.append(
                "source_hint_hits: "
                + ", ".join(debug.playbook_debug.source_hint_hits)
            )
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
