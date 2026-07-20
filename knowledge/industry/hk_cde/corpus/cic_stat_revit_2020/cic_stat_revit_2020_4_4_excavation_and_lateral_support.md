---
source_file: output/HK Standard/CIC BIM Standard/CIC BIM Standards for Preparation
  of Statutory Plan Submissions Dec2020/Appendix 3 CIC BIM User Guide for Preparation
  of Statutory Plan Submissions Revit Dec2020.pdf
doc_id: cic_stat_revit_2020
section_id: cic_stat_revit_2020_4_4_excavation_and_lateral_support
title: 4.4 Excavation and lateral support
page_start: 63
page_end: 68
authority: CIC Statutory Revit Guide 2020 §4.4
authority_type: software_guide
normative_weight: operational
discipline: statutory_submission
lifecycle_stage: statutory
publication_year: 2020
software: Revit
priority: normal
language: en
source_url: hk_cde://cic_stat_revit_2020/cic_stat_revit_2020_4_4_excavation_and_lateral_support
---

# 4.4 Excavation and lateral support

57  
4.4 Excavation and lateral support 
The following objects will be modelled in a foundation plan: 
  Sheet Pile 
  Walling 
  Struct / Tie / Short Struct 
  Stage Topo / Final Topo 
  Basement Wall 
 
4.4.1 Create Sheet Pile 
In the Project Browser, open an existing ground level Click “Structural” in ribbon 
➜ click “Isolated” 
 
In the Properties panel, select family type “SFD-FPL-CIC-Sheet_Pile” ➜ change 
“Offset” to set level ➜ 
Click “Edit Type” to change properties by your own if any 
 
Click “Place on Work Plane” ➜ Drag from starting point to end to create sheet 
pile

58  
 
Repeat the above steps 
 
 
 
4.4.2 Create Walling 
In the Project Browser, open an existing ground level  
Click “Insert” ➜ click “Load Family” ➜ Open “SFM-STB-CIC-UB.rfa” file in 
Browser ➜ click “Open” Remark: repeat the above steps to load different types 
can be loaded into the model 
 
 
Select the required type to load into the project.

59  
 
In Ribbon, click “Structure” ➜ draw walling by dragging starting point to end  
In the Properties panel, select the corresponding type and dimension of walling 
➜ fill in “mark” for identification of element ➜Fill in “ELS_Phase” to identify the 
phasing (i.e. 1,2,3,4 …etc)  
Set cross-section rotation if necessary

60  
 
 
 
 
4.4.3 Create Strut / Short Strut /  Tie 
In Ribbon, click “Structure”  ➜ click “BEAM” ➜ drag from starting point to end to 
create the strut / tie     /short strut 
In the Properties panel, select the  corresponding type and dimension  ➜  select 
the reference level ➜   Fill  in “Mark” for identification of element ➜ Fill in 
“ELS_Phase” to identify the phasing (i.e. 1,2,3,4 …etc .)

61  
Repeat the above steps 
 
 
 
Add Tag in plan view/ section view  (Refer to section 7.1.2 Add Tags –  Tag by 
Category) 
 
Category Family Type 
Structural 
Framing 
ANN-FTG-CIC-
Rectangular 
Standard 
Structural Column ANN-SCG-CIC Mark 
 
 
 
 
4.4.4 Create Stage Topo / Final  Topo 
In Ribbon, click “Massing & Site” ➜ click “Toposurface” ➜ Input surface 
“Elevation” ➜ click “Place Point” on specific elevation ➜ click “Tick” ➜ Repeat 
above steps for different elevations

62  
 
In the Properties panel, fill in “ELS_Phase” and “Name” to identify the phasing 
(i.e. 1,2,3,4 …etc .) and the name of the toposurface (i.e.  1,2,3,4 …etc .). Select 
“Earth” for Material. 
For final excavation toposurface, fill in “Final” for Name and select “Final 
Excavation Level” for Material.
