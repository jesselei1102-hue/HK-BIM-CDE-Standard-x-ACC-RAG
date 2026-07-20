---
source_file: output/HK Standard/CIC BIM for Asset Management and Facility Management
  Case Sharing 2021.pdf
doc_id: cic_amfm_case_2021
section_id: cic_amfm_case_2021_9_model_delivery_standards
title: 9. Model Delivery Standards
page_start: 22
page_end: 25
authority: CIC AM/FM Case Sharing 2021 §9.
authority_type: case_study
normative_weight: reference
discipline: am_fm
lifecycle_stage: operations
publication_year: 2021
software: null
priority: normal
language: en
source_url: hk_cde://cic_amfm_case_2021/cic_amfm_case_2021_9_model_delivery_standards
---

# 9. Model Delivery Standards

Page 22 of 46 
 
9. Model Delivery Standards 
 
9.1. Coordinate System 
The BIM models shall be in HK1980 Grid Coordinates System and refer to Hong Kong Principal Datum. 
The coordinate information were provided by the CIC. 
All BIM models were coordinated with Shared Coordinate System. The Survey Point and Project Base 
Point of models shall be set as below: 
 
Survey Point N/S 819157695.0 
E/W 841001908.0 
Elev 4400.0 
 
 Project Base Point N/S 819154692.5 
E/W 841004397.0 
Elev 4400.0 
Angle to True North 140.34° 
 
9.2. Model Link Diagram 
 
 
The ‘COS Centre’ contains the massing model of the project building, including the building boundary 
line and true coordinates. 
 
9.3. Model File Naming Convention 
The model file naming convention referred to the CIC BIM Standards – General and was customised to 
satisfy project-specific needs and was approved by the CIC. 
The files were named as below: 
 
Revit File Name:  
[Author]-[Zone]-[Level/Location]-[Type]-[Date].rvt 
 
[Author] refers to: CIC

Page 23 of 46 
 
[Zone] refers to: HQ 
[Level/Location] refers to: 38F or 39F 
[Type] refers to: ARC/STR/MEP 
[Date] refers to file date YYYY/MM/DD  
 
e.g. CIC-HQ-38F-ARC-20201231.rvt 
 
9.4. BIM Object Naming Convention 
The BIM object naming convention referred to the CIC Production of BIM Object Guide. All newly created 
functional type were listed out in submission  to the CIC for approval. Each BIM object naming should 
not exceed 30 characters for the entire name, including delimiters but excluding the file extension. 
The BIM objects are created with the naming convention as follow: 
 
Object Name:  
[Category]-[Functional Type]-[Originator]-[Description 1]-[Description 2].rfa 
[Descriptor 1]:  
a. Duplicate information with the Category and Functional Type should be avoided. For example, if 
category is “WDW” (means window), “window” should not be used in this field. If functional type is 
“DBL” (means double), then “double” should not be used in this field. 
b. Capital letters should be used for first letter of each word (e.g. WallMounted, GlobalValve). 
c. All-capital short forms should be used to indicate materials when applicable (e.g. CONC for concrete, 
WD for Wood). If Descriptor 1 starts with all-capital short form, an underscore (_) should be used to 
separate the short form and the following word  (e.g. CONC_Kerb, WD_Slash). 
d. If Descriptor 1 is blank, three nos. of underscores (___) should be used in place of Descriptor 1 (e.g. 
SFM-RCB-ACM-___-01.rfa). 
e. Descriptor 1 should be kept as concise as practicable with the maximum length of 15 characters in 
order to reserve space for 2 digit sequential number in Descriptor 2 for potential future expansion.  
 
[Descriptor 2]:  
a. Descriptor 2 is a 2-digit sequential number (e.g. 01 to 99) to distinguish different types that cannot 
be sufficiently identified by preceding fields. (e.g. STE-STA-ACM-NB_Pier-01.rfa) 
b. If Descriptor 2 is blank, two underscores (__) should be used in place of Descriptor 2. (e.g. PPF-UPV-
ACM-BendSocket-__.rfa) 
 
Type Name: 
Further description shall be added for the controlled parameter, for example dimension, size, model 
type, and mounting method etc ., if necessary. Otherwise, type name shall be equal to the Equipment 
Name or Description in the family name.

Page 24 of 46 
 
 
9.5. Model Color Scheme 
Model color scheme referred to the EMSD BIM-AM Standards and Guidelines v2.0 and was customised 
to satisfy project-specific needs and approved by the CIC. 
No. System Description 
Presentation (2D) Presentation (3D) 
Line 
Weight Line Type R,G,B Color 
Palette 
1 Lift and Escalator Cable 
containment for 
lift and escalator 
0.25 Continuous 128,0,128 
 
2 LV Switchboards Cable 
containment for 
LV Switchboards 
0.35 Divide2 128,128,0 
 
3 Emergency 
Generator 
Cable 
containment for 
Emergency 
Generator 
0.35 Continuous 255,0,64 
 
4 HVAC Exhaust Air Duct 
System 
0.35 Continuous 0,255,0  
Fresh Air Duct 
System 
0.35 Continuous 0,0,255  
Supply Air Duct 
System 
0.35 Continuous 255,0,0  
Return Air Duct 
System 
0.35 Continuous 255,0,255  
Make Up Air 
Duct System 
0.35 Continuous 192,192,192  
Condensate 
Drain Pipe 
System 
0.18 Dashed2 255,128,0 
 
Condensing 
Water Supply 
Pipe System 
0.25 Border2 0,128,64 
 
Condensing 
Water Return 
Pipe System 
0.25 Border2 0,128,255 
 
Make-up Water 
Pipe System 
0.25 Continuous 192,192,192  
5 Fire Services 
Installation 
Sprinkler 0.25 Continuous 255,0,0  
Hose Reel/Fire 
Hydrant 
0.25 Continuous 255,0,0  
Automatic Fire 
Alarm 
0.25 Divide2 255,0,0  
6 Burglar Alarm and 
Security 
Installation 
Cable 
containment for 
Burglar Alarm 
and Security 
Installation 
0.25 Continuous 128,255,255

Page 25 of 46 
 
No. System Description 
Presentation (2D) Presentation (3D) 
Line 
Weight Line Type R,G,B Color 
Palette 
7 PA System  0.25 Continuous 0,128,128  
8 Security System CCTV 0.25 Continuous 255,153,102  
9 Communication 
System 
 0.35 Continuous 128,255,255  
10 Lighting  0.35 Center2 0,255,0  
11 Electrical 
Distribution 
 0.35 Divide2 0,255,0  
12 Plumbing System Cold Water Pipe 
System 
0.25 Long Dash Dash 0,0,255  
Flushing Water 
Pipe System 
0.25 Center 255,255,0  
13 Drainage System  0.35 Divide2 128,128,0  
14 Water Leakage 
Detection System 
Leak Detection 
Cable 
0.35 Continuous 122,48,160
