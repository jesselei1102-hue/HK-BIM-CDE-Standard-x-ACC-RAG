---
source_file: output/HK Standard/DEVB BIM Harmonisation Guidelines for WDs (v3_0) with
  All Appendices.pdf
doc_id: devb_harmonisation_v3
section_id: devb_harmonisation_v3_bim_object_files
title: BIM OBJECT FILES
page_start: 15
page_end: 25
authority: DEVB BIM Harmonisation v3.0 §BIM
authority_type: standard
normative_weight: mandatory
discipline: general
lifecycle_stage: project
publication_year: 2023
software: null
priority: high
language: en
source_url: hk_cde://devb_harmonisation_v3/devb_harmonisation_v3_bim_object_files
---

# BIM OBJECT FILES

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS BIM OBJECT FILES 
 
6 
3. BIM Object Files 
3.1. Principles 
3.1.1. The principles of authoring BIM objects s hould follow the latest version of the CIC 
Production of BIM Object Guide, which contains LOD-G (graphical) and LOD-I (non-
graphical) requirements. In addition, A ppendix V and Appendix VI provide further 
examples for handling BIM objects’ LOD-G and LOD-I.  
3.1.2. CIC BIM Portal has provided an industry-wide, centralised and publicly accessible 
platform for sharing of BI M object files. BIM objects authored by the WDs or from 
capital works projects should be incor porated into the CIC BIM Portal upon 
certification by CIC. WDs should follow Section 3.7 to provide BIM object files to CIC. 
WDs should notify project awardees to util ise BIM object files shared at CIC BIM 
Portal as far as practicable and make reference to WDs’ BIM object files that have been 
internally certified for use. 
3.1.3. BIM object files’ naming convention should follow Section 3.4, which is in line with 
the CIC Production of BIM Object Guide. 
3.1.4. To minimise information loss during conversion, the appropriate category type for the 
BIM objects should be define d. The use of generic mode l for BIM obj ect authoring 
should be minimised as far as practicable. 
3.1.5. To optimise information management within BIM models, replicable BIM objects (e.g. 
windows, doors, signage, fittings) should be used to comp ose BIM models as far as 
practicable. 
 
3.2. CIC Production of BIM Object Guide and Portal 
3.2.1. Since 2019, CIC has set up a BIM portal for pub lic to access the BI M object files. A 
BIM objects library has been established on the CIC BIM Portal, and it contains BIM 
object files under OmniClass cl assifications. Refer to Figure 3-1 for CIC BIM Portal 
(located at https://www.bim.cic.hk/en/resources/bim_objects). 
 
 
P15

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS BIM OBJECT FILES 
7 
Figure 3-1 CIC BIM Portal 
3.2.2. Each BIM object file is accompanied by a BIM object sheet which contained 3D 
geometry and 2D presentation. To fulfil drawing generation needs, 2D presentation may 
be in the form of layout, elevation view, s ectional view, 2D symbols, and tag / label / 
annotations. The BIM object sheet serves to  indicate that the BIM object has been 
completed and satisfied all requirements and functions for drawing production (refer to 
Figure 3-2). 
Figure 3-2 An example of BIM Object Sheet 
P16

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS BIM OBJECT FILES 
 
8 
3.3. Process of Adopting CIC BIM Objects 
3.3.1. In order to utilise the CIC BIM objects as  far as practicable, a process has been 
developed to adopt CIC BIM objects. Refer to Figure 3-3 below for an example of BIM 
object found on CIC BIM Portal. 
 
Figure 3-3 An Example of BIM object found on CIC BIM Portal  
 
 
3.3.2. There are three scenarios for adopting CIC BIM objects, which depend on whether the 
four criteria, including appearance, 2D pres entation, attributes (LOD-I) and naming 
convention, are fulfilled: 
Adoption Scenario 1: If no similar CIC BI M object is found, a new object file 
shall be created and named according to the Guidelines. 
Adoption Scenario 2: If a CIC BIM object is  similar to what is needed but does 
not fulfil all the four criteria, it shall be revised and the file 
shall be renamed according to the Guidelines. 
P17

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS BIM OBJECT FILES 
 
9 
Adoption Scenario 3: If a CIC BIM object is exactly what is need ed and fulfils all 
the four criteria, it shall be adopted without renaming. 
Refer to Figure 3-4 below for BIM object adoption scenarios. 
 
Figure 3-4 BIM Object Adoption Scenarios 
 
Remarks: 
# - Refer to Appendix VI 
* - Refer to Section 3.4 
 
3.4. Naming of BIM Object File 
3.4.1. BIM objects shall be modelled for a speci fic purpose and assigned with the most 
appropriate and representative category.  BIM object files shall be named systematically 
and logically for the understanding of users and for easy BIM object management.  
In accordance with the CIC Production of BIM Object Guide (Version 2 -2021), 
BIM object naming should be in the format as shown below.  
 
<Category>-<Functional Type>-<Originator>-<Descriptor 1>-<Descriptor 
2> .<File Format Extension> 
 
  
file 
  file 
P18

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS BIM OBJECT FILES 
10 
3.4.2. Based on the CIC Production of BIM Object Guide, the following principles are set: 
Table 3-1 Descriptions and Guidelines for the BIM Object Naming Fields 
Field 
No. 
BIM Object 
Naming 
Fields  
Obligation 
Field 
Length 
and 
Format 
Guidelines 
1 Category Required 3 
alpha-
numeric 
These two fields shall follow CIC 
Master Type List. 
(https://www.bim.cic.hk/en/resour
ces/master_list). 
a) Field 1 shall be kept unique in
value and meaning  (e.g. ECD,
SCH)
b) Value of Field 2 could be the
same for different meaning
(e.g. 3PH means three phase
isolator when it is under Field
1 “EIS”. 3PH means 16A 3
phase 5 pin switched socket
outlet when it is under Field 1
“ESO”).
c) Fields 2 can have the same
value as Field 1 if Field 2 has
different meaning and is
necessary to describe the BIM
object at the second level.
d) When Field 2 is not necessary
to describe at the second level,
three underscores (__) should
be used.
2 Functional 
Type 
Required 3 
alpha-
numeric 
3 Originator Required 3 
alpha-
numeric 
For BIM objects originating from 
WDs, corresponding department 
names should be used as originator 
names.  However, other consultant 
or contractors who create the new 
BIM objects should follow Agent 
Responsible Code ( ARC) list for 
originator. For those consultant or 
contractors, this field shall follow 
the up-to-date version of the ARC 
published by DEVB under the 
CAD Standard for Works Projects 
(ARC full list can be found at: 
P19

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS BIM OBJECT FILES 
 
11 
Field 
No. 
BIM Object 
Naming 
Fields  
Obligation 
Field 
Length 
and 
Format 
Guidelines 
https://www.devb.gov.hk/en/const
ruction_sector_matters/electronic
_services/cad_standard/computer
_aided_drafting/cad/index.html) 
 
If a BIM object is fully adopted 
without change, its name should be 
maintained. However, if the BIM 
object is modifie d, its originator 
code should be updated and saved 
as another BIM object file. 
 
4 Descriptor 
1 
Required 1-15 
alpha-
numeric 
Descriptor 1 contains information 
about primary use and material 
when applicable.  
a) Duplicate information with 
the Category and Functional 
Type should be avoided. For 
example, if category is 
“WDW” (means window), 
“window” should not be used 
in this field. If functional type 
is “DBL” (means double), 
then “double” should not be 
used in this field. 
b) Capital letters should be used 
for first letter of each word 
(e.g. WallMounted, 
GlobalValve). 
c) All-capital short forms should 
be used to indicate materials 
when applicable (e.g. CONC 
for concrete, WD for Wood). 
If Descriptor 1 starts with all-
capital short form, an 
underscore (_) should be used 
to separate the short form and 
the following word (e.g. 
CONC_Kerb, WD_Slash). 
d) If Descriptor 1 is blank, three 
nos. of underscores (___) 
shoul
d be used in place of 
P20

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS BIM OBJECT FILES 
 
12 
Field 
No. 
BIM Object 
Naming 
Fields  
Obligation 
Field 
Length 
and 
Format 
Guidelines 
Descriptor 1 (e.g. SFM-RCB-
ACM-___-01.rfa). 
e) Descriptor 1 should be kept as 
concise as practicable with the 
maximum length of 15 
characters in order to reserve 
space for 2 digit sequential 
number in Descriptor 2 for 
potential future expansion. 
 
 5 Descriptor 
2 
Required 2  
alpha-
numeric 
Descriptor 2 is a 2-digit sequential 
number (e.g. 01 to 99) to 
distinguish different types that 
cannot be sufficiently identified 
by preceding fields. (e.g. STE-
STA-ACM-NB_Pier-01.rfa) 
 
If Descriptor 2 is blank, two 
underscores (__) should be used 
in place of Descriptor 2. (e.g. 
PPF-UPV-ACM-BendSocket-
__.rfa) 
 
 
3.4.3. The file name length of BIM objects s hould be 30 characters maximum, including 
delimiters but excluding the file extension. BIM object file name is expected to be as 
short as possible and should comply with the CIC Production of BIM Object Guide. 
3.4.4. Only alphanumeric characters, hyphen (-) and underscore (_) are allowed. Hyphens 
should be used as the delimiter between each naming field. 
3.4.5. Space, special symbols and invalid characters  (including ~ " # %  * : < > ? / \ { | }.) 
shall not be used within BIM object file names. 
3.5. Guidelines for BIM Object Authoring 
While the principles of authoring BIM object should follow the CIC Production of 
BIM Object Guide, this section provides further guidelines for handling BIM 
objects.  
 
3.5.1. Simplifying and Enhancing BIM Objects 
P21

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS BIM OBJECT FILES 
13 
Before using a BIM object, BIM authors should check if it could be simplified or 
modified to meet the project requirements. The basic principle when using the BIM 
objects should be as follows: 
a) At the same LOD-G, utilising the same BIM object without change as far as
practicable.
b) When the LOD-G is too detailed for the project, simplifying the BIM object
should be considered while ensuring th at the same LOD-I is maintained. The
naming of the simplified object should follow Section 3.4 for details and Field 3
of the BIM object file naming shall be renamed after the Originator who altered
the BIM object.  Refer to Figure 3-5 below for a sample simplified BIM object.
Figure 3-5 Sample Simplified BIM Object based on Detailed BIM Object 
c) When the LOD-G is insufficient to meet the project requi rement, a new BIM
object should be developed based on original BIM object file.
P22

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS BIM OBJECT FILES 
 
14 
3.5.2. BIM Object Division 
The CIC Master Type List shows the current  set of classification and codifications. 
A model element may be authored using more than one BIM object. For example, a 
lamp post may contain three BIM objects: type of pole, sub type of lamps and 
foundation (refer to Figure 3-6). 
 
 
Figure 3-6 Sample Lamp Post BIM Object Division 
 
 
3.5.3. LOD-G and LOD-I for different model elements may vary but should ultimately 
facilitate project needs. The attributes “L OD-G” and “LOD-I” should be added to the 
newly created BIM objects to indicate the LOD level number. Refer to Appendix VI 
for details. 
3.5.4. Common BIM software have built- in templates or tools to facilitate the authoring of 
BIM objects. These templates or tools have the capability to embed 2D presentation, 
but the methods may vary. After inserti ng BIM objects into BIM models, project-
specific attributes should be added and populated. Refer to Appendix V for examples 
of BIM object authoring. 
 
3.6. BIM Object Management 
3.6.1. CIC BIM Portal supports Omni Class classification. To f acilitate logical BIM object 
organisation and searching, BIM objects could be organised in a folder structure as the 
first level of OmniClass according to “OmniClass version 2012 Table 23” 
(https://www.csiresources.org/standards/omniclass/standards-omniclass-about). Table 
3-2 below shows an example for the corr esponding Level 1 title with OmniClass 
numbers as folder names. 
 
P23

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS BIM OBJECT FILES 
15 
Table 3-2 Folder Structure of BIM Object Library  
OmniClass 
Table 23 Products 
Folder 
Name Level 1 Title 
23-11 Site Products 
23-13 Structural and Exte rior Enclosure Products 
23-15 Interior and Finish Products 
23-17 Openings, Passages, and Protection Products 
23-19 Specialty Products 
23-21 Furnishings, Fixtures  and Equipment Products 
23-23 Conveying Systems and Ma terial Handling Products 
23-25 Medical and La boratory Equipment 
23-27 General Facility Services Products 
23-29 Facility and Occupa nt Protection Products 
23-31 Plumbing Specific Pr oducts and Equipment 
23-33 HVAC Specific Products and Equipment 
23-35 Electrical and Lighting Speci fic Products and Equipment 
23-37 Information and Communication Specific Products and 
Equipment 
23-39 Utility and Transportation Products 
3.6.2. In addition to managing the folder struct ure, OmniClass classification information 
should also be inputted in BIM objects’ clas sification attributes, in accordance with 
OmniClass version 2012 Table 23.  Refer to Appendix VI for details. 
3.6.3. WDs are recommended to a dopt and customise Appendix VII – Sample BIM Object 
Check Form for departmental use. The corresponding BIM Support Team should 
upkeep their own check forms in the future. 
3.7. Workflow for Sharing BIM Object 
3.7.1. WD’s BIM Support Team should collect, revi ew and register BIM object packages 
(BIM object files, CIC BIM Object Sheets and CIC BIM Object  Check Forms) for 
submission to CIC. 
3.7.2. If CIC deems the BIM object file not ready to be accepted, comments would be provided 
to the BIM Support Team concerned for following up. After CIC certifies and accepts 
the BIM objects, the BIM object files woul d be made available on CIC BIM Portal. 
Feedback regarding the acceptance status would be provided to  the respective BIM 
Support Team within three months after receiving the BIM object packages. 
P24

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS BIM OBJECT FILES 
 
16 
3.7.3. WDs should notify project awardees to utilise BIM objects shared at CIC BIM Portal 
as far as practicable and make reference to WDs’ BIM objects that have been internally 
accepted for use. 
 
 
P25
