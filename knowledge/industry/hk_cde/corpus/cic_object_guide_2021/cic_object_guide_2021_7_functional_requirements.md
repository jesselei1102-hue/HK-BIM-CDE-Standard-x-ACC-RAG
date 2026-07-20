---
source_file: output/HK Standard/CIC BIM Standard/CIC Production of BIM Object Guide
  - General Requirements (2021).pdf
doc_id: cic_object_guide_2021
section_id: cic_object_guide_2021_7_functional_requirements
title: 7 Functional Requirements
page_start: 16
page_end: 17
authority: CIC BIM Object Guide 2021 §7
authority_type: standard
normative_weight: recommended
discipline: bim_objects
lifecycle_stage: project
publication_year: 2021
software: null
priority: high
language: en
source_url: hk_cde://cic_object_guide_2021/cic_object_guide_2021_7_functional_requirements
---

# 7 Functional Requirements

CIC PRODUCTION OF BIM OBJECT GUIDE 
13 
7 Functional Requirements 
This section defines functional requirements of BIM objects, including BIM object naming conventions and expected behaviour. 
 
7.1 Naming Conventions 
1. BIM objects shall be named systematically and logically for the understanding of users and for easy BIM object 
management.  
Field 
No. 
Fields 
Mandatory 
or Optional 
Field 
Length 
Guidelines 
1 Category Mandatory 3 These two fields shall follow the CIC Master Type List. 
Please highlight items that are not following the CIC Master Type List, 
for CIC's confirmation. 
Field 1 shall be kept unique. 
Value of Field 2 could be the same for different meaning (e.g. 3PH 
means three phase isolator when it is under Field 1 “EIS”. 3PH means 
16A 3 phase 5 pin switched socket outlet when it is under Field 1 
“ESO”). 
Fields 2 can have the same value as Field 1 if Field 2 has different 
meaning and is necessary to describe the BIM object at the second 
level. 
When Field 2 is not necessary to describe at the second level, three 
underscores (__) should be used. 
2 
Functional 
Type 
Mandatory 3 
3 Originator Mandatory 3 
For BIM objects originating from Works Departments, corresponding 
department names should be used as originator names.  However, 
other consultants or contractors who create the new BIM objects 
should follow Agent Responsible Code (ARC) list for originator. For 
those consultants or contractors, this field shall follow the up-to-date 
version of the ARC published by DEVB under the CAD Standard for 
Works Projects. ARC full list can be referred to this link: 
https://www.devb.gov.hk/en/construction_sector_matters/electronic_ser
vices/cad_standard/computer_aided_drafting/cad/index.html  
Users to update the originator field with their own abbreviation(s) when 
revising the downloaded BIM object from CIC BIM Portal. 
4 
Descriptor 
1 
Mandatory 1-15 
Descriptor 1 contains information about primary use and material when 
applicable. 
a. Duplicate information with the Category and Functional Type should 
be avoided. For example, if category is “WDW” (means window), 
“window” should not be used in this field. If functional type is “DBL” 
(means double), then “double” should not be used in this field. 
b. Capital letters should be used for first letter of each word (e.g. 
WallMounted, GlobalValve). 
c. All capital short forms should be used to indicate materials when 
applicable (e.g. CONC for concrete, WD for Wood). If Descriptor 1

CIC PRODUCTION OF BIM OBJECT GUIDE 
14 
Field 
No. 
Fields 
Mandatory 
or Optional 
Field 
Length 
Guidelines 
starts with all capital short form, an underscore (_) should be used to 
separate the short form and the following word  (e.g. CONC_Kerb, 
WD_Slash). 
d. If Descriptor 1 is blank, three nos. of underscores (___) should be 
used in place of Descriptor 1 (e.g. SFM-RCB-ACM-___-01.rfa). 
e. Descriptor 1 should be kept as concise as practicable with the 
maximum length of 15 characters in order to reserve space for 2 digit 
sequential number in Descriptor 2 for potential future expansion. 
5 
Descriptor 
2 
Mandatory 2 
Descriptor 2 is a 2-digit sequential number (e.g. 01 to 99) to distinguish 
different types that cannot be sufficiently identified by preceding fields. 
(e.g. STE-STA-ACM-NB_Pier-01.rfa) 
If Descriptor 2 is blank, two underscores (__) should be used in place 
of Descriptor 2. (e.g. PPF-UPV-ACM-BendSocket-__.rfa) 
2. Certain kinds of BIM object may be modelled for a specific purpose such as model submission to Works Departments, 
in which case DEVB BIM Harmonisation Guidelines for WDs should be referred.  
3. Unless otherwise required, all BIM developers shall apply the methodology of naming conventions specified in this 
Guide, including Format, Field Definition and Limitation, in their own BIM object library. 
4. The naming conventions shall include abbreviations of category, functional type, originator and descriptor fields.  
5. The category field shall indicate the BIM object category / classification / catalog based on the BIM platform system.  
6. The originator field shall indicate who owns or creates the BIM object. 
7. The descriptor fields shall indicate the critical characteristic of the BIM object. 
 
Format 
<Category> - <Functional Type> - <Originator> - <Descriptor 1> - <Descriptor 2>.<File Format Extension> 
Limitations on Number of Characters in the Name 
• Maximum 30 characters for the entire name, including hyphen marks (file names exceeding 30 characters may 
result in invalid file paths due to computer operating system limitations). 
• Keep file names as short as possible 
Example 
Field Example Description 
Category DOR-SGL-AEC-Wood-01.xxx A Door, DOR , is the abbreviation of the category / 
classification / catalog “door”. 
Functional Type DOR-SGL-AEC-Wood-01.xxx A Single Door, SGL,  is the abbreviation of the sub- type 
“single”. 
Originator DOR-SGL-AEC-Wood-01.xxx AEC is the abbreviation of Architecture, Engineering 
and Construction.  It represent s a common standard of 
the industry.  Alternatively t his can be replaced by the 
abbreviated name of the owner / creator  
Descriptor 1 DOR-SGL-AEC-Wood-01.xxx A door is made of Wood (Material).  An optional 
descriptive text. 
Descriptor 2 DOR-SGL-AEC-Wood-01.xxx A door is built with a Louvre.  This text further describes 
the BIM object. 
File Format Extension DOR-SGL-AEC-Wood-01.xxx File Format Extension
