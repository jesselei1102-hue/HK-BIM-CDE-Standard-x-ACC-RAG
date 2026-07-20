---
source_file: output/HK Standard/BD_LandsD/LandsD_LandsD_BIM_and_GIS_Data_Integration_Guidelines_Jun2023.pdf
doc_id: landsd_bim_gis
section_id: landsd_bim_gis_chapter_1_introduction
title: Chapter 1 — Introduction
page_start: 4
page_end: 6
authority: LandsD BIM-GIS Guidelines Jun 2023 §Chapter 1 — Introduction
authority_type: statutory
normative_weight: mandatory
discipline: gis
lifecycle_stage: statutory
priority: high
language: en
source_url: hk_cde://landsd_bim_gis/landsd_bim_gis_chapter_1_introduction
---

# Chapter 1 — Introduction

<!-- page 4 -->
______________________________________________________________________________  
BIM and GIS Data Integration Guidelines (June 2023 Edition)                              4 
CHAPTER 1  INTRODUCTION 
Background 
1.1 The Smart City Blueprint for Hong Kong released in December 2017 sets 
out the overall framework and strategy for developing Hong Kong into a 
spatially enabled smart city including the adoption of Building Information 
Modelling (BIM) and the development of Common Spatial Data 
Infrastructure (CSDI) and 3D Digital Map. 
1.2 The 3D Digital Map, which is one of the building blocks of CSDI, is to 
facilitate opening up and sharing of Government geospatial data.   To meet 
the increasing needs of 3D Digital Map applications and to enhance better 
understanding of multi -level spaces of a modern city like Hong Kong, the 
Government aims to develop the high-quality 3D Digital Map by phases and 
strives to cover the whole territory by end 2023. 
1.3 The Lands Department (LandsD) is now producing a set of 3D digital maps 
covering the whole territory, which includes the full-fledged 3D visualisation 
map, the 3D indoor map covering the accessible interior of buildings and 
structures for 1 250 buildings and the 3D pedestrian network data over the 
territory. 
1.4 BIM data, which contains rich content of 3D boundary of floors, units, and 
common areas, can serve as an abundant supply of data required for future 
production and updating of 3D indoor map.  
1.5 In this respect, LandsD ha s conducted a  study on the BIM to GIS data 
conversion and integration processes with the project data contributed by 
the Urban Renewal Authority (URA) under the project of “Development of 3-
Dimensional Intelligent Map (3D iMap) ”.  Based on the data conversion 
results a nd the technical issues encountered during the data conversion 
process shared by URA, the study aims to develop a set of high level 
requirements on BIM modelling and conversion serving as best practices to 
help practitioners of the Architectural, Engineering, and Construction (AEC) 
Sector to achieve seamless data integration between BIM and GIS.

<!-- page 5 -->
______________________________________________________________________________  
BIM and GIS Data Integration Guidelines (June 2023 Edition)                              5 
Purpose and Scope 
1.6 The purpose of the BIM and GIS Data Integration Guidelines (hereinafter 
referred as this Guidelines) is to provide a reference guide with a set  of 
generic rules for the betterment of the conversion process of data from BIM 
to GIS platform. 
1.7 This Guidelines aim to set out general guidelines and recommend good 
practices, focusing on high level requirements on BIM modelling and data 
conversion, to fa cilitate interoperable geospatial data management through 
seamless data integration between BIM and GIS. 
Revision of this Guidelines 
1.8 This Guidelines is a living document for general reference by the practitioners 
of the Architectural, Engineering and Construction (AEC) sector and its 
recommendations are not intended to be mandatory.  This Guidelines will be 
updated regularly to take account of advances in technology and the changing 
needs of the AEC sector.  
Definitions 
1.9 The following is a list of definitions of the terms used in this Guidelines. 
3D Floors: Floor Polygons in vector format.  Each Floor Polygon represents 
the location and the outermost physical extent of the floor of the building. 
3D Gates: Gate models the position and approximate physical extent of the 
entrance and exit of the independent space enclosed by the wall and the 
fence.  Gate usually refers to the opening on the wall or the fence. 
3D Units: Unit Polygons in vector format.  Each Unit Polygon represents the 
location and physical extent of an enclosed space within Floor Polygon 
including all the structural details of the floor including but not limited to the 
building shape, elevators, escalators, entrances, doors, walls, stores, gates, 
hallways, balconies, entrance and exit of the floor.

<!-- page 6 -->
______________________________________________________________________________  
BIM and GIS Data Integration Guidelines (June 2023 Edition)                              6 
3D Windows: Window models the position and approximate physical extent 
of the window of the independent space enclosed by the wall and the fence. 
BIM Object: A combination of object geometry and product informat ion that 
represents the product’s physical characteristics in a digital environment. 
Coordinate System : A set of mathematical rules for specifying how 
coordinates are to be assigned to each point. 
Feature: Abstraction of real -world phenomena.  A feature ma y occur as a 
type or an instance. 
Feature Attribute: Characteristic of a feature.   A feature attribute has a 
name, a data type, and a value domain associated to it. 
Point: Topological 0-dimensional geometric primitive, representing a position. 
Line: Topological 1 -deminsional geometric primitive, representing a linear 
feature. 
Polygon: Topological 2 -deminsional geometric primitive, representing an 
area or a planar surface.
