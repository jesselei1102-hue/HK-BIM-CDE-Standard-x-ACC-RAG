---
source_file: output/HK Standard/CIC BIM Standard/CIC BIM Standards for Preparation
  of Statutory Plan Submissions Dec2020/Appendix 3 CIC BIM User Guide for Preparation
  of Statutory Plan Submissions Revit Dec2020.pdf
doc_id: cic_stat_revit_2020
section_id: cic_stat_revit_2020_3_getting_start
title: 3 Getting Start
page_start: 13
page_end: 18
authority: CIC Statutory Revit Guide 2020 §3
authority_type: software_guide
normative_weight: operational
discipline: statutory_submission
lifecycle_stage: statutory
publication_year: 2020
software: Revit
priority: normal
language: en
source_url: hk_cde://cic_stat_revit_2020/cic_stat_revit_2020_3_getting_start
---

# 3 Getting Start

7  
3 Getting Start 
In this chapter, it covers how to configure and manage standards through the 
development and use of a project template. This template can be rich with 
information that goes beyond the out of box content that Revit provides. The 
template setting is established and content as well as explain how the reuse 
of wor k will increase productivity and standardi se with each project for 
Building Department submission.
 
1. Open a new project in Revit by the following steps: 
Open Revit ➜ click “New” button ➜ click “Browse” in New Project browser to 
open template (CIC_Template_STR.rte for Superstructure Plans; 
CIC_Template_DML.rte for Demolition Plan; CIC_Template_CVL.rte for 
Hoarding Plan) ➜ click “OK”

8  
2. Create Site Boundary 
In the project browser, click “Site” plan under the Structural Plan of View. 
 
Insert CAD drawing of block plan to the view, click “Insert” ➜ “Link CAD” 
 
Move the CAD link towards the location of the project base point such that point 
A of the site boundary and the project base point is  overlapped. 
 
Open a structural plan in Revit, click “Massing & Site” ➜ “Modify Site” ➜ 
“Property Line” to add property line.

9 
Add site boundary symbol in plan view  (Refer to section 7.1.4 Add annotation 
symbol) 
 
Category Family Type 
Generic 
Annotation 
ANN-GNN-CIC-
Site_Boundary_Mark 
/ 
 
3. Set the project base point (for civil model only): 
Inside Site Plan ➜ Click “Manage” in ribbon ➜ “Project Location” ➜” 
Coordinates”➜ click “Specify Coordinates at Point”. 
Select one of the site boundary point s. In the dialog ue box, type the true 
coordination of the point.

10 
In the same view, select the survey point, click the clip to change its state to 
unclipped. 
 
Move the survey point towards the project base point so that they are 
overlapped. Then click the clip to change its state to clipped.   
 
4. Create a grid and level 
Open a structural plan in Revit, click “Architecture” ➜ “Datum” to create a grid in 
the model according to a specific design. 
 
 
Open an elevation in Revit, click “Architecture” ➜ “Datum” to create a level in 
the model according to a specific design.

11 
5. Acquire a shared coordinate system from the civil model (for structure and demolition 
models only) 
In the project browser, open Level 0 plan under Structural Plan of View. Insert CAD 
drawing of block plan to the view, click “Insert” ➜ “Link CAD” 
 
Move the CAD link towards the location of the project base point such that the 
intersection of Grid A and Grid 1 is placed in the project base point. 
 
 
Create grids and site boundary.

12 
Link civil model file to the view, click “Insert” ➜ “Link Revit” 
 
 
Move and rotate the civil model so that their site boundary and grids are 
overlapped. 
 
 
Select the civil model, in the properties panel, click “Not Shared” in “Shared Site” 
➜ select “Acquire the shared coordinate system form xxx.rvt” - > click 
“Reconcile”. 
 
 
Select the survey point, click the clip to change its state to unclipped.  
 
Move the survey point towards the project base point so that they are 
overlapped. Then click the clip to change its state to clipped.  
Save the project.
