---
source_file: output/HK Standard/CIC BIM Standard/CIC BIM Standards for Mechanical,
  Electrical and Plumbing (Version 2 - 2021).pdf
doc_id: cic_mep_2021
section_id: cic_mep_2021_4_2_lod_i_requirements
title: 4.2  LOD-I Requirements
page_start: 39
page_end: 41
authority: CIC BIM Standards MEP 2021 §4.2
authority_type: standard
normative_weight: mandatory
discipline: mep
lifecycle_stage: project
publication_year: 2021
software: null
priority: high
language: en
source_url: hk_cde://cic_mep_2021/cic_mep_2021_4_2_lod_i_requirements
---

# 4.2  LOD-I Requirements

35 
 
 
 4  LOD Elements Specification 
4.2  LOD-I Requirements 
This section describes the LOD-I required for an Information model, it is w ell noted that 
project Appointing Parties / Clients may have their own requirement for LOD-I. This section 
sets out a software -neutral approach for determining LOD -I, using samples instead of 
attempting to giving an exhaustive list of requirements. The BIM standards developed by 
HKSAR Works Departments  should be referred to for further details.  These and other 
relevant publications are given in the CIC BIM Portal 
https://www.bim.cic.hk/en/resources/publications for relevant publications. 
 
The following table lists the attributes commonly attached to individual model elements / 
objects. (where M means “Mandatory” and R means “Required”.)  
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
(eg. Nov 
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
Number Room Number  R* R* R R Alphanumeric

36 
 
4  LOD Elements Specification 
No. Type Attribute Name Description 
LOD-Information Proposed 
Input Format 100 200 300 400 500 
(see Remark 2) 
Name Room Name 
(see Remark 2) 
  R* R R Alphanumeric 
4 Classification  
Properties 
(see Remark 
3) 
OmniClassCode OmniClass code   R R R Alphanumeric 
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
(eg. Nov 
2021) 
Handover Date Handover date    R R MMM YYYY 
(e.g. Nov 
2022) 
7 Verification 
Property 
Verification Verification method 
(input A for "field verified 
by visual inspection" 
and B for "field verified 
by a measured survey") 
    R Text (e.g. A or 
B) 
 
Remarks: 
1. Category (in the form of the shared parameter “CAT Code” under “General Properties”) 
could facilitate grouping and data filtering. In addition, “category” may refer to: 
a) The use of appropriate category or object types when creating BIM objects to 
minimize data loss (especially LOD-G) during open format exchange. 
b) BIM Object naming's abbreviation code fields 1 & 2 to facilitate BIM object library 
management and consistency of information container ID naming. 
2. R* - Room Name and Room Number are required when statutory and contractual 
drawings are produced. 
3. Individual Appointing Party’s classification(s) in addition to or instead of OmniClass 
could be defined by respective Appointing Parties.

37 
 
 
 4  LOD Elements Specification 
4. It is recommended that a full list of element-specific LOD-I should be clearly defined 
before a project commences. 
5. Design Properties should be defined in line with any agreement or Appointing Party 
/ Client Information Requirements provided for individual projects.
