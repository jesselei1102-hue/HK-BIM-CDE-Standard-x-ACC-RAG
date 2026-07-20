---
source_file: output/HK Standard/CIC BIM Standard/CIC Production of BIM Object Guide
  - General Requirements (2021).pdf
doc_id: cic_object_guide_2021
section_id: cic_object_guide_2021_4_4_guidelines_for_assigning_omniclass
title: 4.4 Guidelines for assigning OmniClass®
page_start: 10
page_end: 10
authority: CIC BIM Object Guide 2021 §4.4
authority_type: standard
normative_weight: recommended
discipline: bim_objects
lifecycle_stage: project
publication_year: 2021
software: null
priority: high
language: en
source_url: hk_cde://cic_object_guide_2021/cic_object_guide_2021_4_4_guidelines_for_assigning_omniclass
---

# 4.4 Guidelines for assigning OmniClass®

CIC PRODUCTION OF BIM OBJECT GUIDE 
7 
2. The BIM object m ay also be assigned with a category / classification / catalog  based on another classification 
system, such as The OmniClass® Construction Classification System, if that is available on the BIM platform  used 
for a project, or can be stated as an additional property. 
3. To facilitate the exchange of BIM objects and related information, the BIM object shall be assigned with appropriate 
Industrial Foundation Classes (IFC) parameters. 
4. IFC classes are not recommend to be added in the user defined attribute as this will interrupt the mapping details to 
IFC conversion. 
5. About Classification (classification system), the OmniClass® Table 23 is recommended (and note that version 2012 
should be used, instead of version 2006) if there are no other specific requirements from the project Appointing Party 
/ Client. For Revit users, they need to update the OmniClass® version in Revit from 2006 to 2012, procedure can be 
found from this link:  
https://help.autodesk.com/view/RVT/2021/ENU/?guid=GUID-BA0B2713-ADA0-4E51-A7CD-85D85511F3ED 
6. BIM objects from generic type or category should be minimised, due to the conversion to open format (.IFC) may 
potentially affect the LOD-G representation. 
 
4.4 Guidelines for assigning OmniClass®  
This section defines the guidelines of class ifying construction results, construction resources and construction processes 
according to an international standard, OmniClass ®. It enables an object -oriented classification for the whole life cycle of a 
structure. OmniClass® version 2012 consists of 15 hierarchical tables, each of which represents a different facet of construction 
information. Details of each table can refer to this link: https://www.csiresources.org/standards/omniclass/standards-
omniclass-about 
To facilitate logical BIM object organisation and searching, BIM objects could be organised in a folder structure as the first level 
of OmniClass® Version 2012. The format of OmniClass® code should align with the official numbering format of Construction 
Specifications Institute as “##-## ## ##”, where # is numeric. The t able below shows an example for the corresponding Level 
1 title with OmniClass® numbers as folder names.  
If a specific OmniClass® designation cannot be identified, a similar designation should be used to establish a searchable object 
database for the ease of information identification in the future. 
 
Folder Structure of BIM Object Library 
OmniClass® 
Table 23 Products 
Folder Name Level 1 Title 
23-11 Site Products 
23-13 Structural and Exterior Enclosure Products 
23-15 Interior and Finish Products 
23-17 Openings, Passages, and Protection Products 
23-19 Specialty Products 
23-21 Furnishings, Fixtures and Equipment Products 
23-23 Conveying Systems and Material Handling Products 
23-25 Medical and Laboratory Equipment 
23-27 General Facility Services Products 
23-29 Facility and Occupant Protection Products 
23-31 Plumbing Specific Products and Equipment 
23-33 HVAC Specific Products and Equipment 
23-35 Electrical and Lighting Specific Products and Equipment 
23-37 Information and Communication Specific Products and Equipment 
23-39 Utility and Transportation Products 
 
In BIM authoring software, there are different methods for defining and assigning OmniClass®, by using the default parameters, 
if available, or by creating a common parameter, if relevant default parameter is not available.
