---
source_file: output/HK Standard/CIC_ZCP_BIMIPv1-5_withAppendices.pdf
doc_id: cic_zcp_bimip_v15
section_id: cic_zcp_bimip_v15_2_6_project_information_production_methods_and_procedures
title: 2.6. Project Information Production Methods and Procedures
page_start: 28
page_end: 35
authority: CIC ZCP BIM Implementation Plan v1.5 §2.6.
authority_type: case_study
normative_weight: reference
discipline: implementation
lifecycle_stage: project
publication_year: 2022
software: null
priority: normal
language: en
source_url: hk_cde://cic_zcp_bimip_v15/cic_zcp_bimip_v15_2_6_project_information_production_methods_and_procedures
---

# 2.6. Project Information Production Methods and Procedures

Supply and Installation of Internet of Things (IoT) and Building Information Modelling (BIM) at 
Construction Industry Council - Zero Carbon Park 
BIM Implementation Plan 
 
 
28 
 
 
No. System Description 
Presentation (2D) Presentation (3D) 
Line 
Weight Line Type R, G, B Colour 
Palette 
9 Communication 
System 
 0.35 Continuous 128, 255, 255  
10 Lighting  0.35 Center2 0, 255, 0  
11 Electrical 
Distribution 
 0.35 Divide2 0, 255, 0  
12 Plumbing 
System 
Cold Water 
Pipe System 
0.25 Long Dash 0, 0, 255  
Flushing 
Water Pipe 
System 
0.25 Centre 255, 255, 0 
 
13 Drainage 
System 
 0.35 Divide2 128, 128, 0  
14 Water Leakage 
Detection 
System 
Leak 
Detection 
Cable 
0.35 Continuous 122, 48, 160 
 
15 Photovoltaic 
Panel System 
Solar panels, 
cable 
containment, 
inverter, 
transformer 
0.35 Divide2 0, 255, 0 
 
16 Saltwater 
treatment 
system 
 0.25 Centre 255, 255, 0 
 
 
2.6. Project Information Production Methods and Procedures 
Table 10 shows the document delivery formats and their submissions dates. 
Table 10. Document delivery formats and requirements 
Deliverables Format Submission Date 
1. BIM Implementation 
Plan 
.pdf & .docx Within 2 weeks after commencement date 
of the Works 
2. Asset Data Worksheets .xls Within 6 weeks after commencement date 
of the Works 
3. BIM Object .rfa Within 60 calendar days after 
commencement date of the Works 
4. As-built Model with 
Asset Data 
.rvt, .ifc & .svf Within 60 calendar days after 
commencement date of the Works 
5. Asset Data File .xml (COBieLite) Within 60 calendar days after 
commencement date of the Works

Supply and Installation of Internet of Things (IoT) and Building Information Modelling (BIM) at 
Construction Industry Council - Zero Carbon Park 
BIM Implementation Plan 
 
 
29 
 
 
Deliverables Format Submission Date 
6. As-built Drawings .pdf Within 60 calendar days after 
commencement date of the Works 
 
2.6.1. Details on BIM Use 1 & 2: Existing and As-built Verification 
As stated in section 4.8 1) of the EIR, the Contractor shall incorporate existing conditions and 
verify as-built conditions through a number of methods. These methods are listed in Table 11.  
Table 11. Methods for field verification 
Verification Type Verification Source 
Visual Inspection 360 camera, Site photos, videos,  
Drawings Verification As-built Drawings 
Survey Traditional Surveying techniques, UAS/LiDAR/laser scanning 
Other Digital map products available from the Lands Department  
 
In Revit, parameter “CIC_Site_Verify” is used for indicating obj ects that are checked with on -
site verification, such as images, 360 image/video, and point cloud data. 
2.6.2. Details on BIM Use 4: Data Requirements for Asset Management 
As stated in section 4. 8.4 of the EIR, the CIC’s facility manager shall specify the data re quired 
for the asset management of each element. The detailed list of agreed equipment is provided in 
Appendix B : List of Required Equipment . The equipment list will contain basic object 
information such as BIM Obje ct Name, LOD, Location, as well as attribute fields which are 
requested by Planon and approved by CIC. Asset data will be inserted to these fields according to 
their dedicated FM category. 
The associated attributes are provided in Appendix C : Attribute s / Properties of objects for 
FM/AM. Shared parameters will be developed and created for model elements according to the 
attribute fields in the equipment list. 
Figure 4 shows the workflow for the creation of the bi -directional link of the BIM model to the 
asset management data set. This workflow will be aligned with Appendix IV of the tender 
documentation, Integration Specification Document for Construction Industry Council (CIC)  - 
Version: 01, Date 19 Apr 2021.

Supply and Installation of Internet of Things (IoT) and Building Information Modelling (BIM) at 
Construction Industry Council - Zero Carbon Park 
BIM Implementation Plan 
 
 
30 
 
 
 
 
Figure 4. Workflow for creation of initial model with the input of asset management data 
2.6.3. Details on BIM Use 4: Use of Autodesk Forge in Asset Data 
Workflow 
As shown in Figure 4, an Autodesk Forge model (.svf) is generated from the Revit model so that 
it can be brought into the Planon software system as a 3D model. The asset data contained in each 
Revit element in the equipment list is then mapped to its Forge counterpart by using its asset code 
(refer to the CIC.Common.AssetCode in Appendix C : Attribute s / Properties of objects for 
FM/AM) and its GUID (refer to CIC.Common.BIMGUID in Appendix C: Attributes / Properties 
of objects for FM/AM).

Supply and Installation of Internet of Things (IoT) and Building Information Modelling (BIM) at 
Construction Industry Council - Zero Carbon Park 
BIM Implementation Plan 
 
 
31 
 
 
For elements from linked Revit files, their GUID (LinkBIMGUID) is prepended with the Linked 
Revit Model GUID. This Linked Revit Model GUID is generated automatically when a model 
file is linked to the master file. An example is show in Table 12. 
Table 12. Example of GUID formatting across linked Revit files 
 MEP File (Master) ARC File STR File 
Linked Revit Model 
GUID in Master 
File 
 
N/A e.g.  
2558c4e6-cdff-4fe2-
81e2-51bf8e89da5e-
00102705 
e.g.  
e75eb4fc-f590-4df8-
849b-01f311d707ad-
000331b4 
 
Original Object 
GUID 
 
e.g.  
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00099ea4 
 
e.g.  
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00099ea4 
e.g.  
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00099ea4 
LinkBIMGUID 
 
(Linked Revit 
Model GUID in 
Master File/ 
Original Object 
GUID) 
e.g.  
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00099ea4 
e.g.  
558c4e6-cdff-4fe2-
81e2-51bf8e89da5e-
00102705/ 
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00099ea4 
 
e.g.  
e75eb4fc-f590-4df8-
849b-01f311d707ad-
000331b4/  
ce54ee25-3eec-4c6b-
9dd4-8486e5d1dcde-
00099ea4 
 
2.6.4. Details on BIM Use 4: Data Exchange via COBieLite 
The use of COBieLite export files is specified in sections 10.3 and 10.4 of the EIR a nd is the 
means of achieving an OpenBIM approach to a bi-directional data exchange with the CIC EOMS 
platform. 
2.6.5. Details on BIM Use 4: Operations-phase Model and Data Updates 
During the operations phase, new assets will inevitably be required to be introduced to t he AIM. 
This will involve both adding (or changing) model geometry and inputting (or updating) data. 
Figure 5 illustrates the proposed workflow for such a change. Users are suggested to input data 
with this operation stage data flow. The workflow relies on the Revit model, the Forge model, and 
the updated Equipment List with asset data (see Appendix B: List of Required Equipment).  
It should be noted that the key objective is to ensure that information for asset items - both existing 
and new - is incorporated into the CIC’s EOMS platform completely and accurately. Whether this 
is achieved through the use of the Equipment List or, a s stated in section  2.6.4, by COBieLite, 
will be subject to the technical specifications and best practices of the EOMS platform.

Supply and Installation of Internet of Things (IoT) and Building Information Modelling (BIM) at 
Construction Industry Council - Zero Carbon Park 
BIM Implementation Plan 
 
 
32 
 
 
 
Figure 5. Workflow for update of model and data during operations phase 
Below are the detailed steps of producing the updated equipment list from the Revit model: 
 Step 1 - Request to add new items and data 
When a new item is proposed to be added to the model, the user shall start by editing the latest 
equipment list. The user should add a new row for the i tem on the correct FM category page in 
the equipment list. All asset data fields, except LinkBIMGUID and CIC.Common.BIMGUID 
should be filled in. See Figure 6 
 
Figure 6. Equipment List with Model Data and Asset Data

Supply and Installation of Internet of Things (IoT) and Building Information Modelling (BIM) at 
Construction Industry Council - Zero Carbon Park 
BIM Implementation Plan 
 
 
33 
 
 
 Step 2 - Modelling and data input 
Modellers can build up the objects in the model according to the equipment list. The new object 
should be assigned with a BIM Object name and a unique asset ID (CIC.Common.AssetCode) 
which conforms to project BIM standards. At the same time, the data in Table 13 and Table 14 
below should be input manually into the model: 
Table 13. Model Data for manual input 
Parameter Description Data Format 
in Revit Model 
CIC_Element ID Refer to “Element ID” in Equipment List; 
The value of the parameter referenced the unique 
ID generated from by Revit (Element ID). This 
value is only unique in its own file an d is 
extracted for easy checking internally. This 
project will use CIC.Common.AssetCode, which 
is unique across all files, for mapping data into 
the Planon system. 
Text 
CIC_LOD Refer to “LOD” in Equipment List; 
This parameter indicates the LOD requirement  
of each BIM object. 
Text 
CIC_Site_Verify Refer to “Site Verify” in Equipment List; 
This parameter indicates whether the BIM object 
was site-verified. 
Ys/No 
CIC_Data_Verify Refer to “Data Verify” in Equipment List; 
This parameter indicates whether catalo gues or 
detailed drawings of BIM objects were provided 
and if the BIM object was built according to 
these information sources. 
Ys/No 
CIC_OmniClass_Number Refer to “OmniClass Number” in Equipment 
List; 
This parameter refers to the properly formatted 
OmniClass Number of the BIM object. 
xx-xx xx xx xx 
xx 
CIC_Shared_Parameter A parameter used to for the purposes of 
extracting equipment schedules from Revit and 
organising the data in accordance with the 
established equipment list for the project. 
Text

Supply and Installation of Internet of Things (IoT) and Building Information Modelling (BIM) at 
Construction Industry Council - Zero Carbon Park 
BIM Implementation Plan 
 
 
34 
 
 
Table 14. Asset data for manual input 
Parameter Description Data Format in 
Revit Model 
All asset data provided by 
user in equipment list 
(Except LinkBIMGUID and 
CIC.Common.BIMGUID) 
Refer to Planon’s fields/Asset data in 
Equipment List; 
These data are provided by user and should 
be input into the model. 
Text 
 
In the master file Revit file, the name of the Linked Revit Model should be input with its File 
GUID. By doing so, the LinkBIMGUID of each linked element can be formulated in Revit 
schedules and be used for data mapping into the Planon FM system, see Table 15 and Figure 7. 
Table 15. Linked Revit Model Properties 
Parameter Description Data Format in 
Revit Model 
Name The value of this parameter should be inputted into the 
Linked Revit Model GUID, which is generated 
internally as the “UniqueId” in the Revit master file.  
See Figure 7. 
Text 
 
 
Figure 7. Name parameter of the linked Revit model (example for reference from CIC HQ project)

Supply and Installation of Internet of Things (IoT) and Building Information Modelling (BIM) at 
Construction Industry Council - Zero Carbon Park 
BIM Implementation Plan 
 
 
35 
 
 
 Step 3 - Export Excel worksheets 
After modelling and data input, pre-defined Revit schedules can be exported as Excel worksheets 
using the Revit plugin “Export -Import Excel”. For each Revit file, there are 10 predefined 
schedule templates for exporting, see Table 16. 
Table 16. Schedule templates for Excel export 
Schedule Name in Revit FM Category 
CICZCP_FM_AC AC 
CICZCP_FM_FS FS 
CICZCP_FM_PD PD 
CICZCP_FM_EL EL 
CICZCP_FM_LIFT LIFT 
CICZCP_FM_ELV ELV 
CICZCP_FM_BLDG BLDG 
CICZCP_FM_LAND LAND 
CICZCP_FM_FE FE 
CICZCP_FM_OTH OTH 
 
In addition to the data that was manually input during modelling, the data in Table 17 and  
Table 18 and will also be generated automatically and included in the schedules: 
Table 17. Additional model data generated automatically and included in the schedules 
Parameter Description Data Format in 
Revit Model 
BIM Object Refer to “ BIM Object  Name” in Equipment 
List; 
This parameter indicates the Name of the BIM 
Object. 
Text 
Type Refer to “Type Name” in Equipment List; 
This parameter indicates the Type Name of the 
BIM object. 
Text 
Category Refer to “Model Category” in Equipment List; 
This parameter indicates the Revit Category 
used for building the BIM object. 
Text 
OmniClass Number Refer to “Omni Class Number” in Equipment 
List; 
Text
