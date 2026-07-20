---
source_file: output/HK Standard/DEVB BIM Harmonisation Guidelines for WDs (v3_0) with
  All Appendices.pdf
doc_id: devb_harmonisation_v3
section_id: devb_harmonisation_v3_appendix_vi_lod_i_requirements_creation_and_extraction_v3_
title: Appendix VI - LOD-I Requirements Creation and Extraction (v3.0)
page_start: 86
page_end: 112
authority: DEVB BIM Harmonisation v3.0 §Appendix
authority_type: standard
normative_weight: mandatory
discipline: general
lifecycle_stage: project
publication_year: 2023
software: null
priority: high
language: en
source_url: hk_cde://devb_harmonisation_v3/devb_harmonisation_v3_appendix_vi_lod_i_requirements_creation_and_extraction_v3_
---

# Appendix VI - LOD-I Requirements Creation and Extraction (v3.0)

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
 
 
 – LOD-I Requirements, Creation and Extraction 
 
P86

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
 
TABLE OF CONTENTS 
1. Introduction ....................................................................................................................................... VI-1 
2. LOD-I Across the WDs ..................................................................................................................... VI-1 
2.1. WDs’ Attributes Requirements ......................................................................................................... VI-1 
2.2. The Groups of Attributes in the LOD-I Requirements ...................................................................... VI-1 
2.3. Mandatory and Required Attributes .................................................................................................. VI-2 
2.4. BIM Authoring Software ................................................................................................................... VI-2 
2.5. Samples of Attributes Files ............................................................................................................... VI-2 
3. Creation of Attributes for Required Information ............................................................................... VI-7 
3.1. Creation of Project Information Attributes in Revit .......................................................................... VI-7 
3.2. Creation of Project Information Attributes in Civil 3D ..................................................................... VI-7 
3.3. Creation of Shared Parameters in Revit ............................................................................................ VI-8 
3.4. Creation of Property Set in Civil 3D ............................................................................................... VI-10 
3.5. Creation of Classification in Revit .................................................................................................. VI-15 
3.6. Creation of Material Attribute in Revit ........................................................................................... VI-18 
3.7. Filling in Default Attributes under Room in Revit .......................................................................... VI-21 
4. Types of BIM Model Attribute .................................................................................................. ..... VI-22 
4.1. Common Attributes ......................................................................................................................... VI-22 
4.2. Common Attributes with Alternative Attribute Names ................................................................... VI-22 
4.3. General Attributes ........................................................................................................................... VI-22 
4.4. Remaining Attributes ...................................................................................................................... VI-23 
5. Mapping and Extraction of Attributes from BIM Models ............................................................... VI-24 
5.1. Extraction Method Overview .......................................................................................................... VI-24 
5.2. Extraction of Attributes from Revit ................................................................................................. VI-24 
5.3. Extraction of Attributes from Civil 3D ........................................................................................... VI-24 
 
 
 
List of Tables 
Table App VI-1 LOD-I Across the WDs ........................................................................................................... VI-3 
 
  
P87

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
 
 
List of Figures 
Figure App VI-1 Shared Parameter File for Revit ............................................................................................. VI-2 
Figure App VI-2 Project Information Attributes in Revit .................................................................................. VI-7 
Figure App VI-3 Project Information Attributes in Civil 3D ............................................................................ VI-7 
Figure App VI-4 Adding Custom Property Name in Civil 3D .......................................................................... VI-8 
Figure App VI-5 An Example of User-define Attribute for Pipe Using Property Sets .................................... VI-10 
Figure App VI-6 Step a of Setting up Property Sets for Civil 3D BIM Object ............................................... VI-10 
Figure App VI-7 Step b of Setting up Property Sets for Civil 3D BIM Object ............................................... VI-11 
Figure App VI-8 Step c of Setting up Property Sets for Civil 3D BIM Object ............................................... VI-11 
Figure App VI-9 Step d of Setting up Property Sets for Civil 3D BIM Object ............................................... VI-12 
Figure App VI-10 Step e of Setting up Property Sets for Civil 3D BIM Object ............................................. VI-12 
Figure App VI-11 Step f of Setting up Property Sets for Civil 3D BIM Object .............................................. VI-13 
Figure App VI-12 Step a of Applying Property Sets to Civil 3D BIM Object ................................................ VI-13 
Figure App VI-13 Step b of Applying Property Sets to Civil 3D BIM Object ................................................ VI-14 
Figure App VI-14 Step c of Applying Property Sets to Civil 3D BIM Object ................................................ VI-14 
Figure App VI-15 An Example of Adding OmniClass Information as Shared Parameter in Revit ................. VI-15 
Figure App VI-16 An Example of Pre-set Parameters “OmniClass Number” and “OmniClass Title” under 
Identity Data in Revit Family .......................................................................................................................... VI-16 
Figure App VI-17 Adding Material Attributes to Family Parameters for Loadable Families ......................... VI-18 
Figure App VI-18 Adding Built-in Material Attributes to System Families ................................................... VI-19 
Figure App VI-19 Adding Built-in Material Attributes to Compound Structure System Families ................. VI-20 
Figure App VI-20 Filling in Default Attributes under Room in Revit ............................................................ VI-21 
Figure App VI-21 Sample Tabular Format for Storing Attributes .................................................................. VI-22 
 
 
P88

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-1 
 
1. Introduction 
This Appendix describes Level of Info rmation (LOD-I) for BIM models and BIM 
objects. Section 2 lists out and describes LOD-I across the WDs. Section 3 describes 
how to create attribute fields in different sample authoring software. Section 4 outlines 
different types of BIM attributes, and Section 5 describes principles of BIM attribute 
mapping and extraction.  Validation tools w ith relevant user guidelines to perform 
initial assessments on the BIM data quality are also available for access at the login 
page of the Government BIM Data Repository (website link: 
https://gbdr.landsd.ccgo.hksarg/). 
 
2. LOD-I Across the WDs 
Table App VI-1 describes al igned information requireme nts of BIM models with 
LOD-I 100 to 500. The groupings of attrib utes have been developed based on 
principles set out in CIC BIM Standards - General. Further descriptions of the attribute 
table are as follows:  
2.1. WDs’ Attributes Requirements 
Asset owner could define additional information needs. In accordance with paragraph 
17 of the Technical Circular (Works) No. 1/2025, WDs are required to agree with their 
maintenance agents of the built assets on a standard practice for handover of as-built 
BIM models and documentation which cont ain the essential asset information 
requirements (AIR) to facilitate effective asset management. Asset owners who have 
not defined their information needs should refer to the table below as the basis. Asset 
owners who have already defined their own required attribute(s) should ensure the 
pre-defined attributes could cover relevant LOD-I. 
2.2. The Groups of Attributes in the LOD-I Requirements 
The list of attributes is formulated based on common approaches as discussed with 
WDs. Table App VI-1 contains the following groups of attributes: 
a) Project Information is used to facilitate geolocation and data conversion via 
the Conversion Engine. 
b) General Properties are used to enable information grouping and identification. 
c) Design Properties are used to facilitate design review, drawing generation and 
quantity take-off. 
d) Classification Properties are used to facilitate asset classification. 
Departmental classification(s) in addition to or instead of OmniClass could be 
defined by WDs. 
e) Manufacturer’s Equipment Properties, Condition Properties and Verification 
Property are used to facilitate asset information management. 
 
P89

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-2 
 
 
2.3. Mandatory and Required Attributes  
“M” indicates mandatory information to facilitate metadata extraction and geolocation 
for Conversion Engine. “R” indicates required information to the WDs. To facilitate 
information exchange, Table App VI-1 shows the minimum re quired LOD-I and 
should be inputted into BIM models as fa r as practicable. Exem ptions to exclude 
required information to WDs should be sought from maintenance agencies, and the 
records on the decisions should be kept and documented in BEP. 
2.4. BIM Authoring Software  
Attributes that are built-in to BIM authori ng software should be utilised as far as 
practicable. In the last two columns of Ta ble App VI-1, Revit and Civil 3D are used 
as examples for the attributes’ creation methods. If software ot her than these two 
software is adopted, the methods for creating attributes should be properly 
documented in the BEP. 
2.5. Samples of Attributes Files 
To facilitate WDs’ adoption of the LOD-I across the WDs, a project-specific shared 
parameter text file for Autodesk Revit (r efer to Figure App VI-1) and a .dwg file 
including for Autodesk Civ il 3D with those attribut es can be downloaded from 
DEVB’s Website:  
https://www.devb.gov.hk/en/publications_and_press_releases/publications/devb-
harmonisation-guideline/index.html  
Figure App VI-1 Shared Parameter File for Revit 
P90

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-3 
 
Table App VI-1 LOD-I Across the WDs 
No. Grouping Attribute Name Description 
LOD-I Proposed 
Input Format 
Creation Method for 
Sample Authoring Software 
100 200 300 400 500 Revit Civil 3D 
1 Project 
Information 
Organisation Name Client name (per 
agreement/ contract)  
M M M M M Alphanumeric Use default 
attribute in 
Project 
Information 
Dialog Box 
 
Refer to 
Section 3.1 
Use Custom 
Property in 
Drawing 
Properties 
Dialog Box 
 
Refer to 
Section 3.2 
Project Issue Date Project 
Commencement date 
M M M M M MMM YYYY 
(eg. Nov 2014) 
Project Address The street address of 
the project 
M M M M M Alphanumeric 
Project Name The project name as 
shown on the 
drawing sheet’s title 
block 
M M M M M Alphanumeric 
Project Number The project number 
as shown on the 
drawing sheet’s title 
block 
M M M M M Alphanumeric 
2 General 
Properties 
CAT Code Departmental 
category  
(see Remark 1) 
R R R R R Alphanumeric Shared 
Parameter 
 
Refer to 
Section 3.3 
Property Set 
 
Refer to 
Section 3.4 Locations Location (e.g. 
district code for 
outdoor object)  
 R R R R Alphanumeric 
Departmental 
Unique ID 
The unique ID for 
departmental 
information 
management 
 R R R R Alphanumeric 
P91

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-4 
 
No. Grouping Attribute Name Description 
LOD-I Proposed 
Input Format 
Creation Method for 
Sample Authoring Software 
100 200 300 400 500 Revit Civil 3D 
3 Design 
Properties 
Material Singular material or 
all materials 
pertaining to the 
assembly 
 R R R R Alphanumeric Family 
parameter 
Refer to 
Section 3.6 
Property Set 
 
Refer to 
Section 3.4 
Material Grade Material grade (e.g. 
concrete grade, steel 
grade) 
 R R R R Alphanumeric Shared 
Parameter 
Refer to 
Section 3.3 
 
Design Capacity Design capacity  R R R R Alphanumeric   
  Number Room Number    R R Alphanumeric Use default 
attributes 
under 
“Room” 
Refer to 
Section 3.7 
N/A 
Name Room Name    R R Alphanumeric 
4 Classification 
Properties 
(see Remark 2) 
OmniClassCode OmniClass code   R R R Alphanumeric Classification 
Refer to 
Section 3.5 
Property Set  
Refer to 
Section 3.4 
OmniClassTitle OmniClass title   R R R Alphanumeric   
OmniClassVersion OmniClass version   R R R Alphanumeric   
P92

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-5 
 
No. Grouping Attribute Name Description 
LOD-I Proposed 
Input Format 
Creation Method for 
Sample Authoring Software 
100 200 300 400 500 Revit Civil 3D 
5 Manufacturer’s 
Equipment 
Properties 
Brand Name Brand name    R R Alphanumeric Shared 
Parameter 
Refer to 
Section 3.3 
Property Set 
Refer to 
Section 3.4 
Manufacturer 
Name 
Manufacturer name    R R Alphanumeric   
Model Number Model number of 
element / equipment 
   R R Alphanumeric   
Equipment 
Capacity 
Equipment capacity    R R Alphanumeric   
Asset ID Asset ID    R R Alphanumeric   
Contract Number 
of the Equipment 
The equipment’s 
contract number 
   R R Alphanumeric   
6 Condition 
Properties 
Certified 
Completion Date 
Certified completion 
date 
   R R MMM YYYY 
(eg. Nov 2014) 
Shared 
Parameter 
Refer to 
Section 3.3 
Property Set 
Refer to 
Section 3.4 
Handover Date Handover date    R R MMM YYYY 
(eg. Nov 2014) 
  
P93

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-6 
 
No. Grouping Attribute Name Description 
LOD-I Proposed 
Input Format 
Creation Method for 
Sample Authoring Software 
100 200 300 400 500 Revit Civil 3D 
7 Verification 
Property 
Verification Verification method 
(input A for "field 
verified by visual 
inspection" and 
B for "field verified 
by a measured 
survey") 
    R  T e x t   
(e.g. A or B) 
Shared 
Parameter 
 
Refer to 
Section 3.3 
Property Set 
 
Refer to 
Section 3.4 
 
Remarks: 
1. Category (in the form of the shared parameter “CAT Code” under “General Properties”) could facilitate grouping and data filtering. In 
addition, “category” may refer to: 
a) The use of appropriate category or object  types when creating BIM objects to minimize data loss (especially LOD-G) during open 
format exchange. 
b) BIM Object naming's abbreviation c ode fields 1 & 2 to facilitate  BIM object library management and consistency of information 
container ID naming. 
2. Department-specified classification(s) in addition to or instead of OmniClass could be defined by WDs. 
 
 
P94

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-7 
 
3. Creation of Attributes for Required Information 
3.1. Creation of Project Information Attributes in Revit 
In Revit, default attribut es can be utilised for inpu tting Project Information under 
Manage tab → Settings panel →  Project Information . The figure below 
illustrates the Revit Parameters used for Project Information. 
 
Figure App VI-2 Project Information Attributes in Revit 
 
3.2. Creation of Project Information Attributes in Civil 3D 
In Civil 3D, Project Information attributes can be created by using Custom Property 
in Drawing Properties dialog box.  
 
Figure App VI-3 Project Information Attributes in Civil 3D 
 
To create the Custom Property, first input “DWGPROPS” in the command line to 
show the Drawing Properties dialog box, then follow the steps as illustrated in the 
figure below to add the Project Information attributes. 
 
P95

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-8 
 
Figure App VI-4 Adding Custom Property Name in Civil 3D 
 
 
3.3. Creation of Shared Parameters in Revit 
3.3.1. In Revit, Shared Parameters are identifie d by unique GUIDs to facilitate attribute 
consistency across BIM files. Shared Parameters could be applied to BIM object and 
BIM model. 
3.3.2. Adding Shared Parameters to Revit Family Files (BIM objects in .rfa format) 
a) Create a new family or open an existing one. 
b) Click Create tab Properties panel  ( Family Types). 
c) In the Family Types dialog, under the Parameters group box, click Add. 
d) In the Parameter Properties dialog, select Shared Parameter. 
e) Click Select and choose the appropriate shared parameter from the appropriate 
parameter group. If desired, click Edit; this will return to the Edit Shared 
Parameters dialog which allows opening a different shared parameter file or 
adding new parameters (refer to the steps in Section 3.3.4). 
f) Choose whether to store the parameter by instance or type. 
g) Click OK. The parameter name appears in the Family Types dialog. 
h) Optionally, enter a value for the shared parameter or create a formula to 
calculate its value. 
3.3.3. Adding Shared Parameters to Revit Project Files (BIM models in .rvt format) 
a) Create a new project or open an existing one. 
b) Click Manage tab Settings panel   ( Project Parameters). 
P96

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-9 
 
c) In the Project Parameters dialog, click Add. 
d) In the Parameter Properties dialog, select Shared parameter. 
e) Click Select and choose the appropriate shared parameter from the appropriate 
parameter group. If desired, click Edit; this will return to the Edit Shared 
Parameters dialog which allows opening a different shared parameter file or 
adding new parameters (refer to the steps in Section 3.3.4). 
f) Choose whether to store the parameter by instance or type. 
g) Select the categories to add the shared parameter on the right-hand side. 
h) Click OK. The parameter will appear in the elements. 
i) Optionally, enter a value for the shared parameter or create a formula to 
calculate its value. 
3.3.4. Adding new Shared Parameters in Edit Shared Parameters Dialog 
a) Click Create. 
b) In the Create Shared Parameter File dialog, enter a file name, and save the 
dialog to a desired location. 
c) In the Groups box, click New and enter a name for the parameter group. 
d) From the Parameter Group drop-down menu, select a group. 
e) In the Parameters Group box, click New. 
f) In the Parameter Properties dialog, enter a name, discipline, and type for the 
parameter. 
g) Optionally, under Tooltip Description, click Edit Tooltip. In the Edit Tooltip 
dialog, enter the tooltip text, up to 250 characters. 
  
P97

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-10 
 
3.4. Creation of Property Set in Civil 3D 
3.4.1. In Civil 3D, Property Sets could be used for user-defined attributes for BIM model 
elements. Below is an example of user-define attribute for pipe using Property Sets. 
 
Figure App VI-5 An Example of User-define Attribute for Pipe Using Property Sets 
 
3.4.2. Property Sets could be defined in Style Manager. The following are key steps for 
setting up Property Sets for user-defined attributes for Civil 3D BIM object. 
a) Input command “STYLEMANAGER” in the command line to open the Style 
Manager which is shown as below Figure: 
 
Figure App VI-6 Step a of Setting up Property Sets for Civil 3D BIM Object 
 
  
P98

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-11 
 
b) Under Style Manager, right click Property Set Definitions under 
Documentation Objects, then click New. 
 
Figure App VI-7 Step b of Setting up Property Sets for Civil 3D BIM Object 
 
 
c) Input the Name and Description of the Property Set in General tab. 
 
Figure App VI-8 Step c of Setting up Property Sets for Civil 3D BIM Object 
 
  
P99

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-12 
 
d) Under Applies To tab, select the types of object (e.g. Pipe) to be applied in the 
Property Set.  
 
Figure App VI-9 Step d of Setting up Property Sets for Civil 3D BIM Object 
 
 
e) In Definition tab, click the properties as required to be added to the Property 
Set. 
 
Figure App VI-10 Step e of Setting up Property Sets for Civil 3D BIM 
Object 
 
  
P100

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-13 
 
f) Edit the Name, Description, Type, Source, Default value, etc. for the properties. 
 
Figure App VI-11 Step f of Setting up Property Sets for Civil 3D BIM Object 
 
3.4.3. The steps for applying Property Set to Civil 3D BIM objects are as follows: 
a) Select the model element, input PROPERTIES command in the command line, 
then click Extend Data in the PROPERTIES palettes. 
 
Figure App VI-12 Step a of Applying Property Sets to Civil 3D BIM Object 
 
  
P101

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-14 
 
b) Click Add Property Sets icon in the bottom left of the PROPERTIES palettes. 
In the Add Property Sets dialog, click to select the pre-defined Property Set 
“PipeData”, then click the OK button. 
 
Figure App VI-13 Step b of Applying Property Sets to Civil 3D BIM Object 
 
 
c) The “PipeData” of Property Set is now added to BIM object shown as below 
Figure. 
 
Figure App VI-14 Step c of Applying Property Sets to Civil 3D BIM Object 
 
 
  
P102

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-15 
 
3.5. Creation of Classification in Revit 
This section describes the methods of a dding classification information in Revit. 
Classification information could be department-specified classification(s), additional 
classification (e.g. OmniClass), or both. If de partment-specified classification(s) are 
used, classification information could be created as Shared Parameters (refer to 
Section 3.3 for details). If Om niClass classification is used, there are three creation 
methods as described in sections below.  
3.5.1. This section describes a sample creation method for classification information 
especially for OmniClass, as this method is not limited by OmniClass and Revit’s 
updates. Considering OmniClass version w ould be updated from time to time, to 
ensure consistency, if OmniCl ass is the project-specific  or stakeholder-specified 
classification system, OmniClass inform ation should be inputted as Shared 
Parameters. Refer to the figure below for an example and Section 3.3. for details. 
 
Figure App VI-15 An Example of Adding OmniClass Information as Shared 
Parameter in Revit 
 
 
  
P103

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-16 
 
3.5.2. Revit has an add-in program named “Sta ndardized Data Tool” for classification 
management. Refer to the below link for the details of the add-in program. 
https://interoperability.autodesk.com/standardizeddatatool.php 
3.5.3. Revit provides pre-set parameters “OmniClass Number” and “OmniClass Title” under 
Identity Data for Revit families. These pa rameters correspond to OmniClass “Table 
23 – Products” in Revit Family. Classification number could be defined by editing the 
Revit family’s properties. Refer to the figure below for an example. 
Figure App VI-16 An Example of Pre-set Parameters “OmniClass Number” 
and “OmniClass Title” under Identity Data in Revit Family 
 
 
  
P104

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-17 
 
If OmniClass 2012 standards is assigned to  be used and the OmniClass numbers 
supplied in Revit are incorrect, please refer to below link and update the OmniClass 
Taxonomy File accordingly. 
https://knowledge.autodesk.com/support/revit-
products/troubleshooting/caas/CloudHelp/cloudhelp/2020/ENU/Revit-
Troubleshooting/files/GUID-BA0B2713-ADA0-4E51-A7CD-85D85511F3ED-
htm.html 
  
P105

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-18 
 
3.6. Creation of Material Attribute in Revit 
3.6.1. In Revit, Family parameters for loadable families can be added as material attributes 
in the Family Editor . Key steps for adding a materi al attribute are described as 
follows: 
 
Figure App VI-17 Adding Material Attributes to Family Parameters for Loadable 
Families 
 
  
P106

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-19 
 
3.6.2. For Revit system families (e.g. basic ceilings, ramps), material should be set using the 
built-in “Material” parameter in the Type Properties dialog under Materials and 
Finishes. Refer to the figure below for details. 
 
Figure App VI-18 Adding Built-in Material Attributes to System Families 
 
  
P107

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-20 
 
3.6.3. For compound structures, which are system families composed of parallel layers (e.g. 
walls, floors, compound ceilings and roofs), material should be set using the built-in 
“Material” parameter for each compound structure layer in the Type Properties  
dialog under Materials and Finishes. 
 
Figure App VI-19 Adding Built-in Material Attributes to Compound Structure 
System Families 
 
  
P108

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-21 
 
3.7. Filling in Default Attributes under Room in Revit 
In Revit, Room objects already contain Name and Number as default parameters. The 
location of these attribute on “Properties” tab are described as follows: 
Figure App VI-20 Filling in Default Attributes under Room in Revit 
 
  
P109

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-22 
 
4. Types of BIM Model Attribute  
Prior to the publication of the Guidelines, some WDs have already defined and 
implemented asset owner-specific attributes . A mapping approach is utilised to 
consolidate the information whilst allowing WDs who needs to keep their pre-defined 
attributes. Four different types of LOD-I attributes exist, with different degrees of the 
alignment. This section explains their definitions and harmonisation approaches. 
4.1. Common Attributes 
Common attributes are those with the sa me attribute names and GUID with those 
listed in Table App VI-1 of this appendix. This kind of attribute name are aligned, and 
the information could be stored with the same nature for ease query. 
4.2. Common Attributes with Alternative Attribute Names 
The common attributes with alternative at tribute names are those who contain the 
same information as one of the common attributes with an  alternative name as pre-
defined by the WDs. Mapping is required to associate the WDs’ attribute names with 
the common attribute. With mapping defined, naming of the attributes from different 
WDs but with the same nature could be mapped and stored for ease query. 
For example, if multiple attributes mean ing “Asset Code” exist with names such as 
DSD.Com.Asset Code, EMSD.Common.Asset Code, which could all be mapped into 
the same column in the tabular format. Refer to figure below for an example. 
 
Figure App VI-21 Sample Tabular Format for Storing Attributes 
 
4.3. General Attributes 
The general attributes are those commonly adopted across more than one WD but 
without aligned attribute names. Similar to  Section 4.2, review is required to group 
those attributes with similar nature, prior to map these attribute names into the same 
column of the tabular format.  
P110

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-23 
 
4.4. Remaining Attributes 
Remaining attributes are the attributes that not classified as the common attributes and 
general attributes. Those attributes are di scipline-oriented and not necessary to be 
aligned. Thus, the remaining at tributes list could be stor ed without alterations to 
maintain the completeness of the information. 
  
P111

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX VI 
 
VI-24 
 
5. Mapping and Extraction of Attributes from BIM Models 
5.1. Extraction Method Overview 
After attribute mapping, extraction of attributes from BIM models could be conducted 
through authoring software’s bu ilt-in functions, scripts or plug-ins. The sections 
below describe principles of attribute extraction from Revit and Civil 3D. 
5.2. Extraction of Attributes from Revit 
The attributes in Revit can be exported to an external dataset in tabular format. The 
software default attributes and user defined attributes could be identified and extracted 
to tabular format. For example, Dynamo fo r Revit may be used to view and extract 
element parameters. 
5.3. Extraction of Attributes from Civil 3D 
For Autodesk Civil 3D, since COBie spread sheet cannot be exported directly from 
Civil 3D currently, Property Set should be defined in Civil 3D in order to extract the 
attributes in IFC format. Refer to Section 3.4 for details on Property Set. 
P112
