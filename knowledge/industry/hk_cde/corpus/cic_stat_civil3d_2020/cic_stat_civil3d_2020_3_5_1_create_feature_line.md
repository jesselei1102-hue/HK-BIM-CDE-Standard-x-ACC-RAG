---
source_file: output/HK Standard/CIC BIM Standard/CIC BIM Standards for Preparation
  of Statutory Plan Submissions Dec2020/Appendix 2 CIC BIM User Guide for Preparation
  of Statutory Plan Submissions Civil 3D Dec2020.pdf
doc_id: cic_stat_civil3d_2020
section_id: cic_stat_civil3d_2020_3_5_1_create_feature_line
title: 3.5.1 Create Feature Line
page_start: 14
page_end: 15
authority: CIC Statutory Civil 3D Guide 2020 §3.5.1
authority_type: software_guide
normative_weight: operational
discipline: statutory_submission
lifecycle_stage: statutory
publication_year: 2020
software: Civil 3D
priority: normal
language: en
source_url: hk_cde://cic_stat_civil3d_2020/cic_stat_civil3d_2020_3_5_1_create_feature_line
---

# 3.5.1 Create Feature Line

8 
 
3.4 Create Site Boundary 
One way of representing Site Boundary is to use Parcel object which is an enclosed 
boundary. 
Draw a polyline in model space, then press the button “Ribbon > Home > Create Design > 
Parcel > Create Parcel from Objects” and select the polyline. Press enter after selection. 
Specify “Site” and “Parcel Style” then press Okay. The representation of boundary can be 
customized via Parcel Style as shown below 
 
3.5 Creating Feature Lines and Grading 
Feature line is one basic building block when working with Grading in Civil 3D. All gradings 
are essentially started from feature lines. The process of creating Grading will create 
additional feature lines from the origin feature lines. 
3.5.1 Create Feature Line 
One way of creating new feature line is to draw a polyline (representing the platform 
boundary) in model space, then press the button “Ribbon > Home > Create Design > Feature 
Lines > Create Feature lines from Objects” and select the polyline. Press enter after selection. 
Elevations of feature line can also be edited by selecting a feature line and click on Elevation 
Editor button on Feature Line contextual ribbon. 
3.5.2 Create Grading 
The steps below show how to create Grading 
1. Open Grading Creation Tools by clicking on Home>Grading>Grading Creation Tools  
button. 
 
2. Set a Grading Group which will contain all gradings by clicking on  button. A Grading 
Group is used to organize gradings into named collections for surface creation and 
volume computations. 
3. Set a target Surface by clicking on  button. This will be used as the base surface 
when selecting Grade to Surface criteria to create Grading.

9 
 
4. Select a suitable grading criterion to create Grading by selecting from the dropdown box 
. There are four methods to create Grading: Grade to 
Distance, Grade to Elevation, Grade to Relative Elevation and Grade to Surface. For 
example, when selecting Grade to Surface, the Grading (slope) will be created from the 
original feature line to the selected surface by a given slope such as 3.00:1. The image 
below demonstrates the newly created slope when using Grade to Surface criterion. 
 
 
5. Create Grading by clicking on  button. Follow the instructions on the command line 
to create Grading from the selected feature line. It should be noted that when asking for 
Cut or Fill format, you can select the Slope and enter 2:1 for 2:1 slope.  
 
 
Click on the surface of the grading and select the Tin surface 
 
Then, view it in Object Viewer and you will see that the platform is not filled 
Platform 
Newly created slope 
target to the surface 
Newly created slope 
target to the surface 
Grade to Surface: 
Feature Line 
 Feature Line
