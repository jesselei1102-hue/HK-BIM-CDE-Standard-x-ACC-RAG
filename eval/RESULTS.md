# Eval Results

Generated: `2026-07-14T07:02:18.881957+00:00`

Baseline proof that **hybrid** covers Docs + HK CDE + Playbook on cross-domain cases, while forced single-track modes cannot.

## Suite summary

| Suite | Result | Exit |
|-------|--------|------|
| `query_kb` | **PASS** | 0 |
| `hk_cde` | **PASS** | 0 |
| `playbook` | **PASS** | 0 |
| `hybrid` | **PASS** | 0 |
| `hybrid_vs_single` | **PASS** | 0 |

## Hybrid vs single-track (hybrid expect cases)

Cases: **6** (`eval/hybrid_cases.jsonl`)

| Mode | Docs hit | HK CDE hit | Playbook hit | DualRecall | TripleRecall |
|------|----------|------------|--------------|------------|--------------|
| `docs` | 5/6 | 0/6 | 0/6 | 0.0% | 0.0% |
| `hk_cde` | 0/6 | 6/6 | 0/6 | 0.0% | 0.0% |
| `playbook` | 0/6 | 0/6 | 6/6 | 0.0% | 0.0% |
| `hybrid` | 6/6 | 6/6 | 6/6 | 100.0% | 100.0% |

### Verdict

- Hybrid beats best single-track on TripleRecall: **True**
- Hybrid ≥ best single-track on DualRecall: **True**
- Gate: **PASS**

## Raw outputs

### `query_kb`

```
评测用例：20 条
------------------------------------------------------------------------
[OK] [KB✓] 设置权限
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions
       path:     kb_rewrite sim=0.48253268003463745 kb=folder_permissions_set
[OK] [KB✓] 文件夹权限
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions
       path:     original sim=0.5962129235267639 kb=-
[OK] [KB✓] 审批
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews_Create_Edit
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews_Create_Edit
       path:     kb_rewrite sim=0.4976852536201477 kb=approval_workflow_config
[OK] [KB✓] 审阅
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews_Create_Edit
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews_Create_Edit
       path:     kb_rewrite sim=0.5531103610992432 kb=approval_workflow_config
[OK] [KB✓] 附函
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Create_Transmittal
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Create_Transmittal
       path:     kb_rewrite sim=0.4904695153236389 kb=create_transmittal
[OK] [KB✓] 传送件
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Create_Transmittal
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Create_Transmittal
       path:     kb_rewrite sim=0.5407608151435852 kb=create_transmittal
[OK] [KB✓] 支持格式
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Supported_Files_Docs
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Supported_Files_Docs
       path:     kb_rewrite sim=0.4407714009284973 kb=supported_files
[OK] [KB✓] 文件大小
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Product_Limitations
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Product_Limitations
       path:     kb_rewrite sim=0.46952974796295166 kb=file_size_limit
[OK] [KB✓] 支持浏览器
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=System_Requirements_ACC
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=System_Requirements_ACC
       path:     kb_boost sim=0.48735618591308594 kb=supported_browsers
[OK] [KB✓] 公开链接
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Share_files
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Share_files
       path:     kb_rewrite sim=0.45463985204696655 kb=share_files
[OK] [KB✓] 上传
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Upload_files
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Upload_files
       path:     kb_boost sim=0.5032068490982056 kb=upload_files
[OK] [KB✓] 标记
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Markups_Files_Docs
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Markups_Files_Docs
       path:     kb_rewrite sim=0.47994089126586914 kb=markups
[OK] [KB✓] 命名标准
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Set_Up_Naming_Standard
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Set_Up_Naming_Standard
       path:     original sim=0.5544769167900085 kb=-
[OK] [KB✓] 活动日志
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Project_Activity_Log
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Project_Activity_Log
       path:     kb_boost sim=0.502344012260437 kb=activity_log
[OK] [KB✓] 如何设置文件夹权限
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions
       path:     original sim=0.6024138927459717 kb=-
[OK] [KB✓] Autodesk Docs 中单个文件最大可以多大？
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Product_Limitations
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Product_Limitations
       path:     original sim=0.6924505233764648 kb=-
[OK] [KB✓] What browsers are supported for Autodesk Construction Cloud?
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=System_Requirements_ACC
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=System_Requirements_ACC
       path:     original sim=0.7171584367752075 kb=-
[OK] [KB✓] 如何在 Docs 里创建 transmittal？
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Create_Transmittal
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Transmittals
       path:     original sim=0.734486997127533 kb=-
[OK] [KB✓] approval workflow
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews_Create_Edit
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews_Create_Edit
       path:     kb_rewrite sim=0.6648216247558594 kb=approval_workflow_config
[OK] [KB✓] transmittal
       expected: https://help.autodesk.com/view/DOCS/ENU/?guid=Create_Transmittal
       got:      https://help.autodesk.com/view/DOCS/ENU/?guid=Create_Transmittal
       path:     kb_boost sim=0.5843551754951477 kb=create_transmittal
------------------------------------------------------------------------
ShortQueryRecall@1: 20/20 (100.0%)
KB触发准确率:       20/20 (100.0%)
无KB误改写率:       0/20 (0.0%)
```

### `hk_cde`

```
HK CDE Eval
  cases: 26
  SectionRecall@1: 95.7% (22/23)
  industry route accuracy: 82.6% (19/23)
  docs false positive (industry steal): 0
PASS
```

### `playbook`

```
Playbook Eval
  cases: 8
  intent accuracy: 100.0% (8/8)
  playbook recall: 100.0% (6/6)
  hybrid triple recall: 100.0% (2/2)
PASS
```

### `hybrid`

```
Hybrid Orchestrator Eval
  cases: 12
  intent accuracy: 100.0% (12/12)
  DualRecall: 100.0% (6/6)
  TripleRecall(+playbook): 100.0% (6/6)
  false hybrid (pure-track stolen): 0
PASS
```

### `hybrid_vs_single`

```
Hybrid vs Single-Track Coverage
  hybrid expect cases: 6
  mode           docs   hk_cde   playbook  DualRecall  TripleRecall
  docs       5/ 6 0/ 6 0/   6       0.0%         0.0%
  hk_cde     0/ 6 6/ 6 0/   6       0.0%         0.0%
  playbook   0/ 6 0/ 6 6/   6       0.0%         0.0%
  hybrid     6/ 6 6/ 6 6/   6     100.0%       100.0%

  Verdict: hybrid TripleRecall 100.0% vs best single-track 0.0%; hybrid DualRecall 100.0% vs best single-track 0.0%
  wrote eval/results/hybrid_vs_single.json
PASS
```

## How to re-run

```bash
source .venv/bin/activate
python scripts/run_eval_suite.py
# optional: also check generated section headers (slow)
python scripts/eval_hybrid.py --generate
```
