---
source_file: output/HK Standard/CIC BIM for Asset Management and Facility Management
  Case Sharing 2021.pdf
doc_id: cic_amfm_case_2021
section_id: cic_amfm_case_2021_13_upkeep_of_model_geometry_and_information_in_o_m_stage
title: 13. Upkeep of Model Geometry and Information in O&M Stage
page_start: 33
page_end: 36
authority: CIC AM/FM Case Sharing 2021 §13.
authority_type: case_study
normative_weight: reference
discipline: am_fm
lifecycle_stage: operations
publication_year: 2021
software: null
priority: normal
language: en
source_url: hk_cde://cic_amfm_case_2021/cic_amfm_case_2021_13_upkeep_of_model_geometry_and_information_in_o_m_stage
---

# 13. Upkeep of Model Geometry and Information in O&M Stage

Page 33 of 46 
 
13. Upkeep of Model Geometry and Information in O&M Stage  
 
Native format of BIM models would be updated in Revit. When data update involves changes in model 
geometry, for examples, adding objects or attributes, users are suggested to input data by following the 
operation stage data flow  below. In this data flow, Forge model and equipment list with asset 
information should be exported to EOMS. Since the equipment list with asset information  will be the 
major tool for transferring data, the COBieLite exported will not be imported to EOMS . The following 
are the detailed steps of producing an updated equipment list from Revit model: 
13.1. Request to add new items and data 
When a new item is proposed t o be added in BIM model, user should  start with editing the latest 
equipment list. User should add a new row for the item on the correct asset category page within the 
equipment list. All asset information  except LinkBIMGUID and CIC.Common.BIMGUID should b e filled 
correctly. 
 
13.2. Modelling and data input 
BIM objects should be built up in the BIM model according to the equipment list. The new BIM object 
should be assigned with an object name and a unique asset ID (CIC.Common.AssetCode), which in lines 
with project BIM standards.  
At the same time, the following data should be input manually into the BIM model: 
Model Data 
Parameter Description Data Format in 
Revit Model 
CIC_Element ID Refer to “Element ID” in Equipment List; 
The value of this parameter makes reference to the 
unique ID generated from Revit model (Element ID). 
This value is only unique in its own file and is 
extracted for easy checking internally. This project 
will use CIC.Common.AssetCode, which is unique 
across all files, for mapping data in Planon system. 
Text 
CIC_LOD Refer to “LOD” in Equipment List; 
This parameter indicates the LOD requirement of 
each BIM object. 
Text 
CIC_Site_Verify Refer to “Site Verify” in Equipment List; 
This parameter indicates whether the BIM object 
was site-verified. 
Yes/No 
CIC_Data_Verify Refer to “Data Verify” in Equipment List; 
This parameter indicates whether catalogues or 
detailed drawings of BIM objects was provided and 
the BIM object was built according to these 
information. 
Yes/No

Page 34 of 46 
 
Asset Information 
Parameter Description Data Format in 
Revit Model 
All asset information provided by 
user in equipment list (Except 
LinkBIMGUID and 
CIC.Common.BIMGUID) 
Refer to Planon’s fields/ asset information in 
Equipment List; 
These data are provided by user  and should be 
input into the model. 
Text 
 
In the master BIM model file (MEP BIM model ), the name of the Linked Revit Model should be input 
with its File GUID. By this, the LinkBIMGUID of each linked element can be formulated in Revit schedules 
and be used for data mapping in the EOMS. 
 
Linked Revit Model Properties 
Parameter Description Data Format in 
Revit Model 
Name The value of this parameter should be input the 
Linked Revit Model GUID, which is generated 
internally in the Revit master file. 
Text 
 
Example:

Page 35 of 46 
 
 
13.3. Export Excel worksheets 
After modelling and data input, pre-defined Revit schedules can be exported as Excel worksheets using 
Revit plugin “Export-Import Excel”.  
In each Revit file, there are 10 schedule templates ready for export: 
Schedule Name in Revit Asset Category 
CICHQ_FM_AC AC 
CICHQ_FM_FS FS 
CICHQ_FM_PD PD 
CICHQ_FM_EL EL 
CICHQ_FM_LIFT LIFT 
CICHQ_FM_ELV ELV 
CICHQ_FM_BLDG BLDG 
CICHQ_FM_LAND LAND 
CICHQ_FM_FE FE 
CICHQ_FM_OTH OTH 
 
Apart from the manual data input during modelling, the data below will be generated from Revit 
automatically and included in the schedules: 
Model Data 
Parameter Description Data Format in 
Revit Model 
Family Refer to “Family Name” in Equipment List; 
This parameter indicates the  Family Name of the 
BIM object. 
Text 
Type Refer to “Type Name” in Equipment List; 
This parameter indicates the Type Name of the BIM 
object. 
Text 
Category Refer to “Model Category” in Equipment List; 
This parameter indicates the Revit Category used for 
building the BIM object. 
Text 
OmniClass Number Refer to “Omni Number” in Equipment List; 
This parameter indicates the Omni Class number 
classified for the BIM object. 
Text 
OmniClass Title Refer to “Omni Title” in Equipment List; 
This parameter indicates the Omni Class title 
classified for the BIM object. 
Text

Page 36 of 46 
 
Asset Information 
Parameter Description Data Format in Revit 
Model 
CIC.Common.BIMGUID Refer to “CIC.Common.BIMGUID” in Equipment List; 
The value of this parameter is generated internally 
in Revit models. 
Text 
LinkBIMGUID Refer to “LinkBIMGUID” in Equipment List; 
This parameter is a combined parameter consist ing 
of Linked File Name (same as Linked File GUID) and 
CIC.Common.BIMGUID. The data is generated 
automatically in the schedules. 
EOMS requires this parameter for mapping the data 
to the BIM model geometry. 
Text 
 
13.4. Update the equipment list and SDI template 
The content of the equipment list can be replaced entirely by the Excel worksheets exported. The 
updated equipment list will contain the latest asset information and data from BIM model, and ready 
for transfer to SDI template. Since there is format requirement from SDI template for importing the asset 
information and data into EOMS, the format should be verified before it is transferred to SDI template. 
 
Guidance Note: Appointing Parties may consider to arrange the maintenance and upkeep of the AIM and 
asset information by their operation team if the staffs were capable and available to do so, under a well-
established workflow and mechanism. Alternatively, Appointing Par ties may consider to outsource the 
works to an external vendor or professional, in project-basis or term-contract, etc., or embed the works 
into the consultancy agreement or construction contract when a project or property is to be renewed , 
renovated, undergo alterations and additions works, depending on scope, scale and size of the projects, 
complexity, timeframe, etc.
