---
source_file: output/HK Standard/CIC_ZCP_BIMIPv1-5_withAppendices.pdf
doc_id: cic_zcp_bimip_v15
section_id: cic_zcp_bimip_v15_2_5_3_bim_object_naming_convention
title: 2.5.3. BIM Object Naming Convention
page_start: 24
page_end: 25
authority: CIC ZCP BIM Implementation Plan v1.5 §2.5.3.
authority_type: case_study
normative_weight: reference
discipline: implementation
lifecycle_stage: project
publication_year: 2022
software: null
priority: normal
language: en
source_url: hk_cde://cic_zcp_bimip_v15/cic_zcp_bimip_v15_2_5_3_bim_object_naming_convention
---

# 2.5.3. BIM Object Naming Convention

Supply and Installation of Internet of Things (IoT) and Building Information Modelling (BIM) at 
Construction Industry Council - Zero Carbon Park 
BIM Implementation Plan 
 
 
24 
 
 
2.5.2. Model File Naming Convention 
The model file naming convention refers to the Hong Kong ‘Local Annex’ of ISO 19650-2:2018 
in the CIC BIM Standards - General (Version 2.1 - 2021) and may be modified under the CIC’s 
approval. 
The Revit model files shall be named as below: 
[Project Code ( 1-8)]-[Originator ( 3)]-[Volume (1-3)]-[Location ( 1-4)]-[Discipline ( 1-2)]-
[Type (1-2)_Characteristic (1)]-[Sequential Number (3)].rvt 
Blue text refers to the field length in alphanumeric format 
Green text refers to the field length in alphabetic format 
Red text refers to the field length in numeric format 
 
[Project Code] shall be: ZCP21 
[Originator] shall be: CIC 
[Volume] shall be: C1  
[Location] refers to: Locations within the ZCP project ( VC for the Z ero Carbon Building, 
TER for the Park area) 
[Discipline] refers to: AR for Architectural, ST for Structural, BS for Building Services, FS 
for Fire Services, LA for Landscape 
[Type] shall be: M3 for model files 
[Characteristic] shall be: A for as-built 
[Sequential Number] shall be: 001, 002, 003, etc. if needed 
 
e.g., ZCP21-CIC-C1-VC-AR-M3_A.rvt 
 
2.5.3. BIM Object Naming Convention 
BIM Object  file naming will refer to the CIC Production of Building Information Modelling 
Object Guide: General Requirements (Version 2 - 2021) section 7.1 which also refers to the CIC’s 
Master list of ‘Category’ and ‘Functional Type ’. Each BIM Object name should not exceed 30 
characters, including hyphen marks. 
BIM Objects will be created with the file naming convention below: 
BIM Object File Name:  
[Category]-[Functional Type]-[Originator]-[Descriptor 1]-[Descriptor 2].File Format Extension 
 
[Category] 
a. The category field shall indicate the BIM object category / classification / catalogue based 
on the BIM platform system; 
b. Three capital letters will be used in this field; and 
c. Any new Category code proposed, that this not following the CIC Master Type List, will 
be subject to approval by the Appointing Party. 
[Functional Type] 
a. This field shall indicate the functional type of the BIM Object an d is a subdivision under

Supply and Installation of Internet of Things (IoT) and Building Information Modelling (BIM) at 
Construction Industry Council - Zero Carbon Park 
BIM Implementation Plan 
 
 
25 
 
 
the Category field. See the example from Table 8 below; 
b. Three capital letters will be used in this field - Refer to the CIC Master Type List; 
c. Any new Functional Type code proposed, that this not in the CIC Master Type List, will 
be subject to approval by the Appointing Party; and 
d. When a Functional Type is not necessary, three underscores (___) should be used. 
[Originator] 
a. The originator field shall indicate who owns or creates the BIM object; 
b. Three capital letters will be used in this field; 
c. For BIM objects originating from Works Departments, corresponding department names 
should be used as originator names. However, other consultants or contractors who create 
the new BIM objects should follow Agent Responsible Code (ARC) list for originator. For 
those consultants or contractors, this field shall follow the up-to-date version of the ARC 
published by DEVB under the CAD Standard for Works Projects. ARC full list can be 
referred to this link: 
https://www.devb.gov.hk/en/construction_sector_matters/electronic_services/cad_standard/com
puter_aided_drafting/cad/index.html; and 
d. Any new Originator code proposed, that this not in the CIC Master Type List, will be 
subject to approval by the Appointing Party. 
Descriptors: The descriptor fields shall indicate the critical characteristic of the BIM object. 
[Descriptor 1]:  
a. Descriptor 1 contains information about primary use and material when applicable. 
b. Duplicated information with in the Category and Functional Type will be avoided. For 
example, if category is “WDW” (meaning window), “window” should not be used in this 
field. If functional type is “DBL” (meaning double), then “double” should not be used in 
this field; 
c. Capital letters should be used for first letter of each word (e.g. , WallMounted, 
GlobalValve); 
d. All-capital short forms should be used to indicate materials when applicable (e.g., CONC 
for concrete, WD for Wood). If Descriptor 1 starts with all -capital short form, an 
underscore (_) should be used to separate the short form and the following word (e.g. , 
CONC_Kerb, WD_Slash); 
e. If Descriptor 1 is blank, three unders cores (___) should be used in place of Descriptor 1 
(e.g., SFM-RCB-ACM-___-01.rfa); and 
f. Descriptor 1 should be kept as concise as practicable with a maximum length of 15 
characters in order to reserve space for the potential future expansion of the 2-digit 
sequential number in Descriptor 2 for potential future expansion.  
[Descriptor 2]:  
a. Descriptor 2 is a 2 -digit sequential number (e.g. , 01 to 99) to distinguish different types 
that cannot be sufficiently identified by preceding fields. (e.g., STE-STA-ACM-NB_Pier-
01.rfa)
