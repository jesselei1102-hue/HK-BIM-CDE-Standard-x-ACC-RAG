---
source_file: output/HK Standard/CIC BIM for Asset Management and Facility Management
  Case Sharing 2021.pdf
doc_id: cic_amfm_case_2021
section_id: cic_amfm_case_2021_10_workflow_on_logistics_of_information_exchange_data_transfe
title: 10. Workflow on Logistics of Information Exchange / Data Transfer and Mapping
page_start: 26
page_end: 28
authority: CIC AM/FM Case Sharing 2021 §10.
authority_type: case_study
normative_weight: reference
discipline: am_fm
lifecycle_stage: operations
publication_year: 2021
software: null
priority: normal
language: en
source_url: hk_cde://cic_amfm_case_2021/cic_amfm_case_2021_10_workflow_on_logistics_of_information_exchange_data_transfe
---

# 10. Workflow on Logistics of Information Exchange / Data Transfer and Mapping

Page 26 of 46 
 
10. Workflow on Logistics of Information Exchange / Data Transfer 
and Mapping 
 
The following implementation flow chart demonstrates the data flow for information exchange / data 
transfer and mapping. 
 
 
10.1. Equipment List with Model Data and Asset Information 
An equipment list was established and contained all of the asset information in respect with BIM objects. 
This approach required ATAL to input all the necessary information, submitted to the CIC for reviewing 
and commenting. It was approved by the CIC and pas sed to Planon for their further extraction to a 
Standard Data Input (SDI) template before uploading on to the EOMS. 
An example of equipment list as follow:

Page 27 of 46 
 
 
There is a total of 10 major categories agreed between the CIC, ATAL and Planon for the consolidation 
of asset information as follows: 
Abbreviation Asset Group 
AC Air-Conditioning / Ventilation / Exhaust System 
FS Fire Services Installation System 
PD Plumbing and Drainage System 
EL Electrical Distribution System 
LIFT Lift / Escalator Service 
ELV ELV / AV / CCTV System / IoT 
BLDG Building Works 
LAND Landscaping / Green Works 
FE Furniture & Equipment 
OTH Others 
 
10.2. Colour in columns refers to the information related to the respect participants. 
Columns with heading in Orange: Input by the CIC 
 The columns indicate the status when the objects are created in BIM model ( LOD-G) and asset 
information are inserted in the equipment list. 
• BIM Model Include (Y/N) – Determine the object should be created in the BIM Model 
• FM System Include (Y/N) – Determine the object should contain asset information 
Columns with heading in Blue: Input by ATAL 
 The columns indicate the information and status of the production of objects for ATAL’s internal 
reference. 
• CIC_Element ID – An object ID created from Revit 
• Family – A naming management for object 
• Type Name – Object family type 
• Category – Object family category 
• CIC_LOD – Indicate the model element in graphical and geometric representation, same 
principle as LOD-G 
• CIC_Site_Verify – is u sed for indicating objects that are checked with on -site / field 
verification, such as images, 360° image/video, point cloud data 
• CIC_Data_Verify – is used for indicating objects that have catalogue to show its respect 
information from CIC

Page 28 of 46 
 
• Omni Number –  Table 23 OmniClass® classification is used to organise and retrieve 
information, the levels are proposed by ATAL 
• Omni Title – OmniClass® classification title 
Columns with heading in Green: Fields provided by Planon, asset information  provided by the CIC and 
input by ATAL. 
 The columns indicate the information of the objects that would be shown in the EOMS. 
 
10.3. LinkBIMGUID 
LinkBIMGUID is one of the columns that is essential and acts as the linkage between BIM objects and 
the EOMS. This parameter is a combined parameter consisting of Linked File Name (same as Linked File 
GUID) and CIC. Common.BIMGUID (e.g. CIC.Common.BIMGUID in this project 0e307a9b-fcde-494e-
a646-54770657a713-000cd648). Data is generated automatically in the schedu les. EOMS requires this 
parameter for mapping the data to the BIM model geometry. 
 
10.4. Material appearance 
The CIC required the asset BIM viewer (Forge model viewer) in the EOMS to display materials for 
selected assets. Material appearance was a potential issue when mapping from Forge model viewer to 
the EOMS . Some BIM objects were suspected that the material did not successfully attached and 
displayed in the EOMS , it required investigation and resolution by ATAL technical team in a promptly 
duration. 
Without material attached on BIM objects, example: a CIC notice plate. 
An example of a CIC notice plate, with and without material attachment as follow:  
Without material attachment With material attachment
