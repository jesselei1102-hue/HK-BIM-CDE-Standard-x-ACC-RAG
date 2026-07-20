#!/usr/bin/env bash
# Bootstrap HK CDE + Playbook indexes for a fresh clone (no Docs crawl required).
#
# Usage:
#   bash scripts/bootstrap_indexes.sh
#   bash scripts/bootstrap_indexes.sh --with-docs   # only if output/DOCS exists
#   bash scripts/bootstrap_indexes.sh --skip-ollama-check
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

WITH_DOCS=0
SKIP_OLLAMA=0
for arg in "$@"; do
  case "$arg" in
    --with-docs) WITH_DOCS=1 ;;
    --skip-ollama-check) SKIP_OLLAMA=1 ;;
    -h|--help)
      sed -n '2,10p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown arg: $arg" >&2
      exit 2
      ;;
  esac
done

if [[ ! -d .venv ]]; then
  echo "Creating .venv ..."
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -q -r requirements.txt

PREFLIGHT_ARGS=(--track hk_cde)
if [[ "$SKIP_OLLAMA" -eq 1 ]]; then
  PREFLIGHT_ARGS+=(--skip-ollama)
fi

echo "==> Building HK CDE index (scope=high)"
python scripts/ingest_industry_hk_cde.py --scope high --rebuild
python scripts/build_industry_query_kb.py
python scripts/build_industry_kb_index.py --rebuild

echo "==> Building Playbook index"
python scripts/ingest_playbook_acc_hk.py --rebuild
python scripts/build_playbook_query_kb.py
python scripts/build_playbook_kb_index.py --rebuild

echo "==> Building orchestrator semantic route index"
python scripts/build_orchestrator_route_index.py --rebuild

if [[ "$WITH_DOCS" -eq 1 ]]; then
  if [[ ! -d output/DOCS ]]; then
    echo "ERROR: --with-docs requested but output/DOCS is missing." >&2
    echo "Obtain Autodesk Docs help Markdown legally first." >&2
    exit 1
  fi
  echo "==> Building Docs index"
  python ingest.py --rebuild
  python scripts/build_query_kb.py
  python scripts/build_kb_index.py --rebuild
fi

echo "==> Preflight"
if [[ "$WITH_DOCS" -eq 1 ]]; then
  python -m rag.preflight --track all --require-docs ${SKIP_OLLAMA:+--skip-ollama}
else
  python -m rag.preflight --track all ${SKIP_OLLAMA:+--skip-ollama}
fi

echo
echo "Bootstrap complete."
echo "  HK only:   python ask.py --corpus hk_cde \"What is WIP?\""
echo "  Playbook:  python ask.py --corpus playbook \"WIP folder structure\""
if [[ "$WITH_DOCS" -eq 1 ]]; then
  echo "  Hybrid:    python ask.py --corpus hybrid \"HK CDE folder permissions in ACC\""
else
  echo "  Docs/hybrid: obtain Docs corpus, then re-run with --with-docs"
fi
