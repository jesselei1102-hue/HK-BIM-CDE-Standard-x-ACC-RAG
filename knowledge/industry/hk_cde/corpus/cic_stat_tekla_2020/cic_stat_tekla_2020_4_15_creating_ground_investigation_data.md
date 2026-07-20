---
source_file: output/HK Standard/CIC BIM Standard/CIC BIM Standards for Preparation
  of Statutory Plan Submissions Dec2020/Appendix 4 CIC BIM User Guide for Preparation
  of Statutory Plan Submissions Tekla Dec2020.pdf
doc_id: cic_stat_tekla_2020
section_id: cic_stat_tekla_2020_4_15_creating_ground_investigation_data
title: 4.15 Creating Ground Investigation Data
page_start: 29
page_end: 32
authority: CIC Statutory Tekla Guide 2020 §4.15
authority_type: software_guide
normative_weight: operational
discipline: statutory_submission
lifecycle_stage: statutory
publication_year: 2020
software: Tekla
priority: normal
language: en
source_url: hk_cde://cic_stat_tekla_2020/cic_stat_tekla_2020_4_15_creating_ground_investigation_data
---

# 4.15 Creating Ground Investigation Data

23 
 
4.15 Creating Ground Investigation Data  
 
Rock core samples from the bored hole and standard penetration tests results are needed to be 
modelled in 3D for drawing production. A Grasshopper script could be downloaded from the CIC 
website to facilitate users to model this information in 3D.

24 
 
First users need to organise GI data in Excel as shown in the picturesm below for rock core samples 
in the bored hole and SPT results.  Name

25 
 
Second, after installing Rhino6 , users could type “Grasshopper” on the command bar to open 
Grasshopper. After Grasshopper is opened, go to “File” at the top left cor ner and choose “Open 
Document” to open the “Tekla_GI Rock Core.gh” file to open the script.

26 
 
After the “Tekla_GI Rock Core.gh” file is opened, right-click at the “File Path Component” and choose 
the Excel file the user had prepared for rock core samples. Then right-click at the “Tekla Column 
Component” at the right and choose “Bake to Tekla” to create 3D geometries in Tekla. Those 3D 
geometries created should be assigned to the “GI” Tekla phase and could be used for 2D drawing 
production.    
 
For SPT information, open the “Tekla GI_SPT.gh” file, right-click at the “File Path Component” and 
choose the Excel file the user had prepared for SPT information and then bake those 3D object to 
Tekla by using the same method as mentioned above.
