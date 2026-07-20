---
source_file: output/HK Standard/CIC BIM for Asset Management and Facility Management
  Case Sharing 2021.pdf
doc_id: cic_amfm_case_2021
section_id: cic_amfm_case_2021_11_workflow_of_integrating_bim_and_asset_information_for_am_a
title: 11. Workflow of integrating BIM and Asset Information for AM and FM
page_start: 29
page_end: 31
authority: CIC AM/FM Case Sharing 2021 §11.
authority_type: case_study
normative_weight: reference
discipline: am_fm
lifecycle_stage: operations
publication_year: 2021
software: null
priority: normal
language: en
source_url: hk_cde://cic_amfm_case_2021/cic_amfm_case_2021_11_workflow_of_integrating_bim_and_asset_information_for_am_a
---

# 11. Workflow of integrating BIM and Asset Information for AM and FM

Page 29 of 46 
 
11. Workflow of integrating BIM and Asset Information for AM and 
FM 
 
11.1. Asset Information 
Source of asset information shall be provided by following the Excel templates established and the 
suitability of data format shall be assured before the information is imported into the EOMS. BIM GUID 
with prefix for assets of non-MEP models in the Excel template is required, to highlight new or modified 
assets in the EOMS. Planon would provide the 10 Asset Standard Data Input ( SDI) templates according 
to the 10 major assets categories, and a Space SDI template. CIC would be responsible to fill up with the 
required information and data by copying from the source template to the SDI template.  
11.2. BIM models  
In this particular project, a total of three Revit BIM models, including MEP model (Master model), STR 
and ARC models (Linked models), and combine them in Autodesk Forge format for uploading into the 
EOMS. 
Notes: 
• BIM GUID in the STR and ARC models contains a prefix while that in the MEP models does not. 
• The following data in the Excel templates shall be provided: 
o For assets in STR and ARC  models  BIM GUID with prefix in the BIM GUID column & 
BIM GUID without prefix in the last column  
o For assets in MEP model  BIM GUID without prefix in the BIM GUID column 
BIM models can be viewed under Asset selection level > Asset’s BIM Viewer as shown below:

Page 30 of 46 
 
Below are some of the major fields currently used in the Asset Management in the EOMS. All formats 
and lengths of the fields were confirmed in the project. 
S/n Description System  Name Length S/n Description System  Name Length 
1 Asset Code Code 100 43 Power Source FreeString124 100 
2 BIM GUID BimGuid 100 44 Electrical Power 
Supply 
FreeString3 30 
3 Asset Tag AssetTag 100 45 Current (A) FreeString4 30 
4 IoT Code FreeString122 100 46 Starting Current (A) FreeDecimal5 16 
5 Desciption Name 255 47 Cooling Capacity 
(kW) 
FreeString62 50 
6 Desciption 
(Chinese) 
FreeString61 50 48 Heating Capacity 
(kW) 
FreeString63 50 
7 Translated 
Name 
LangFieldDetail - 49 Refrigerant FreeString100 30 
8 Property PropertyRef 10 50 Air Flow (l/s) FreeString11 30 
9 Space SpaceRef 10 51 Energy label EnergyLabel 10 
10 Asset Group ItemGroupRef 10 52 Motor Power (kW) FreeDecimal11 16 
11 Main Asset ParentRef 10 53 Filter FreeString13 30 
12 Brand Brand 30 54 Service Floor / 
Location 
FreeString111 50 
12 Model / Type Type 30 55 Remarks Comment 100 
13 Model No. FreeString100 30 56 Head (M) FreeDecimal2 16 
14 Serial No. FreeString101 30 57 Total Capacity (kW) FreeString12 30 
15 Dimension (W) 
mm 
FreeString102 30 58 Water Flow (I/s) FreeString14 30 
16 Dimension (L) 
mm 
FreeString103 30 59 Motor Power of 
Pump (kW) 
FreeDecimal3 16 
17 Dimension (H / 
D) mm 
FreeString104 30 60 Nos. of Phase FreeDecimal4 16 
18 Weight FreeString27 30 61 Nos. of Way FreeDecimal6 16 
19 Manufacturer Manufacturer 255 62 Nos. of Pole FreeDecimal7 16 
20 Origin FreeString64 50 63 Rating FreeString15 30 
21 Manual / 
Catalog 
Regulations - 64 Outgoing Circuit FreeString16 30 
22 Product 
Website 
FreeString123 100 65 Accessible Lift FreeString20 30 
23 Supplier FreeString112 50 66 Lift Car No. FreeString17 30 
24 Supplier 
Contract 
FreeString113 50 67 Lift Car Capacity FreeString18 30 
25 Delivery Time FreeString105 30 68 Lift Car Loading FreeString19 30 
26 Maintenance 
Service 
company 
FreeString114 50 69 Material FreeString32 100 
27 Date of 
Handover 
FreeDate1 - 70 FRC / FPR (Hour(s)) FreeDecimal8 16 
28 Date of 
Installation / 
Manufacture 
ConstructionDate - 71 Fire Retardant FreeString21 30 
29 Date first used FirstUsedDate - 72 Class (Fire 
Retardant) 
FreeString22 30 
30 Warranty Start 
Date 
FreeDate2 - 73 Colour FreeString23 30 
32 Warranty End 
Date 
FreeDate3 - 74 Colour Code FreeString24 30

Page 31 of 46 
 
S/n Description System  Name Length S/n Description System  Name Length 
33 Certificate 
Renewal 
FreeString106 30 75 Internal Finish FreeString33 100 
34 Type of 
Certificate 
FreeString107 30 76 External Finish FreeString34 100 
35 Certificate No. FreeString108 30 77 Tree ID FreeString35 100 
36 Certificate 
Renewal 
Interval 
FreeString109 30 78 Tree Assessment 
Records (Form 1) 
FreeString38 100 
37 Certificate 
Validity Period 
FreeString110 30 79 Tree Assessment 
Records (Form 2) 
FreeString41 100 
38 Is planned 
maintenance 
required? 
(Y/N) 
IsPlannedMainten
anceAllowed 
1 80 DLO Records FreeString42 100 
39 Maintenance 
start date 
MaintenanceStart
date 
- 81 Slope / Retaining 
Wall No. 
FreeString25 30 
40 Maintenance 
end date 
MaintenanceEndd
ate 
- 82 Category (1, 2 or 3) FreeString26 30 
41 Maintenance 
Period 
FreeString1 30 83 Frequency of 
Engineer Inspection 
FreeString43 100 
42 Term 
Maintenance 
Contract Item 
No. 
FreeString2 30 84 Handle by 
Department 
FreeString44 100 
 
11.3. CAD drawings  
CAD drawing s generated from the BIM model was required for Planon to import  into the Space & 
Workspaces.  The CAD drawings include the polylines in the following CAD layers: 
1. Floor polyline  50-gross, 51-net 
2. Space polyline  70-spaces 
3. Space data  71-spaces_data (this layer would be put into the Space Block, which contains the 
Space Name and Space Number attributes) 
Example:  
 
Guidance Note: CAD/ 2D drawings may not be required, subject to the needs of the operation team.
