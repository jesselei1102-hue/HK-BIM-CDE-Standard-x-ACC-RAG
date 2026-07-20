---
source_file: output/HK Standard/CIC_ZCP_BIMIPv1-5_withAppendices.pdf
doc_id: cic_zcp_bimip_v15
section_id: cic_zcp_bimip_v15_2_7_federation_strategy
title: 2.7. Federation Strategy
page_start: 36
page_end: 36
authority: CIC ZCP BIM Implementation Plan v1.5 §2.7.
authority_type: case_study
normative_weight: reference
discipline: implementation
lifecycle_stage: project
publication_year: 2022
software: null
priority: high
language: en
source_url: hk_cde://cic_zcp_bimip_v15/cic_zcp_bimip_v15_2_7_federation_strategy
---

# 2.7. Federation Strategy

Supply and Installation of Internet of Things (IoT) and Building Information Modelling (BIM) at 
Construction Industry Council - Zero Carbon Park 
BIM Implementation Plan 
 
 
36 
 
 
Parameter Description Data Format in 
Revit Model 
This parameter indicates the OmniClass Table 
23 Products (2012-05-16) number classified for 
the BIM object. 
OmniClass Title Refer to “OmniClass Title” in Equipment List; 
This parameter indicates the OmniClass  Table 
23 Products (2012-05-16) title classified for the 
BIM object. 
Text 
 
Table 18. Additional asset data generated automatically and included in the schedules 
Parameter Description Data Format in 
Revit Model 
CIC.Common.BIMGUID Refer to “C IC.Common.BIMGUID” in 
Equipment List; 
The value of this parameter is generated 
internally “UniqueId” in Revit models. 
Text 
LinkBIMGUID Refer to “LinkBIMGUID” in Equipment List; 
The parameter is a combined parameter 
consisted of Linked File Name and 
CIC.Common.BIMGUID. The data is generated 
automatically in the schedules. 
Planon system requires this parameter for 
mapping the data to the model geometry. 
Text 
 
 Step 4 - Updating the equipment list and SDI template 
The content of the equipment list can be replaced entirely by the newly exported Excel worksheets. 
The updated equipment list will contain the latest data from model and is ready to be transferred 
to the SDI (Standard Data Import) template. Since the SDI template requires data in a specific 
format in  order to transfer data into the Planon system, users must take care to verify the 
formatting of the data before it is input into the SDI template. 
2.7. Federation Strategy 
The approach for federation for the ZCP model is relatively simple due to the limited si ze of the 
project. A master Revit file links the trade Revit files of structure, architecture, and building 
services. Each trade file is a single Revit model. While the model for the landscaping is still under 
discussion at this time, it will most likely b e its own Revit file and will be linked to the master 
Revit file in the same way as the other trade Revit files.
