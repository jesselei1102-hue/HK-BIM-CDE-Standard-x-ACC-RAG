---
source_file: output/HK Standard/CIC BIM Standards General 2024/CIC BIM Standards General
  (Version 2024).pdf
doc_id: cicbims_2024
section_id: cicbims_2024_appendix_b_examples_of_model_zones_and_levels_definitions
title: Appendix B Examples of Model Zones and Levels Definitions
page_start: 207
page_end: 213
authority: CICBIMS 2024 §Appendix
priority: normal
language: en
source_url: hk_cde://cicbims_2024/cicbims_2024_appendix_b_examples_of_model_zones_and_levels_definitions
---

# Appendix B Examples of Model Zones and Levels Definitions

Appendix B Examples of Example of LOD-I 
 
207 
 
Appendix B Examples of Model Zones 
and Levels Definitions 
 
Example 1 Tall Building  Example 
 
Single  Tower Example - Simple  
For a simple  tower project,  it is recommended to model discipline  element s in one model 
file to keep the relationship  and continuity  of the elements.  
 
 
 
 
 
The file naming for the model files should  be as follows :- 
Project 
Code 
- Originator - Volume - Location - Discipline - Type 
BIMS2020 - CIC - XX - ZZ - AR - M3 
BIMS2020 - CIC - XX - ZZ - ST - M3 
BIMS2020 - CIC - XX - ZZ - FS - M3

Appendix B Examples of Model Zones & Levels Definitions 
 
 
208 
 
Single  Tower Example – Typical / Complex 
For tall buildings,  the project  may be divided  into basement,  podium  and tower models.  In 
this example,  a new residential  tower will be constructed adjacent  to existing  development.  
The models  should  be separated as follows ; 
BAS = Basement  POD = Podium  
TYP = Typical Levels  RF = Roof Level 
 
 
 
The file naming for the model files should  be as follows : - 
 
Project 
Code 
- Originator - Volume - Location - Discipline - Type 
BIMS2020 - CIC - POD - XX - AR - M3 
BIMS2020 - CIC - TYP - XX - AR - M3 
BIMS2020 - CIC - RF - XX - AR - M3

Appendix B Examples of Example of LOD-I 
 
209 
 
Multiple Towers and multiple  Zones Example – Typical / Complex 
For a large scale of the project  site, it would be better  to classify  the blocks  / buildings  into 
zones.  
 
Considering  the buildings  are divided  into zones,  basement,  podium  and tower, the file 
naming  for the model files should be as follows :- 
 
 
 
 
Project 
Code 
- Origin
-ator 
- Volume - Location - Discipline _ Sub-
discipline 
 Type 
BIMS2020 - CIC - T1 - TYP - AR   - M3 
BIMS2020 - CIC - T2 - TYP - AR   - M3 
BIMS2020 - CIC - T3 - TYP - AR   - M3

Appendix B Examples of Model Zones & Levels Definitions 
 
 
210 
 
Example 2 MTR West Kowloon  Terminus 
 
Large plan project  with multiple contracts 
The models  for the project  shall be created by sub-dividing the project  on plan into three 
zones representing the 811B, 810A and 810B contracts.  These zones should  be further  
sub-divided  to control  the Revit file sizes.  The files are identified by the project  gridlines.  
 
The file naming for the model files should  be as follows :- 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Project 
Code 
- Originator - Volume - Location - Discipline - Type 
811B - MTR - WKT - G0111 - AR - M3 
811B - MTR - WKT - G0111 - ST - M3 
810A - MTR - WKT - G1118 - AR - M3 
810A - MTR - WKT - G1831 - AR - M3 
810A - MTR - WKT - G3141 - AR - M3 
810B - MTR - WKT - G4149 - AR - M3 
811B - MTR - WKT - PTI - AS - M3

Appendix B Examples of Example of LOD-I 
 
211 
 
Example 3 Hong Kong International  Airport  
 
Large plan project  with different  phases  of construction  
Due to the scale,  complexity  and planned  construction  phasing,  the BIM Manager  should  
separate the models  by zone and by discipline,  by sub-dividing  the Midfield  Concourse on 
plan into 11 separate Location.  
 
The zones and the zone file name codes are defined as:- 
 
Figure 55 Information Model Zones 
Location     Sub-Location ( Levels ) 
CNN - Concourse North   Foundation  Level to L7 Mezzanine  (see  section  below)  
CND - Concourse Central  Node  L0 APM track to L7 Mezzanine (see  section below)  
CNS - Concourse South   Foundation  Level to L7 Mezzanine  (see  section  below)  
LBN – Fixed Link Bridge  North  Foundation  Level to L7 Mezzanine  
LBS – Fixed Link Bridge  South  Foundation  Level to L7 Mezzanine  
RFN - Roof Framing North   L6 Departure to L8 Roof (see  section  below)  
RFD - Roof Framing Central  Node  L0 APM track to L7 Mezzanine (see  section below)  
RFS - Roof Framing South   L6 Departure to L8 Roof (see  section  below)  
APM - APM Tunnel     L0 APM track to Foundation Level 
SRR - South Runway Road   Foundation  Level to L5 Arrival 
CVL - Civil Airfield  Services     
 
 
 
 
 
 
 
 
 
 
 
 
 
Figure 56 Information Model Zone Cross Section

Appendix B Examples of Model Zones & Levels Definitions 
 
 
212 
 
The match lines between the Concourse Node and the North/South Concourse are shown 
along the structural  movement  joints  as below: - 
 
 
Figure 57 Information Model Zone Break Line at North - Concourse 
 
The match lines between the Roof Node and the North/South Roof follow  the structural  
steel roof framing,  as shown below, and match with the concourse movement  joints.  
 
 
 
 
 
 
Figure 58 Information Model Zone Break Line at North - Roof

Appendix B Examples of Example of LOD-I 
 
213 
 
The match lines between the Concourse Node and APM Tunnel is as shown below: - 
 
 
Figure 59 Information Model Zone Break Line at Node / APM
