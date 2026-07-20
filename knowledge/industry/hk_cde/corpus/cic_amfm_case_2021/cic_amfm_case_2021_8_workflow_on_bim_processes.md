---
source_file: output/HK Standard/CIC BIM for Asset Management and Facility Management
  Case Sharing 2021.pdf
doc_id: cic_amfm_case_2021
section_id: cic_amfm_case_2021_8_workflow_on_bim_processes
title: 8. Workflow on BIM Processes
page_start: 15
page_end: 21
authority: CIC AM/FM Case Sharing 2021 §8.
authority_type: case_study
normative_weight: reference
discipline: am_fm
lifecycle_stage: operations
publication_year: 2021
software: null
priority: normal
language: en
source_url: hk_cde://cic_amfm_case_2021/cic_amfm_case_2021_8_workflow_on_bim_processes
---

# 8. Workflow on BIM Processes

Page 15 of 46 
 
5.7. Field Verification 
5.8. Model Archive 
6. BIM Standard 
6.1. BIM Standard 
6.2. COBie Standard 
6.3. List of Required Equipment 
7. Model Delivery Standard 
7.1. Software Requirement 
7.2. Coordinate System 
7.3. Revit Link Diagram 
7.4. Model File Naming Convention 
7.5. Family Naming Convention 
7.6. Model Color Scheme 
8. Drawings Production 
8.1. Drawing List / Sheet List 
8.2. Updated As-built Drawings 
9. Operation Stage Data Flow 
9.1. Operation workflow of data update 
10. Appendices, including: 
LOD Responsibility Matrix 
List of Required Equipment 
Attributes/Properties of objects for AM/FM 
Drawing List/Schedule 
 
 
 
8. Workflow on BIM Processes 
 
8.1.  BIM Model Development 
Information Management 
For the purpose of information management, a data-rich ABIM is produced. As-built drawings of building 
systems, MEP installation details and engineering specification s are the sources of existing as -built 
information. All information was verified by ATAL upon receiving from the CIC. Meanwhile the project’s 
information standards and project’s production methods and procedures , such as naming convention  
of information model and BIM objects , model breakdown structure, and settings of asset parameters 
and attributes, were strictly managed according to the CIC BIM standards and requirements and agreed

Page 16 of 46 
 
with the CIC before any production . The entire process of as -built information modelling was closely 
monitored and quality checked and assured by ATAL to comply with all requirements of the CIC. 
Guidance Note: For the planning and organisation of model breakdown structure, federation strategy as 
well as modelling methodology requirements depend, please refer to the CIC BIM standards  – General 
and relevant CIC BIM standards for recommendations. In addition, the Appointing Party and the project 
team shall take into account the project scale  and complexity, capability and requirements of the BIM 
authoring software and the BIM-enabled platform to be used for AM and facilities upkeep, as well as the 
requirements in the conversion / interfacing / integration from/between native BIM models & asset 
information to/and BIM-enabled platform for AM and facilities upkeep.   
  
8.2. As-Built Information Modelling 
Site Information 
To ensure the accuracy of the ABIM  against the actual site conditions , 360 ° cameras were used to 
capture the site conditions and served as a major reference. 360° photos and videos were produced by 
ATAL as supporting reference and route-traceable record. 
The paths / routes for capturing 360° photos and videos was planned before the site visits. All accessible 
rooms and open area s were recorded. For narrow areas, more site photos were  captured as 
supplementary records. Deviations between site record s captured by ATAL  and the existing as -built 
drawings provided by the CIC were  reported to the CIC for review and clarification. Raw data of 360 ° 
photos and videos were submitted to the CIC for reference. The CIC reviewed and compared the  360° 
photos and videos and the ABIM submitted by ATAL. 
All visible MEP services were modelled accurately according to the site conditions. MEP services which 
were covered or blocked by false ceilings were modelled with reference to the existing as-built drawings 
provided by the CIC. A specific parameter, namely “CIC_Site_Verify” would be assigned to all MEP BIM 
objects to indicate whether it was verified against site conditions. 
 
BIM Object Management & ABIM Preparation 
The project-specific BIM objects library and project template with MEP system settings were prepared 
in the beginning of the project . ATAL Building S ervice BIM Engineers collect ed all building systems 
related information provided by the CIC . All BIM objects  were prepared and developed in compliance 
with the CIC BIM standards and guidelines. BIM objects were standardised, managed and classified in a 
centralised BIM object library of the project. The relational database was verified and recognised as LOD-
I 500 c/w LOD -G 200 -400 included in the required asset, facility or equipment, such as T&C data / 
supplier records / O&M menus / as-built drawings, etc., from the BIM database. 
 
8.3. Coordination and Clash Avoidance 
By use of BIM, dedicated Building Services Engineer will identify possible design conflicts and issues.  
Software ‘Navisworks Manage’ was used for design review and coordination, to check clashes of visible 
MEP services. For any issue s found in the clash analysis process, ATAL  BIM Engineer attend ed

Page 17 of 46 
 
coordination meetings using BIM, to resolve the clashes and potential problems with the CIC before 
submitting ABIM for approval and handover to the EOMS for integration. 
 
8.4. FM/AM Data-Input & Integration 
Specified drawings and schedules were  agreed and developed from the approved ABIM . In the BIM 
authoring software ‘Revit’, parameter, namely “CIC_Data_Verify” was used for indicating BIM objects 
that have material catalogue to show its respective information. Attribute and properties of BIM objects 
for FM/AM were agreed by the CIC. Before importing the BIM model onto the EOMS , ATAL converted 
the BIM model from native format (Revit) into Forge format. A Forge converter was developed, in which 
was fully compatible with the BIM requirements and specifications by Planon and the EOMS for this 
project. 
 
8.5. Data Flow 
The flow chart below demonstrates the data flow for building up the initial ABIM and data set for the 
EOMS in this project.  
 
 
8.6. Preparing the Revit model 
Equipment List  
At early stage, an overall equipment list was created and prepared by ATAL by listing out all project 
related BIM objects (asset for FM/AM) to be included in the ABIM or EOMS. The CIC identified and

Page 18 of 46 
 
confirmed what BIM objects should be included in the EOMS and classified the BIM objects into 10 major 
categories. 
 
Sample list of required equipment extracted from the BEP of this project as follows: 
 
 
The equipment list contained basic BIM object information, such as object name (Revit Family Name ), 
LOD, location, as well as attribute fields which were suggested by Planon and approved by the CIC. Asset 
information would be inserted to these fields according to their categories. 
 
Revit Model  
LOD-I: Shared parameters were developed and created for Revit modelling according to the attribute 
fields in the equipment list. 
LOD-G: Revit models were  constructed according to as -built information, including as -built drawings, 
site record and asset catalogues. These information were consolidated and amended in the equipment 
list for model development and auditing. 
Sample LOD Responsibility Matrix extracted from the BEP of this project as follows:

Page 19 of 46 
 
 
 
 
Output data from Revit Model to EOMS 
The initial ABIM  contained latest asset information provided by the CIC and input in to Revit by ATAL. 
When the Revit model was ready, geometry and asset information was exported and transferred to the 
EOMS.  
According to the project requirements, both Forge model and a lightweight .XML format for the standard 
related to managing asset information, namely ‘Construction Operations Building Information Exchange 
(COBieLite) were submitted to Planon for asset information  mapping. Planon  requested to use an 
equipment list in .XLSX format for storing and updating asset information, this would allow Planon to 
update on the EOMS in a more efficient and compatible way during project implementation period. This 
method was agreed and approved by the CIC for data transfer in lieu of using COBieLite. Both of the 
COBieLite, equipment list and  the Forge model were submitted to Planon. In operation stage, only 
equipment list and Forge model were adopted for updating data.

Page 20 of 46 
 
 
Equipment List with Asset Information  
The equipment list with asset information  was continuously maintained and updated, and the Revit 
model was converted to the EOMS from time to time for testing . A final version of the ABIM together 
with the most updated equipment list were finally agreed and approved by the CIC before integrating 
into the EOMS.  
 
Forge Model  
The Forge model wa s generated from the Revit model as one of the deliverables to the EOMS  for 
geometry presentation. By using of the Autodesk Forge GUI and platform, Forge model (.svf) was  
produced.  
In this project, the 38 /F MEP BIM model and 39 /F MEP BIM model serve d as the master files when 
uploading to the Forge platform. The linked Architectural ( ARC) and Structural (STR) BIM models were 
uploaded together with the master files. In Forge, geometry of the Revit BIM objects could be mapped 
with asset information by their asset code (refer to CIC.Common.AssetCode in the equipment list) and 
GUID (refer to LinkBIMGUID in the equipment list). 
Sample asset code as follows, please refer to Section 11 for more details. 
• First Exhaust Fan at 38/F: HQ-NA-038-AC-EAD-EAF-001 
• Second Exhaust Fan at 38/F: HQ-NA-038-AC-EAD-EAF-002 
  
For BIM objects from linked files, their GUI Ds (LinkBIMGUID) were added with the Linked Revit Model 
GUIDs as a prefix to their original GUIDs. This Linked Revit Model GUIDs were generated automatically 
when a model file is linked to the master file. 
Example: 
 MEP File (Master) 
 
ARC File STR File 
Linked Revit Model 
GUID in Master File 
 
N/A e.g.  
2558c4e6-cdff-4fe2-
81e2-51bf8e89da5e-
00102705 
e.g.  
e75eb4fc-f590-4df8-
849b-01f311d707ad-
000331b4 
 
Original Object GUID 
 
e.g.  
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00099ea4 
 
e.g.  
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00011ab2 
e.g.  
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00033cd3 
LinkBIMGUID 
 
(Linked Revit Model 
GUID in Master File  / 
Original Object GUID) 
e.g.  
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00099ea4 
e.g.  
2558c4e6-cdff-4fe2-
81e2-51bf8e89da5e-
00102705 / 
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00011ab2 
 
e.g.  
e75eb4fc-f590-4df8-
849b-01f311d707ad-
000331b4 /  
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00033cd3

Page 21 of 46 
 
 
8.7. Quality Assurance and Control 
A list of items and procedure were developed aiming to facilitate reviewing and quality checking of the 
BIM models in terms of LOD-G and LOD-I, which had to satisfy the requirements of the CIC. 
QA Items QC Support 
Information  
• Layout Information 360° Video and Images Verification; Site photos 
Verification; As-built drawings verification 
• Asset Information 
 
O&M Manual Checking; Catalogue Checking 
Modelling Quality  
• Issue Management 
 
Visual Checking; Clash Analysis (Navisworks Manage) 
• Level of Development (LOD) 
 
LOD equipment list; LOD system list 
Standards  
• Modelling Standard 
 
Modelling Standard Checklist  
• Drawings Standard 
 
Drawing Standard Checklist 
 
8.8. Field Verification 
Field Verification Method  
Visual Inspection 360° camera, site photos and videos 
Drawings Verification As-built Drawings 
 
In Revit, parameter “CIC_Site_Verify” was used for indicating BIM objects that were checked with field 
verification, such as images, 360° image / video. 
 
8.9. Model Archive 
Deliverables in the format below were completed by ATAL and submitted to the CIC: 
• BIM models of 38/F and 39/F in native format (.rvt) 
• BIM models of 38/F and 39/F in Forge format (.svf) 
• Equipment List of 38/F and 39/F in Excel format (.xlsx) 
• Asset data files of 38/F and 39/F in COBieLite format (.xml)
