---
source_file: output/HK Standard/CIC BIM Standard/CIC BIM Standards General 2024/CIC
  BIM Standards General (Version 2024).pdf
doc_id: cicbims_2024
section_id: cicbims_2024_2_6_3_level_of_information_lod_i
title: 2.6.3 Level of Information (LOD-I)
page_start: 45
page_end: 46
authority: CICBIMS 2024 §2.6.3
authority_type: standard
normative_weight: mandatory
discipline: general
lifecycle_stage: project
publication_year: 2024
software: null
priority: high
language: en
source_url: hk_cde://cicbims_2024/cicbims_2024_2_6_3_level_of_information_lod_i
---

# 2.6.3 Level of Information (LOD-I)

2 Information Requirements 
 
 
45 
 
2.6.3 Level of Information (LOD-I) 
Level of Information ( LOD-I) is the description of non- graphical information in a model 
element and will evolve as the project progresses. LOD -I requirements should be defined 
and agreed beforehand as identified within the AIR . Provision of a data dictionary against 
which product data templates  can be prepared facilitates  the delivery of verifiable data. As 
the required LOD -I varies for each project, this Standards does not aim  to provide an 
exhaustive list of information for each model element, but instead indicates a suitable 
approach for adoption.  
 
To specify LOIN, and how information is to be delivered, the specifiers should identify the 
following prerequisites:  
 
• Purposes of the information to be delivered; 
• Information delivery milestones; 
• Parties who will request and deliver information; and 
• Objects in one or more breakdown structures. 
 
The LOD-I required for the model elements should be determined based on their intended 
usage and should NOT be over specified. This Standard s indicates a suitable approach by 
giving examples of minimum LOD -I associated with typical elements /objects  at five levels  
from LOD-I 100 to LOD-I 500 as shown in Table below. (where M means “Mandatory” and R 
means “Required”. ) 
No. Type Attribute Name  Description LOD-Information Proposed 
Input Format  100 200 300 400 500 
1 Project 
Information 
(Appointing 
Parties 
specific)  
Organisation 
Name 
Client name (per 
agreement/ 
contract)  
M M M M M Alphanumeric  
Project Issue 
Date 
Project 
Commencement 
date 
M M M M M MMM YYYY  
(eg. Nov 2021 ) 
Project Address  The street address 
of the project  
M M M M M Alphanumeric  
Project Name  The project name 
as shown on the 
drawing sheet’s title 
block  
M M M M M Alphanumeric  
Project Number  The project number 
as shown on the 
drawing sheet’s title 
block  
M M M M M Alphanumeric  
2 General 
Properties  
CAT Code  Departmental 
category  
(see Remark 1)  
R R R R R Alphanumeric  
Locations  Location (e.g. 
district code for 
outdoor object)  
 R R R R Alphanumeric  
Departmental 
Unique ID  
The unique  ID for 
departmental 
information  
management  
 R R R R Alphanumeric  
3 Design  
Properties  
Material  Singular material  or 
all materials  
pertaining  to the 
assembly  
 R R R R Alphanumeric  
Material  Grade  Material grade  (e.g.   R R R R Alphanumeric

2 Information Requirements 
 
 
46 
 
No. Type Attribute Name  Description LOD-Information Proposed 
Input Format  100 200 300 400 500 
concrete  grade, 
steel  grade)  
Design Capacity  Design  capacity   R R R R Alphanumeric  
Number  Room  Number  
(see Remark 2)  
 R* R* R R Alphanumeric  
Name Room  Name 
(see Remark 2)  
  R* R R Alphanumeric  
4 Classification  
Properties 
(see  
Remark  3) 
OmniClassCode  OmniClass  code   R R R Alphanumeric  
OmniClassTitle  OmniClass  title    R R R Alphanumeric  
OmniClass  
Version  
OmniClass  version    R R R Alphanumeric  
5 Manufacturer’
s Equipment  
Properties  
Brand  Name Brand  name    R R Alphanumeric  
Manufacturer 
Name 
Manufacturer name    R R Alphanumeric  
Model Number of  
element  / 
equipment  
Model number     R R Alphanumeric  
Equipment  
Capacity  
Equipment  capacity     R R Alphanumeric  
Asset  ID Asset  ID    R R Alphanumeric  
Contract Number  
of the Equipment  
The equipment’s  
contract number  
   R R Alphanumeric  
6 Condition  
Properties  
Certified  
Completion  Date 
Certified  completion  
date 
   R R MMM YYYY 
(eg.  Nov 2021)  
Handover  Date Handover  date    R R MMM YYYY 
(eg.  Nov 2022)  
7 Verification 
Property  
Verification  Verification  method  
(input  A for "field 
verified by visual  
inspection"  and B 
for "field  verified by 
a measured  
survey")  
    R Text (e.g.  A or 
B) 
 
Remarks:  
1. Category (in the form of the shared parameter “CAT Code” under “General Properties”) 
could facilitate grouping and data filtering. In addition, “category” may refer to:  
a) The use of appropriate category or object types when creating BIM objects to 
minimize data loss (especially LOD- G) during open format exchange.  
b) BIM Object naming's abbreviation code fields 1 & 2 to facilitate BIM object library 
management and consistency of information container ID naming.  
2. R* - Room Name and Room Number are required when statutory and contractual 
drawings are produced.  
3. Individual Appointing Party’s classification(s) in addition to or instead of OmniClass 
could be defined by respective Appointing Parties.  
4. It is recommended that a full list of element -specific LOD- I should be clearly defined 
before a project commences.  
5. Design Properties should be defined in line with any agreement or Appointing Party / 
Client Information Requirements provided for individual projects.
