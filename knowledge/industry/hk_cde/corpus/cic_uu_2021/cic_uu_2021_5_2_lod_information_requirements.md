---
source_file: output/HK Standard/CIC BIM Standard/CIC BIM Standards for Underground
  Utilities (Version 2 - 2021).pdf
doc_id: cic_uu_2021
section_id: cic_uu_2021_5_2_lod_information_requirements
title: 5.2  LOD-Information Requirements
page_start: 25
page_end: 29
authority: CIC BIM Standards UU 2021 §5.2
authority_type: standard
normative_weight: mandatory
discipline: underground_utilities
lifecycle_stage: project
publication_year: 2021
software: null
priority: high
language: en
source_url: hk_cde://cic_uu_2021/cic_uu_2021_5_2_lod_information_requirements
---

# 5.2  LOD-Information Requirements

21 
 
5 LOD Elements Specification 
5.2  LOD-Information Requirements 
This section describes the LOD-I required for an Information model, i t is w ell noted that 
project Appointing Parties / Clients may have their own requirement for LOD-I. This section 
sets out a software- neutral approach for determining LOD -I, using samples instead of 
attempting to giving an exhaustive list of requirements. The BIM standards developed by  
HKSAR Works Departments should be referred to for further details. These and other 
relevant publications are given in the CIC BIM Portal: 
https://www.bim.cic.hk/en/resources/publications for relevant publications. 
 
The following table lists the attributes commonly attached to individual model elements / 
objects. 
(where M means “Mandatory” and R means “Required”.)  
 
No. Type Attribute Name Description 
LOD-Information Proposed 
Input Format 100 200 300 400 500 
1 Project 
Information 
(Appointing 
Parties specific) 
Organisation Name Client name (per 
agreement/ contract) 
M M M M M Alphanumeric 
Project Issue Date Project Commencement 
date 
M M M M M MMM YYYY 
(e.g. Nov 
2021) 
Project Address The street address of 
the project 
M M M M M Alphanumeric 
Project Name The project name as 
shown on the drawing 
sheet’s title block 
M M M M M Alphanumeric 
Project Number The project number as 
shown on the drawing 
sheet’s title block 
M M M M M Alphanumeric 
2 General 
Properties 
CAT Code Departmental category 
(see Remark 1) 
R R R R R Alphanumeric 
Locations Location (e.g. district 
code for outdoor object) 
 R R R R Alphanumeric 
Departmental 
Unique ID 
The unique ID for 
departmental 
information 
management 
 R R R R Alphanumeric 
Reference Level Reference level used for 
2D drawing annotation 
R R R R R Alphanumeric 
Z level 
Refer to Appendix E for 
details 
 R R R R Number 
Size  R R R R Number

22 
 
5 LOD Elements Specification 
No. Type Attribute Name Description 
LOD-Information Proposed 
Input Format 100 200 300 400 500 
Minimum Cover 
provided 
 R R R R Number 
No. of ducts  R R R R Alphanumeric 
Type of Protection 
Protection of the 
elements 
 R R R R Alphanumeric 
Status 
Status of the UU 
elements: Existing or 
New Build 
 R R R R Alphanumeric 
Year of construction 
Year of construction of 
the UU elements 
   R R Alphanumeric 
Owner 
Owner of the UU 
elements 
   R R Alphanumeric 
3 Design 
Properties 
Material Singular material or all 
materials pertaining to 
the assembly 
 R R R R Alphanumeric 
Material Grade Material grade (e.g. 
concrete grade, steel 
grade) 
 R R R R Alphanumeric 
Design Capacity Design capacity  R R R R Alphanumeric 
Number Room Number 
(see Remark 2) 
 R* R* R R Alphanumeric 
Name Room Name 
(see Remark 2) 
  R* R R Alphanumeric 
4 Classification  
Properties 
(see Remark 
3) 
OmniClassCode OmniClass code   R R R Alphanumeri
c 
OmniClassTitle OmniClass title   R R R Alphanumeric 
OmniClassVersion OmniClass version   R R R Alphanumeric 
5 Manufacturer’s 
Equipment 
Properties 
Brand Name Brand name    R R Alphanumeric 
Manufacturer Name Manufacturer name    R R Alphanumeric 
Model Number of 
element / equipment 
Model number    R R Alphanumeric 
Equipment Capacity Equipment capacity    R R Alphanumeric 
Asset ID Asset ID    R R Alphanumeric 
Contract Number of 
the Equipment 
The equipment’s 
contract number 
   R R Alphanumeric 
6 Condition 
Properties 
Certified Completion 
Date 
Certified completion 
date 
  
 
 R R MMM YYYY 
(e.g. Nov 
2021)

23 
 
5 LOD Elements Specification 
Handover Date Handover date    R R MMM YYYY 
(e.g. Nov 
2022) 
7 Verification 
Properties 
Verification Verification method 
(input A for "field verified 
by visual inspection" 
and B for "field verified 
by a measured survey") 
    R Text (e.g. A or 
B) 
QL Standard 
Qualification level of the 
UU elements/objects 
(see Remark 7) 
    R Alphanumeric 
QL Grade 
Grade of the quality 
level 
(see Remark 7) 
    R Alphanumeric 
 
Remarks: 
1. Category (in the form of the shared parameter “CAT Code” under “General Properties”) 
could facilitate grouping and data filtering. In addition, “category” may refer to: 
a) The use of appropriate category or object types when creating BIM objects to 
minimize data loss (especially LOD-G) during open format exchange. 
b) BIM Object naming's abbreviation code fields 1 & 2 to facilitate BIM object library 
management and consistency of information container ID naming. 
2. R* - Room Name and Room Number are required when statutory and contractual 
drawings are produced. 
3. Individual Appointing Party’s classification (s) in addition to or instead of OmniClass 
could be defined by respective Appointing Parties. 
4. It is recommended that a full list of element -specific LOD-I should be clearly defined 
before a project commences. 
5. Design Properties should be defined in line with any agreement or Appointing Party / 
Client Information Requirements provided for individual projects. 
6. For details of the attributes “Z level”, “Size”, “Thickness” and “No. of ducts” refer to 
Appendix E. 
7. For details of the attributes “Z level”, “Size”,  “Thickness” and “No. of ducts” refer to 
Appendix E. 
Among the above attributes, “Reference Level” , “Status”, “QL Standard” and  “QL 
Grade” are relatively new to the current UU industry, and further guidance is given for 
these attributes.

24 
 
5 LOD Elements Specification 
• Reference Level: C are must be taken in annotating the correct levels when 
generating 2D drawings from BIM models . This attribute/information states which 
reference level shall be used for annotation when generating 2D drawings. 
Reference levels for UU are usually presented in the following ways: 
1. Top level   
2. Crown level  
3. Centre level  
4. Invert level (by manhole survey of gravity flow pipeline)  
5. Bottom level  
6. Cover Depth 
For detailed description of the different reference levels refers to Appendix F. 
 
• Status: In some situations, existing UU elements may need to be modelled for 
coordination with their elements, this attribute/information indicates whether the UU 
elements is an existing elements or a new-build elements. 
 
• QL Standard: This attribute/information informs the users of the BIM model what 
standard/specification of accuracy is used for the UU elements. The project team 
should have an agreed QL specification or standard at the outset. If no any specific 
requirements are stated , PAS 128 can be a referenc e, with details as given in 
Appendix B. This attribute/information is optional and is subject to the individual 
project needs. 
 
• QL Grade: This attribute/information describes the grade or level of the QL standard 
for the UU elements, e.g. if PAS 128 is being used, the grade of PAS 128 shall be 
used to describe the accuracy of the elements, (e.g. QL-A, QL -C). This 
attribute/information is optional and is subject to the individual project needs. 
 
Apart from the above attribute/information, it is recommended to have the following 
documents/project information or folder path structure in place to link up with the BIM 
Models, if available: 
• Conduit condition evaluation report 
• Manhole and pipes internal condition survey (CCTV and report) 
• Comprehensive utility survey 
• Water leakage detection report. 
• Survey of buried water carrying services 
• Routine inspection reports 
• Repair and maintenance record

25 
 
5 LOD Elements Specification 
Any product-specific technical information/attributes should be  agreed with the project 
Appointing Party / Client of the project. 
 
Further details of the information / attributes described in the section are given in the BIM 
standards developed by  the Works Departments. These and other relevant publications 
are included in the CIC BIM Portal https://www.bim.cic.hk/en/resources/publications for the 
relevant publications.
