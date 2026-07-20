---
source_file: output/HK Standard/DEVB BIM Harmonisation Guidelines for WDs (v3_0) with
  All Appendices.pdf
doc_id: devb_harmonisation_v3
section_id: devb_harmonisation_v3_federation_and_bim_model_naming
title: FEDERATION AND BIM MODEL NAMING
page_start: 26
page_end: 32
authority: DEVB BIM Harmonisation v3.0 §FEDERATION
authority_type: standard
normative_weight: mandatory
discipline: general
lifecycle_stage: project
publication_year: 2023
software: null
priority: high
language: en
source_url: hk_cde://devb_harmonisation_v3/devb_harmonisation_v3_federation_and_bim_model_naming
---

# FEDERATION AND BIM MODEL NAMING

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS FEDERATION AND BIM MODEL NAMING  
 
17 
4. Federation and BIM Model Naming 
4.1. BIM Model Naming Principle 
4.1.1. This section provides the principle to set out the BIM model naming (information 
container ID) and federation strategy to achieve consistent BIM model federation. A 
hierarchical and logical mode l organisation can serve to facilitate BIM management 
and subsequent LOIN implementation su ch as LOD-I management and colour 
appearance. 
4.1.2. ISO 19650‑2:2018 Part 2 Section 5.1.7(a) states th at each information container shall 
have a unique ID, based upon agreed and documented convention comprising fields 
separated by a delimiter, w ithin a project Common Data Environment (CDE). Unique 
ID should be consistent among WDs to facilita te interdepartment al information 
exchange via the GBDR. The hierarchy should include the following descriptions: 
a) What asset is the BIM model related to; 
b) Who is the originator of information; 
c) Which geospatial zone and system(s) it belongs to; 
d) Where it is located; 
e) Which discipline it is related to; 
f) What type of information the model contains; and 
g) What unique information is necessary to further distinguish the model from 
others. 
4.1.3. ISO 19650 ‑2:2018 Part 2 Section 5.1.7(b) states that the project's common data 
environment shall enable each field to be assigned a value from an agreed and 
documented codification standard. The codifi cation standard for model file naming 
would set out: 
a) Field sequence; 
b) Information container ID fields (and sub-fields if applicable); 
c) Description of each information container ID field and sub-field; 
d) Whether the field is required or optional; 
e) Format which defines length and alphabetic, numeric or alphanumeric; 
f) Whether the codification is common or project-specific; and 
g) Where the detailed list of codification information can be located. 
4.1.4. Information container ID, model divisi on, federation and corresponding abbreviation 
codes should be sustainable and consider the future potential use of metadata. 
 
P26

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS FEDERATION AND BIM MODEL NAMING  
 
18 
4.2. Information Container Identification Fields 
4.2.1. Model naming shall follow the informati on container ID fields sequence and 
corresponding abbreviation codes. The arrangement of information container ID fields 
is primarily derived from the principles  in ISO 19650 to suit the common practices 
within WDs. Naming convention should follow Section 4 of the Guidelines.   
4.2.1.1. The maximum total length of model names is 43 characters (including delimiters and 
information dividers; excluding file extension). Appendix VIII – Federation Strategy 
Diagrams and Naming Examples shows examples for reference. 
4.2.1.2. Information container ID fields are reserved for information pertinent to information 
exchange between WDs. To ensure that  the total length of model naming is 
manageable, metadata should only be used when: 
a) The information container ID field is only relevant to individual WDs; 
b) The identification does not facilitate work breakdown structure; 
c) The length of the information container ID field is relatively long; or 
d) The detailed descriptions would lose the meaning and adversely affect 
information exchange if abbreviated. 
The input format for metadata that facilitate data filtering (e.g. security code) should 
be consistent. Flexibility on the input format is allowed for other cases. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
P27

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS FEDERATION AND BIM MODEL NAMING  
19 
4.2.2. Table 4-1 describes the Information Container ID Fields. 
Table 4-1 Information Container ID Fields 
Field 
No. 
Information 
Container ID 
Field  
Sub-
field 
No. 
Information Container ID Field Description Obligation Field Length 
and Format 
Nature of 
Codification  
1 Project N/A A unique identifier should be used to serve as 
the project code (e.g. agreement, contract, future 
asset categorisation). 
A unique code should be assigned to each 
project stage (e.g. design, construction and 
operations) to determine the relationship with a 
particular asset.
 
Required 1-8
alphanumeric 
Project-specific 
(Appendix IX ,  
Table App IX-1) 
2 Originator N/A A unique identifier based on Agent Responsible 
Code (ARC) should be used to indicate the 
model’s responsible authoring party. 
The ARC is updated from time to time, which 
could be found at  
https://www.devb.gov.hk/en/construction_se
ctor_matters/electronic_services/cad_standa
rd/computer_aided_drafting/cad/index.html
 
Required 3 
alphanumeric 
Common 
(Agent Responsible 
Codes) 
3 Volume (and 
System when 
applicable) 
3.1
 A unique identifier should be used to indicate 
specific geospatial zone or volume within a 
project.
 
Required 1-3
alphanumeric 
Project-specific 
(Appendix IX ,  
Table App IX-2) 
P28

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS FEDERATION AND BIM MODEL NAMING  
 
20 
Field 
No. 
Information 
Container ID 
Field  
Sub-
field 
No. 
Information Container ID Field Description Obligation 
 
Field Length 
and Format 
Nature of 
Codification  
 3.2 An identifier should be used to indicate a 
collection of interconnected model elements 
across main disciplines under a system (e.g. 
sewerage system, water supply system, 
highway). System is used to facilitate data 
sharing instead of creating multiple 
interdisciplinary data sets.  
 
Optional 
 
1-3 
alphanumeric 
 
Common 
(Appendix X,  
Table App X‑1) 
4 Location (and 
Sub-location 
when 
applicable) 
 
4.1 An identifier should be used to indicate a 
specific location (e.g. slope number, feature 
code, building code) for geospatial coordination 
and future asset management. Common 
abbreviation codes should be used as far as 
practicable.
 
Required 
 
1-4 
alphanumeric 
 
Common  
(Appendix X,  
Table App X-2) 
and 
Project-specific  
(Appendix IX,  
Table App IX-3)  
4.2 An identifier should be used to indicate a sub-
location (e.g. level) within the same location. 
Additional sub-locations, if any, should be 
defined in the project information standard. 
This field’s value should not duplicate that of 
Field 4.1. 
 
Optional 
 
1-4 
alphanumeric 
 
Common 
(Appendix X, 
Table App X-3  
and X-4) 
5 Discipline 
(and Sub-
discipline 
when 
applicable)
 
5.1 An identifier should be defined for each primary 
discipline to facilitate appearance settings and 
information filtering for interdepartmental 
coordination. In the case that data filtering and 
collaboration is required, BIM models should be 
authored separately for each sub-discipline.
 
Required 
 
1-2 alphabetic 
 
Common 
(Appendix X, 
Table App X-5) 
5.2 An identifier should be used to indicate each 
sub-discipline appointment. 
Additional sub-disciplines, if any, should be 
defined in the project information standard. 
Optional 
 
 
1-2 alphabetic 
 
Common 
(Appendix X, 
Table App X-6) 
P29

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS FEDERATION AND BIM MODEL NAMING  
21 
Field 
No. 
Information 
Container ID 
Field  
Sub-
field 
No. 
Information Container ID Field Description Obligation Field Length 
and Format 
Nature of 
Codification  
Additional abbreviations should be based on 
those currently used by WDs as far as 
practicable. 
6 Type (and 
Characteristic 
when 
applicable)
 
6.1 An identifier should be used to indicate the 
information held within the container. 
As ISO 19650 states “this list can be expanded 
with project-specific codes,” Type is not limited 
to information unique to BIM models. 
Required 1-2
alphanumeric 
Common 
(Appendix X, 
Table App X-7)
 
6.2 An identifier should be used to indicate the 
model’s characteristic when relevant.
 
Optional 1 alphabetic Common 
(Appendix X, 
Table App X-8) 
7 Sequential 
Number
 
7 A sequential number should be assigned when it 
is necessary to further distinguish the model 
from the others. It can also be used to 
distinguish other documents such as drawings. 
Refer to Appendix VIII for details. 
Optional 3 numeric Project-specific 
P30

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS FEDERATION AND BIM MODEL NAMING 
 
22 
4.2.3. Required and Optional Information Container ID Fields  
The column “Obligation” in Table 4-1 indicates whether the field is required or 
optional.  Optional information container ID could be omitted at the discretion of the 
WDs. 
4.2.4. Abbreviation Codes 
4.2.4.1. The column “Nature of Codification” in Table 4-1 indicates wh ether the field is 
project-specific pertaining to individual projects, or common which could be 
applicable universally to all projects. 
4.2.4.2. Abbreviation codes serve to facilitate information container ID generation and BIM 
model upload validation for the GBDR. WDs should utilise these codes for model 
naming. Note that these codes are case sensitive. There are two types of abbreviation 
codes, including: 
a) Refer to Appendix X for details about the list of common codes for Information 
Container ID Fields. 
b) Project-specific codes should be documen ted in BEP. Refer to Appendix IX 
which contains examples of project-specific codes. 
4.2.4.3. The universal codes of ZZ and XX for information container ID fields shall be used 
when the conditions below exist.  Appendi x X for applying the universal codes in 
different information container ID fields for details. 
a) ZZ – multiple exist within a BIM model. 
b) XX – none or not applicable. 
4.2.5. Delimiter and Information Divider 
4.2.5.1. Hyphen (-, also known as minus) should be used as the delimit er to separate 
information container ID fields. 
4.2.5.2. Underscore ( _ ) should be used as an in formation divider between the sub-fields 
within each field when applicable. 
4.2.5.3. When optional field is not required, it should be left empty, and the preceding 
delimiter “-” (hyphen) or information divider “_” (underscore) should be eliminated. 
4.2.6. Space and Special Symbols 
Space, special symbols and invalid characters (including ~ " # % * : < > ? / \ { | }.) 
shall not be used within information container IDs. 
4.3. Federation Strategy 
4.3.1. In coherence with the sequence of information container ID fields, federation diagrams 
are established to describe the federation structure in a WBS as shown in Appendix VIII. 
4.3.2. In accordance with principles stated in Sections 4.1 and 4.2, federation strategy should 
ensure:  
P31

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS FEDERATION AND BIM MODEL NAMING 
23 
a) The information container breakdown (model division) conforms to
requirements from departmental information owners (if known);
b) The breakdown is sufficient to facilitate data filtering for information sharing
according to Appendix III for details;
c) File size limitation conforms to the maximum as stated in Section 2.3.1; and
d) The information is clearly grouped.
4.4. BIM Model Naming 
In accordance with Sections 4.1 – 4.3, model naming should be in the format as 
shown below.  
<project code> - <originator> - <volume_system> - <location_sub-location> - 
<discipline_subdiscipline> - <type_characteristic> - <sequential number> . <file 
extension> 
Refer to Appendix VIII for examples. 
4.5. Naming of Drawings Generated from BIM model 
WDs should consider adopting the model na ming format for draw ing file naming. 
Refer to Appendix VIII for an example. 
P32
