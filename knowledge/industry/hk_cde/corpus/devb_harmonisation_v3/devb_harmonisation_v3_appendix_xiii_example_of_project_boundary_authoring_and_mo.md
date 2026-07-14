---
source_file: output/HK Standard/DEVB BIM Harmonisation Guidelines for WDs (v3_0) with
  All Appendices.pdf
doc_id: devb_harmonisation_v3
section_id: devb_harmonisation_v3_appendix_xiii_example_of_project_boundary_authoring_and_mo
title: Appendix XIII-Example of Project Boundary Authoring and Model File List (v3.0)
page_start: 152
page_end: 155
authority: DEVB BIM Harmonisation v3.0 §Appendix
priority: normal
language: en
source_url: hk_cde://devb_harmonisation_v3/devb_harmonisation_v3_appendix_xiii_example_of_project_boundary_authoring_and_mo
---

# Appendix XIII-Example of Project Boundary Authoring and Model File List (v3.0)

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX XIII 
 
 
Appendix XIII – Example of Project Boundary Authoring and Model File 
List 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Remarks: Please read this Appendix in conjunction with Appendix XIV- Guidelines for 
Submission of Design and As-built BIM Models to LandsD. 
  
P152

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX XIII 
 
 
 
TABLE OF CONTENTS 
1. Project Boundary ............................................................................................................................ XIII-1 
2. Model File List ............................................................................................................................... XIII-2 
 
  
P153

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX XIII 
 
 
XIII-1 
 
1. Project Boundary 
1.1 The project boundary should be set up for BIM model per project. The boundary should 
be one or multiple closed outer lines of all model elements.  
 
Table 1-1 Examples of Project Boundary 
  
Not closed, overlapping Close d 
 
Multiple closed areas Multiple closed areas with intersection 
 
 
1.2 The project boundary in 2D should be provided a nd stored in a separa ted file in one of 
the following formats: DWG, Shapefile, or DGN format for each project. The file shall 
be named Project boundary.dwg, Project boundary.shp , or Project boundary.dgn , as 
appropriate, and be prepared in accordance with the following requirements:  
a) Supported file format versions:  
- DWG: 2018 or later  
- DGN: V8 
- Shapefile: Version 1.0. 
b) The setting of coordinate system should be HK1980 Grid and in meter.  
c) Any object which is not related to the boundary should be hidden. 
d) Reference blocks should be avoided. 
 
P154

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX XIII 
 
 
XIII-2 
 
1.3 For Autodesk Revit model, a DWG file should be exported from the Revit project file to 
store the project boundary separately. The e xported layer should be named as Project 
Boundary and it should be modelled as Property Line.  
 
Figure 1-1 Call Out Property Line in Revit 
 
 
1.4 For Civil 3D, the DWG file should be based on  project specific Civil 3D template with 
project information. The layer should be named as Project Boundary and used continuous 
line as the line type. 
Figure 1-2 Layer Setting for Project Boundary in DWG 
 
 
1.5 WDs should follow Appendix XIV - Guidelines for Submission of Design and As-built 
BIM Models to LandsD to submit the project boundary to respective folder for effective 
data management on the GBDR. 
 
2. Model File List 
2.1 WDs should input the following in formation in model file list template and submit it to 
respective folder according to Appendix XIV - Guidelines for Submission of Design and 
As-built BIM Models to LandsD. An .xlsx file describes model file list can be 
downloaded from DEVB’s Website: 
https://www.devb.gov.hk/en/publications_and_press_releases/publications/devb-
harmonisation-guideline/index.html 
 
No.  Item 
1 Serial Numbe r 
2 Model File Name 
3 Descriptio n 
4 Sta ge – Detail Design (D) / As-built (AB) 
5 File Format 
6 Software Versio n 
 
P155
