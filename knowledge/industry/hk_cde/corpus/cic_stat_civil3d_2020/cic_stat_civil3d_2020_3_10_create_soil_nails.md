---
source_file: output/HK Standard/CIC BIM Standard/CIC BIM Standards for Preparation
  of Statutory Plan Submissions Dec2020/Appendix 2 CIC BIM User Guide for Preparation
  of Statutory Plan Submissions Civil 3D Dec2020.pdf
doc_id: cic_stat_civil3d_2020
section_id: cic_stat_civil3d_2020_3_10_create_soil_nails
title: 3.10 Create Soil Nails
page_start: 22
page_end: 22
authority: CIC Statutory Civil 3D Guide 2020 §3.10
authority_type: software_guide
normative_weight: operational
discipline: statutory_submission
lifecycle_stage: statutory
publication_year: 2020
software: Civil 3D
priority: normal
language: en
source_url: hk_cde://cic_stat_civil3d_2020/cic_stat_civil3d_2020_3_10_create_soil_nails
---

# 3.10 Create Soil Nails

16 
 
3.10 Create Soil Nails 
COGO points are used to model soil nails in Civil 3D. 3D soil nails can be created by using dynamo 
with Civil 3D 2020 after the information is filled to the COGO points in Civil 3D. Press the button 
“Ribbon > Home > Create Ground data > Points > Create Points -Surface > Random Points”, then 
select the surface before picking the location of points on the plan view. Adjust the COGO point 
“Style” to “Soil Nail – plan view” and “Point Label Style” to describe only. 
Type “STYLEMANAGER” in the command bar, choose Documentation Objects > Property 
Set Definitions to apply “CIC_Soil Nail” for COGO points. In property menu, choose 
“Extended Data” and add the “CIC_Soil Nail” data set by pressing the  button at the left 
button in property meun. Format of extended data could be customized by users in C3D 
Style Manager.  
 
For Civil 3D 2020 users, they could press “Manage > Dynamo” and open the dynamo “Soil 
Nail to 3D” to generate 3D soil nails based on the information they entered in the COGO 
points.
