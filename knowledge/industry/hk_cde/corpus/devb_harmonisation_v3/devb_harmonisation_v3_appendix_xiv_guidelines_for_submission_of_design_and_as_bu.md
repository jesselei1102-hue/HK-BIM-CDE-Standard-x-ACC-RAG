---
source_file: output/HK Standard/DEVB BIM Harmonisation Guidelines for WDs (v3_0) with
  All Appendices.pdf
doc_id: devb_harmonisation_v3
section_id: devb_harmonisation_v3_appendix_xiv_guidelines_for_submission_of_design_and_as_bu
title: Appendix XIV - Guidelines for Submission of Design and As-built BIM Models
  to LandsD (v3.0)
page_start: 156
page_end: 169
authority: DEVB BIM Harmonisation v3.0 §Appendix
priority: high
language: en
source_url: hk_cde://devb_harmonisation_v3/devb_harmonisation_v3_appendix_xiv_guidelines_for_submission_of_design_and_as_bu
---

# Appendix XIV - Guidelines for Submission of Design and As-built BIM Models to LandsD (v3.0)

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
Appendix XIV -  Guidelines for Submission of Design and As-built BIM 
Models to LandsD 
 
P156

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
TABLE OF CONTENTS 
 
1. Introduction .................................................................................................................................. XIV-1 
2. The Essentials for Successful BIM Data Submission to GBDR ................................................ XIV-2 
2.1 Folder Structure for BIM Data Submission .................................................................................... XIV-2 
2.2 Completeness Check for BIM Data Submission ............................................................................ XIV-6 
3. BIM Data Submission to GBDR ................................................................................................. XIV-7 
3.1 Submission via the GBDR Web User Interface ............................................................................. XIV-7 
3.2 Submission using GBDR BIM APIs .............................................................................................. XIV-9 
4. Checklist for the Complete BIM Data Submission .................................................................. XIV-12 
 
 
 
List of Tables 
Table App XIV-1 Subfolders at Level 1 ......................................................................................................... XIV-3 
Table App XIV-2 Subfolders at Level 2 ......................................................................................................... XIV-3 
Table App XIV-3 Subfolders at Level 3 ......................................................................................................... XIV-3 
Table App XIV-4 Subfolders at Level 4 ......................................................................................................... XIV-3 
Table App XIV-5 Subfolders at Level 5 ......................................................................................................... XIV-3 
Table App XIV-6 Subfolders at Level 6 ......................................................................................................... XIV-4 
Table App XIV-7 Subfolders at Level 7 ......................................................................................................... XIV-5 
Table App XIV-8 BIM Submission Requirements ......................................................................................... XIV-6 
Table App XIV-9 Examples of GBDR BIM APIs ......................................................................................... XIV-9 
 
 
 
List of Figures 
Figure App XIV-1 The 7-Level Folder Structure in GBDR ........................................................................... XIV-2 
Figure App XIV-2 Input Project Details ......................................................................................................... XIV-7 
Figure App XIV-3 Assign Files to the Corresponding Subfolders ................................................................. XIV-8 
Figure App XIV-4 BIM API Document on the GBDR Website .................................................................. XIV-10 
Figure App XIV-5 GBDR BIM API Sandbox .............................................................................................. XIV-10 
Figure App XIV-6 Response Simulated by GBDR BIM API Sandbox ....................................................... XIV-11 
P157

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-1 
 
1 Introduction 
1.1.1 The Government BIM Data Repository (GBDR) serves as the common platform for 
territory-wide BIM data sharing across the Government in support of BIM 
Harmonisation and continuously uplifting of BIM data quality, enabling seamless 
BIM/GIS data integration to support smart city applications.  
 
1.1.2 Currently, the GBDR provides two submission modes: 
 Web User Interface of the GBDR, and  
 GBDR BIM Application Programming Interfaces (APIs). 
 
1.1.3 This appendix outlines the requirements for submitting BIM data to the GBDR to 
facilitate effective BIM data sharing. It also provides comprehensive guidance to the 
data providers in arranging BIM submission to LandsD using the two aforementioned 
submission modes of the GBDR.  
 
P158

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-2 
 
2 The Essentials for Successful BIM Data Submission to GBDR 
2.1. Folder Structure for BIM Data Submission 
2.1.1. To facilitate efficient and structured BIM data management, a standardised 7-level 
folder structure is being implemented for uploading and storing of BIM data in the 
GBDR.  This hierarchical structure (refer to Figure App XIV-1) is designed to 
streamline submission procedures, ensure consistency, and support robust BIM data 
organisation and management across projects.  
 
Figure App XIV-1 The 7-Level Folder Structure in GBDR 
 
 
2.1.2. Folders and subfolders for BIM data submission across all seven levels are 
systematically created by the GBDR, based on project information collected by 
Development Bureau (DEVB) from works departments (WDs).  
P159

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-3 
 
2.1.3. The descriptions of folder and subfolder from Level 1 to Level 7 are summarised 
below:- 
Table App XIV-1 Subfolders at Level 1 
Subfolder name Description 
ArchSD Architectural Services Department 
CEDD Civil Engineering and Development Department 
DSD Drainage Services Department 
EMSD Electrical and Mechanical Services Department 
HyD Highways Department 
WSD Water Supplies Department 
 
Table App XIV-2 Subfolders at Level 2 
Subfolder name Description 
CONTRACT / CONSULTANCY 
NUMBER 
Contract number or consultancy agreement 
number of projects with BIM adoption, collected 
by DEVB from WDs 
 
Table App XIV-3 Subfolders at Level 3 
Subfolder name Description 
DESIGN Design BIM model submission  
AS-BUILT As-built BIM model submission 
 
Table App XIV-4 Subfolders at Level 4 
Subfolder name Description 
HARMONISED BIM models that comply with DEVB BIM 
Harmonisation Guidelines for WDs 
NON-HARMONISED BIM models that do not comply with DEVB BIM 
Harmonisation Guidelines for WDs 
REVAMPED BIM models revamped by LandsD  to comply 
with DEVB BIM Harmonisation Guidelines for 
WDs
 
Table App XIV-5 Subfolders at Level 5 
Subfolder name Description 
P160

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-4 
 
01 SHARED BIM data submitted by WDs 
02 CONVERTED Open BIM data in IFC format and Open GIS data 
in CityGML format converted by LandsD 
(Only for harmonised or revamped BIM models) 
03 ARCHIVE For data archive 
 
Table App XIV-6 Subfolders at Level 6 
Subfolder name Description 
1_1 RVT BIM models in Autodesk Revit format (.rvt) 
1_2 C3D BIM models in Autodesk Civil 3D format (.dwg) 
1_3 IFC BIM models in IFC format (.ifc) 
1_4 NWD A federated model of the project in Autodesk 
Navisworks Document format (.nwd) 
1_5 PROJECT_BOUNDARY Project boundary file in GIS or CAD format 
of .dwg, .shp or .dgn 
[Refer to Appendix XIII for details] 
1_6 MODEL_FILE_LIST An excel file (.xlsx) detailing all files to be 
submitted under the project, including BIM data, 
project boundary, etc. 
[Refer to Appendix XIII for required input details] 
1_7 OTHER_NATIVE_BIM BIM models in formats other than RVT, C3D and 
IFC, such as Archicad, OpenBuildings Designer, 
OpenRoads Designer, Tekla, SketchUp, etc. 
[Refer to “Details of subfolders  at Level 7” in Section 2.1] 
1_8 PROJECT_SPECIFIC_CODE A configuration file in JSON format (.json) that 
defines project-specific file naming conventions. 
 (Applicable only to harmonised or revamped 
BIM models) 
[Refer to Native BIM Validation Tool package 
available on GBDR website] 
2_1 EXTRACTED_REVIT Extracted set of “1_1 RVT” (.rvt) converted by 
the GBDR 
2_2 EXTRACTED_C3D Extracted set of “1_2 C3D” (.dwg) converted by 
the GBDR 
2_3 FULL_IFC Full set of IFC models converted by the GBDR  
from “1_1 RVT” and “1_2 C3D” (.ifc) 
 
2_4 EXTRACTED_IFC Extracted set of “2_3 FULL_IFC” (.ifc) 
converted by the GBDR
 
P161

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-5 
 
Subfolder name Description 
2_5 FULL_CITYGML Full set of CityGML models converted by the 
GBDR from “2_3 FULL_IFC” (.gml)  
2_6 EXTRACTED_CITYGML Extracted set of “2_5 FULL_CITYGML” (.gml) 
converted by the GBDR 
 
Table App XIV-7 Subfolders at Level 7 
Subfolder name Description 
1_7_1 ARCHICAD BIM models created using Archicad (.pln) 
1_7_2 OPENBUILDINGS_DESIGNER BIM models created using OpenBuildings 
Designer (.dgn)
 
1_7_3 OPENROADS_DESIGNER BIM models created using OpenRoads Designer 
(.dgn) 
1_7_4 TEKLA BIM models created using Tekla Structures (.zip) 
[A zip file of the whole model folder] 
1_7_5 SKETCHUP BIM models created using SketchUp (.skp) 
 
  
P162

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-6 
 
2.2. Completeness Check for BIM Data Submission 
2.2.1 WDs can submit BIM data either through the GBDR Web User Interface or using 
the GBDR BIM APIs. Both submission modes are supported by streamlined 
procedures for uploading BIM data, which are detailed in Sections 3.1 to 3.2. 
2.2.2 Once non-harmonised, harmonised, or revamped models are uploaded to the 
appropriate  subfolders under the “01 SHARED” folder, the GBDR will 
automatically initiate a completeness check mechanism. This backend mechanism 
check whether all the necessary files have been included in the submission to the 
GBDR.  
2.2.3 A summary of the submission requirements is provided in Table App XIV-8 BIM 
Submission Requirements. If the system detects any missing data or incomplete 
submission, an email notification will be sent to the respective WD for follow up. 
Table App XIV-8 BIM Submission Requirements 
File Format 
Allowable  
File 
Extension 
Subfolder Name Mandatory 
/ Optional 
BIM File 
Revit .rvt  1_1 RVT  
Mandatory 
 
Note: 
submit  
at least  
one format
 
Civil 3D .dwg  1_2 C3D  
IFC  .ifc  1_3 IFC 
Archicad .pln 1_7_1 ARCHICAD  
OpenBuildings 
Designer .dgn  1_7_2 OPENBUIL DINGS_DESIGNER  
OpenRoads 
Designe
r .dgn  1_7_3 OPENROADS_DESIGNER  
Tekla .zip  1_7_4 TEKLA  
SketchUp  .skp  1_7_5 SKETCHUP  
Reference File 
Navisworks  .nwd 1_4 NWD Optional 
Project Boundary 
GIS / CAD .dwg/.dgn/.shp 1_5 PROJECT_BOUNDARY  Mandatory 
Model File List 
Excel .xlsx  1_6 MODEL_FILE_LIST  Mandatory 
Project Specific Code 
JSON .json  1_8 PROJECT_SPECIFIC_CODE Mandatory 
 
Note: 
not required 
for  non-
harmonised 
BIM data 
submission 
 
 
P163

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-7 
 
3 BIM Data Submission to GBDR 
3.1 Submission via the GBDR Web User Interface 
To submit BIM data via the GBDR Web User Interface, follow the steps outlined below. 
3.1.1 Login to the GBDR. 
3.1.2 Click “BIM Data Submission”. 
3.1.3 Input the required project details (refer to Figure App XIV-2). Then, click “Select Data”.  
Figure App XIV-2 Input Project Details 
(Note: This figure is for illustration purpose only.)  
 
 
 
3.1.4 Click “ ADD FILE”  to add files in accordance with the requirements set out in  
Table App XIV-8 BIM Submission Requirements. Ensure that all files meet the prescribed 
format to facilitate successful submission to the GBDR. 
 
3.1.5 Click to assign the added files to th e corresponding subfolders. Then, Click “Next ”. 
(Refer to Figure App XIV-3) 
 
 
 
 
P164

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-8 
 
 
Figure App XIV-3 Assign Files to the Corresponding Subfolders 
(Note: This figure is for illustration purpose only.) 
 
 
3.1.6 Add reference file(s), if applicable. Click “Next”. 
 
3.1.7 Click “Confirm Data Upload” to proceed with uploading the selected files to the GBDR. 
Once the process is complete, check the upload status of each file to ensure successful 
submission. 
 
3.1.8 To delete any previously submitted f iles from the GBDR, navigate to the relevant 
subfolder, and select the file to be removed. Then, click to initiate the deletion process. 
 
3.1.9 A message box will appear once the deletion process is completed. Click “Close”.  
 
  
P165

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-9 
 
3.2 Submission using GBDR BIM APIs 
3.2.1 To support the development of system interfacing between the GBDR and the BIM 
Common Data Collaboration Platform (CDCP) or BIM/GIS applications of WDs, a 
suite of BIM APIs has been developed (refer to Table App XIV-9). These BIM APIs 
enable direct submission of BIM models and data from WDs’ CDCP and systems to 
the GBDR, and the retrieval of BIM data from the GBDR for further use and analysis 
in the WDs’ CDCP and systems.  
3.2.2 For detailed specifications and implementation guidelines, please refer to the BIM 
API Document available on the GBDR website (refer to Figure App XIV-4). 
 
Table App XIV-9 Examples of GBDR BIM APIs 
 
API Name Description 
Login to Government BIM 
Data Repository 
This API is provided for logging into the Government BIM 
Data Repository with UserID and SessionKey. 
Retrieve BIM Model List This API is provided for retrieving the full list of BIM 
models available for downloa d. Before downloading the 
BIM Model, users may apply filters to narrow of selection 
based on the parameters provided. If no filters are 
specified, a complete list is returned. 
Select and Download BIM 
Files 
This API is provided for selecting specific BIM model files 
from the list for download. 
Get Download URL for BIM 
Model 
This API is provided for obtaining the URL needed to 
download the selected BIM models. 
Get Contract and 
Department Information 
This API is provided for retrieving Contract and 
Department information from the list of project 
information provided by DEVB collected from WDs. 
Upload BIM File This API is provided for uploading BIM files and other 
data to the GBDR. 
Checking if File Exists This API is provided for checking whether a specific BIM 
file already exists in the GBDR. 
Delete BIM File This API is provided for deleting previously submitted 
BIM files from the GBDR. 
Check BIM File Upload 
Status 
This API is provided for checking the upload status of BIM 
files submitted to the GBDR. 
 
P166

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-10 
 
Figure App XIV-4 BIM API Document on the GBDR Website 
 
3.2.3 In addition to the API documentation, LandsD has developed the GBDR BIM API 
Sandbox (refer to Figure App XIV-5) to assist IT developers and contractors of WDs 
in simulating API responses. This sandbox environment supports system interfacing 
development, testing and integration workflows (refer to Figure App XIV-6) , which 
is accessible on GBDR website.  
Figure App XIV-5 GBDR BIM API Sandbox 
 
  
P167

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-11 
 
Figure App XIV-6 Response Simulated by GBDR BIM API Sandbox 
 
P168

DEVB BIM HARMONISATION GUIDELINES  
FOR WORKS DEPARTMENTS    APPENDIX XIV  
 
XIV-12 
 
4 Checklist for the Complete BIM Data Submission 
4.1.1 This checklist can be used to check that all essential items are prepared for a 
successful BIM data submission to the GBDR. 
Checklist for Complete BIM Data Submission 
A Project Details  
A1 Project Type  Consultancy Agreement  Works Tender 
A2 Stage  Design (D)  As-built (AB) 
A3 Comply with the DEVB BIM  
Harmonisation Guidelines for WDs?  Yes [Harmonised]  No [Non-Harmonised] 
 
B Data Upload  
B1 Submit at least one format: 
1_1 RVT (.rvt) 1_2 C3D (.dwg) 
1_3 IFC (.ifc) 1_7_1 ARCHICAD (.pln) 
1_7_2 OPENBUILDINGS_DESIGNER(.dgn) 1_7_3 OPENROADS_DESIGNER (.dgn) 
1_7_4 TEKLA (.zip)  
*only one ZIP file for the whole model 1_7_5 SKETCHUP (.skp) 
B2 Submit all of the below information:  
1_5 PROJECT_BOUNDARY  
(.dwg, .shp or .dgn) 
 
*Submit ONLY ONE file 
File Name: Project boundary.dwg/.shp/.dgn 
1_6 MODEL_FILE_LIST (.xlsx) 
 
*Submit ONLY ONE file 
File Name: Model file list.xlsx 
Mark all files in “1_1”, “1_2”, “1_3”, “1_5”, “1_7” and “1_8” 
B3  If select “Yes” in item A3 of this checklist, submit below information:  
1 8 PROJECT_SPECIFIC_CODE (.json) 
 
*Submit ONLY ONE file 
File Name: Project specific code.json
 
Note: This checklist is intended to help users review the completeness of the data files before uploading them to the GBDR.  
It is provided for guidance only and is NOT required as part of the submission. 
 
P169
