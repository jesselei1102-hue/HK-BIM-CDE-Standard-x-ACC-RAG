---
source_file: output/HK Standard/BD_LandsD/LandsD_LandsD_BIM_and_GIS_Data_Integration_Guidelines_Jun2023.pdf
doc_id: landsd_bim_gis
section_id: landsd_bim_gis_chapter_3_high_level_requirements_on_data_conversion
title: Chapter 3 — High Level Requirements on Data Conversion
page_start: 11
page_end: 12
authority: LandsD BIM-GIS Guidelines Jun 2023 §Chapter 3 — High Level Requirements
  on Data Conversion
priority: high
language: en
source_url: hk_cde://landsd_bim_gis/landsd_bim_gis_chapter_3_high_level_requirements_on_data_conversion
---

# Chapter 3 — High Level Requirements on Data Conversion

<!-- page 11 -->
______________________________________________________________________________  
BIM and GIS Data Integration Guidelines (June 2023 Edition)                              11 
Conversion Requirement #2: Design of GIS Data Schema 
3.3 For seamless integration with other spatial related information from the 
Government departments or private sector, when converting data from BIM to 
GIS, it is suggested to adopt the following data model and structure , which 
consists of 4 semantic components including building footprint, shell, floor and 
unit. Depending on  the intended purpose of the  applications, additional 
feature attributes could be integrated, such as  Property Reference Number 
(PRN) and Assessment Number. 
3.4 For mapping indoor features within a building, major feature classes of the 
exported GIS data are suggested as follows:- 
 
  
Feature Class Name  Data Type  Details  
3D Floor  Polygon  
Represents the location and the 
outermost physical extent of the 
floor of the building 
3D Units  Polygon 
Represents the location and 
physical extent of an enclosed 
space within Floor Polygon 
Place of Interest  
Point / 
Polygon 
Represents a location that a user is 
interested in on a map 
3D Gate Polyline 
Represent the position and 
approximate physical extent o f the 
entrance and exit of the 
independent space enclosed by 
the wall and the fence. 
3D Window  Polyline 
Represent the position and 
approximate physical extent of the 
window of the independent space 
enclosed by the wall and the fence

<!-- page 12 -->
______________________________________________________________________________  
BIM and GIS Data Integration Guidelines (June 2023 Edition)                              12 
Conversion Requirement #3: Filling of Interstitial Spaces between Units 
3.5 Spaces in BIM environment may be enclosed by “Wall” objects with thickness.  
When the extent of space is delineated by “Room” object based on the interior 
lines of the wall, interstiti al spaces between Unit polygons are created after 
the “Room” objects are converted into GIS platform.  It is a good practice to 
fill the interstitial spaces by expanding the extent of the Unit polygons using 
GIS software. 
 
 
Figure 5 An illustration showing a group of building units converted from the BIM model 
before (above) and after (below) filling the interstitial spaces using GIS software
