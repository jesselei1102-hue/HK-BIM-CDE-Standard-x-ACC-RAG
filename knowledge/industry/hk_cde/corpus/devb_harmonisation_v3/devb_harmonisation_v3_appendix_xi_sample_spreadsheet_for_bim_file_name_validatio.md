---
source_file: output/HK Standard/DEVB BIM Harmonisation Guidelines for WDs (v3_0) with
  All Appendices.pdf
doc_id: devb_harmonisation_v3
section_id: devb_harmonisation_v3_appendix_xi_sample_spreadsheet_for_bim_file_name_validatio
title: Appendix XI - Sample Spreadsheet for BIM File Name Validation (v3.0)
page_start: 142
page_end: 148
authority: DEVB BIM Harmonisation v3.0 §Appendix
priority: normal
language: en
source_url: hk_cde://devb_harmonisation_v3/devb_harmonisation_v3_appendix_xi_sample_spreadsheet_for_bim_file_name_validatio
---

# Appendix XI - Sample Spreadsheet for BIM File Name Validation (v3.0)

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX XI 
 
 
 
 – A Sample Spreadsheet for BIM File Name Validation 
P142

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX XI 
 
 
 
Table of Content 
 
1. Introduction ....................................................................................................................................... XI-1 
2. BIM File Name Validation Process Using Spreadsheet .................................................................... XI-1 
 
 
 
List of Figures 
Figure App XI-1 - The “Project Specified Code” Worksheet ............................................................................ XI-2 
Figure App XI-2 –The Worksheets for Each Field ............................................................................................ XI-3 
Figure App XI-3 - The “Model Naming” Worksheets ...................................................................................... XI-3 
Figure App XI-4 – Example of Drop-Down List for Selecting Codes .............................................................. XI-4 
Figure App XI-5 - Example of Auto-Generated Information for Model Files .................................................. XI-4 
Figure App XI-6 - Hidden Columns on the “Model Naming” Worksheet ........................................................ XI-5 
Figure App XI-7 – Example of Cells with Grey Font Colour............................................................................ XI-5 
 
 
 
P143

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX XI 
 
XI-1 
 
1. Introduction 
1.1. BIM file name validation process can be embedded in BIM CDCP, GBDR or 
spreadsheet. 
1.2. This Appendix provides an example of BIM file name validation process using the 
spreadsheet approach. This process is not required if the BIM CDCP has validation 
capabilities. 
1.3. This Appendix is composed of the following: 
1.3.1. A spreadsheet file containing worksheets fo r code management and BIM model name 
generation; and 
1.3.2. The step-by-step instructions in the section below on how to utilise the spreadsheet to 
facilitate the data validation process. 
 
2. BIM File Name Validation Process Using Spreadsheet 
2.1. In this example, a data spreadsheet has been created based on the project of Kwu Tung 
North (KTN) and Fanling North (FLN) New Development Areas (NDA), Phase 1. 
2.2. To ensure that the data going through conversion engine into GBDR to be shared with 
other parties have consistent naming (information container ID), a validation list is 
formed based on two types of codes: 
2.2.1. Common Codes in accordance with Appendix X – Common Codes for Naming; and 
2.2.2. Project-specific Codes which would be different for different projects. An example of 
project-specific codes is provided in Appendix IX – Sample Project Specific Codes for 
Naming. 
 
P144

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX XI 
 
XI-2 
 
2.3. To add codes to the list: 
2.3.1. Go to the "Project Specific Code" work sheet (orange coloured  tab). The “Common 
Code” worksheet should not be modified without consensus between all WDs. 
 
Figure App XI-1 - The “Project Specified Code” Worksheet 
 
 
 
2.3.2. Find the corresponding field and add the information to the bottom of the list. The field 
length and format as specified in the Guidelines should be followed. 
 
 
 
 
 
 
 
 
 
 
 
 
 
2.3.3. The value of the field will be automa tically updated in th e corresponding field 
worksheet (green coloured tabs). 
 
P145

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX XI 
 
XI-3 
 
Figure App XI-2 –The Worksheets for Each Field 
 
 
2.3.4. The updated codes can now be selected from the “Model Naming” worksheet (blue 
coloured tabs). 
 
Figure App XI-3 - The “Model Naming” Worksheets 
 
 
2.4. To automatically generate a list of model names for the model registers: 
2.4.1. Go to the “Model Naming” worksheet. 
2.4.2. Use the drop-down list of each field (from Column A to Column K) to select the correct 
code. Required fields must not be omitted. The cells with project-specific code selected 
P146

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX XI 
 
XI-4 
 
would be automatically highlighted with or ange colour while that with common code 
selected would be automatically highlighted with blue colour. 
 
Figure App XI-4 – Example of Drop-Down List for Selecting Codes 
 
 
2.4.3. After selecting the codes for all required fields, the model file name, length of file name 
and description (from Column W to Column Y) would be generated automatically. 
 
Figure App XI-5 - Example of Auto-Generated Information for Model Files 
 
 
2.5. The limitations of the sample spreadsheet for BIM file name validation should be noted. 
To keep this spreadsheet’s file size mana geable, the numbers of rows for the “Model 
Naming” worksheet and the worksheets for each field are capped at 10,000.  
 
P147

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX XI 
 
XI-5 
 
2.6. On the “Model Naming” worksheet, the cells  from Column L to Column V are input 
with formulas for background control of Data . Since users don't need to input or view 
these cells, they are hidden for better user experience. 
 
Figure App XI-6 - Hidden Columns on the “Model Naming” Worksheet 
 
 
 
2.7. On the “Field 4.1” and “Field 5.2” worksheets, the cells with grey font colour are input 
with formulas for generating the drop-down lists. They should not be modified, cleared 
or deleted. 
 
Figure App XI-7 – Example of Cells with Grey Font Colour 
 
P148
