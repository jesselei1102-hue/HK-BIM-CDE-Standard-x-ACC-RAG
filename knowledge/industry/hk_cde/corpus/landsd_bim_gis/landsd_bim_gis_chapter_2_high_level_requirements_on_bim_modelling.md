---
source_file: output/HK Standard/BD_LandsD/LandsD_LandsD_BIM_and_GIS_Data_Integration_Guidelines_Jun2023.pdf
doc_id: landsd_bim_gis
section_id: landsd_bim_gis_chapter_2_high_level_requirements_on_bim_modelling
title: Chapter 2 — High Level Requirements on BIM Modelling
page_start: 7
page_end: 10
authority: LandsD BIM-GIS Guidelines Jun 2023 §Chapter 2 — High Level Requirements
  on BIM Modelling
priority: high
language: en
source_url: hk_cde://landsd_bim_gis/landsd_bim_gis_chapter_2_high_level_requirements_on_bim_modelling
---

# Chapter 2 — High Level Requirements on BIM Modelling

<!-- page 7 -->
______________________________________________________________________________  
BIM and GIS Data Integration Guidelines (June 2023 Edition)                              7 
CHAPTER 2  HIGH LEVEL REQUIREMENTS ON BIM MODELLING 
2.1 This chapter describes the high level requirements on BIM modelling to 
facilitate the conversion process of data from BIM to GIS platform. 
Modelling Requirement #1: Mapping of Information Elements from BIM to GIS 
Environment 
2.2 To ensure the interoperability for effective exchange of d ata across the BIM 
domain and GIS domain, it is of paramount significance to define the mapping 
of the information elements from BIM to GIS environment  prior to the data 
preparation stage .  By defining such mapping routines  (Figure 1  refers), 
automation of the conversion process of BIM objects to the corresponding 
GIS features could be achieved.  
 
Figure 1 An illustration of mapping of information elements from BIM to GIS 
 
2.3 The table below gives an example on the mapping of curtain wall and basic 
wall objects in BIM to the corresponding feature types in GIS.  
BIM Domain GIS Domain 
Model Categories Feature Class InteriorUsage 
Wall Curtain Wall Bldg_Envelope Window 
Basic Wall Exterior Wall

<!-- page 8 -->
______________________________________________________________________________  
BIM and GIS Data Integration Guidelines (June 2023 Edition)                              8 
Modelling Requirement #2: Assignment of Unique Identifier for BIM Objects 
2.4 For ease of quality checking subsequent to the data conversion from BIM to 
GIS, it is a good practice to export the unique identifier of the elements in the 
BIM model (e.g. element ID in Revit) during the conversion of BIM elements 
to GIS.  It is not uncommon to encounter error or unexpected results during 
the data conversion process s ince the data stored on BIM platform and GIS 
platform are of different data structure s.  The unique identifier , if exported 
from BIM elements  to GIS feature s, could then be used for tracking the 
original element in the BIM model to facilitate further investigation and to 
ensure data completeness after the data conv ersion process .  Figure 2 
below demonstrates the unique identifier of a BIM object being exported and 
stored as one of the attributes in the converted GIS data. 
After conversion 
 
Figure 2 An illustration of assigning the unique identifier for BIM object

<!-- page 9 -->
______________________________________________________________________________  
BIM and GIS Data Integration Guidelines (June 2023 Edition)                              9 
Modelling Requirement #3: Delineation of Units 
2.5 According to the INSPIRE Data Specification on Buildings – Technical 
Guidelines D2.8.III.2_v3.0 (2013), a “Unit” is a subdivision of Building with its 
own lockable access from the outside or from a common are a (i.e. not from 
another Building Unit), which is atomic, functionally independent, and may be 
separately sold, rented out, inherited, etc.   To facilitate spatial analysis and 
indoor routing applications in the GIS environment after conversion, BIM 
modelers are recommended to delineate the extent of an enclosed space as 
“Room” or “Space” element (or equivalent) on BIM platform.  
 
Figure 3 An illustration of delineating the extent of Unit elements on BIM platform 
 
Modelling Requirement #4: Definition of Subtype for Classification the Use of 
a Space 
2.6 To reduce duplication of effort in classifying and verifying the use of building 
units in GIS platform after data conversion from BIM, BIM modelers are 
recommended to indicate the use of a space in the name property of the 
“Room” element in a standardized manner in the BIM model.  
2.7 The classification of the use of space could refer to the list of UnitSubtype as 
defined in the 3D Indoor Map Data Dictionary of LandsD as published on the 
Hong Kong GeoData Store .  If BIM modelers follow another classification 
system to define the use of a space, a mapping table between the adopted 
classification system and the classification system in 3D Indoor Map Data 
Dictionary could be prepared for seamless conversion.

<!-- page 10 -->
______________________________________________________________________________  
BIM and GIS Data Integration Guidelines (June 2023 Edition)                              10 
CHAPTER 3  HIGH LEVEL REQUIREMENTS ON CONVERSION  
OF DATA FROM BIM TO GIS 
3.1 This section describes the high level conversion requirement for seamless 
conversion of data from BIM to GIS 
Conversion Requirement #1: Level of Details in GIS Environment 
3.2 BIM models store rich geometric and semantic information of a building 
throughout the building life cycle.  Depending on the intended purpose of 
integration, partial objects in a BIM model could be selected and converted to 
the GIS platform to avoid excessive amount of details in the output GIS data. 
The unnecessary details increase demand for processing power and storage 
space, and might hinder data sharing.  It is therefore important to define the 
required features on the GIS platform and the expected level of details.  For 
instance, the inclined BIM objects such as escalators, balustrades and railings 
could be generalized in terms of base levels, feature height of floors and walls.  
Figure 4 below gives an example showing the covered walkway represented 
in 3D objects on BIM platform was filtered out in the converted GIS data.  
 
After conversion  
 
Figure 4 An illustration of filtering excessive amount of details from BIM model 
from the converted GIS output data
