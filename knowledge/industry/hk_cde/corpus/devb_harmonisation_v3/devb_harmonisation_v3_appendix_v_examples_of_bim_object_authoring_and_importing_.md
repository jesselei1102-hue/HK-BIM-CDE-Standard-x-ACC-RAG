---
source_file: output/HK Standard/DEVB BIM Harmonisation Guidelines for WDs (v3_0) with
  All Appendices.pdf
doc_id: devb_harmonisation_v3
section_id: devb_harmonisation_v3_appendix_v_examples_of_bim_object_authoring_and_importing_
title: Appendix V - Examples of BIM Object Authoring and Importing Civil 3D BIM Objects
  into BIM Models (v3.0)
page_start: 54
page_end: 85
authority: DEVB BIM Harmonisation v3.0 §Appendix
authority_type: standard
normative_weight: mandatory
discipline: general
lifecycle_stage: project
publication_year: 2023
software: null
priority: high
language: en
source_url: hk_cde://devb_harmonisation_v3/devb_harmonisation_v3_appendix_v_examples_of_bim_object_authoring_and_importing_
---

# Appendix V - Examples of BIM Object Authoring and Importing Civil 3D BIM Objects into BIM Models (v3.0)

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
 
 – Examples of BIM Object Authoring and Importing 
Civil 3D BIM Objects into BIM Models 
 
P54

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
TABLE OF CONTENTS 
1. Introduction ........................................................................................................................................ V-1 
2. Revit BIM Objects ............................................................................................................................. V-1 
2.1. Revit Family Templates for BIM Object ............................................................................................ V-1 
3. Civil 3D BIM Objects ........................................................................................................................ V-2 
3.1. Name of Civil 3D Tool for BIM Object ............................................................................................. V-2 
3.2. Use of Civil 3D Object Style for 2D Presentation .............................................................................. V-2 
3.3. Use of Civil 3D Object Style for 3D Presentation .............................................................................. V-4 
4. Insertion of Civil 3D BIM Objects into BIM Models ........................................................................ V-5 
4.1. Subassemblies .................................................................................................................................... V-5 
4.2. Pipes Catalog ...................................................................................................................................... V-7 
4.3. Pressure Pipes Catalog ....................................................................................................................... V-9 
 
 
 
List of Tables  
Table 2-1 Revit Family Template to be Used for the Types of BIM Objects ..................................................... V-1 
Table 3-1 Civil 3D Tools to be Used for the Types of BIM Objects .................................................................. V-2 
 
 
List of Figures 
Figure 3-1 Setting of Structure Style for 2D Symbol ......................................................................................... V-3 
Figure 3-2 Setting of Component Display .......................................................................................................... V-3 
Figure 3-3 Setting of Structure Style for 3D Presentation .................................................................................. V-4 
Figure 4-1 “Import Subassemblies” Panel .......................................................................................................... V-5 
Figure 4-2 Input Source File for “Import Subassemblies” ................................................................................. V-5 
Figure 4-3 "Tool Palettes" Panel ........................................................................................................................ V-6 
Figure 4-4 Files for "Pipes Catalog" ................................................................................................................... V-7 
Figure 4-5 Set "Pipe Network Catalog" .............................................................................................................. V-7 
Figure 4-6 Pipe Network Catalog Settings ......................................................................................................... V-8 
Figure 4-7 Edit Network Parts List ..................................................................................................................... V-8 
Figure 4-8 Properties of Part Size Creator .......................................................................................................... V-9 
Figure 4-9 Default Catalog ................................................................................................................................. V-9 
Figure 4-10 Each Folder stored with below Two Folders .................................................................................. V-9 
Figure 4-11 Default Names of the Drawings in the DWG Folder .................................................................... V-10 
Figure 4-12 Images in IMG Folder ................................................................................................................... V-10 
Figure 4-13 Panel of “Content Catalog Editor” ................................................................................................ V-25 
Figure 4-14 Configure General Information for Importing a Part .................................................................... V-25 
Figure 4-15 Configure Part Type Information .................................................................................................. V-26 
Figure 4-16 Configure Model Properties .......................................................................................................... V-27 
P55

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
Figure 4-17 Review and Update Connection Point Information ...................................................................... V-28 
Figure 4-18 Save the Content Catalog file ........................................................................................................ V-29 
P56

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-1 
1. Introduction 
BIM object authoring and insertion methods  into BIM models may vary between 
software. In this Appendix, Revit and Civ il 3D are used as examples to outline the 
creation methods. If software  other than the two softwa re is adopted, the methods 
for creating BIM object should be properly documented in the BEP. 
Irrespective of software used, built-in temp lates, functions and built-in attributes 
within the authoring software should be used as far as practicable. 
 
2. Revit BIM Objects 
2.1. Revit Family Templates for BIM Object 
Revit provides family templates for creating BIM object. The table below shows the 
Revit family templates that would be used for the types of revamped BIM object. 
Table 2-1 Revit Family Template to be Used for the Types of BIM Objects  
Item 
No. 
Type of BIM Object Revit Family Template to be 
Used 
1. Electrical switch, socket outlet, 
control box, sensor 
Electrical Fixture 
2. LV switch board, genset, motor Electrical Equipment 
3. Lighting, lamp Lighting Fixture 
4. Pump, air-conditioning Mechanical Equipment 
5. Manhole, gully, U-chan nel Plumbing Fixture 
6. Road sign, sign gantry, road 
furniture, noise barrier 
Site 
7. Pipe accessories such as valve, 
water meter, fire hydrant 
Pipe Accessories 
8. Louvre Window 
9. Silencer, damper Duct Accessories 
10. Diffuser Air Terminal 
11. Sign, symbol Detail Item 
 
  
P57

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-2 
3. Civil 3D BIM Objects 
3.1. Name of Civil 3D Tool for BIM Object 
Civil 3D provides tools for creating BIM object. The table below shows the tools 
that would be used for the types of BIM objects. 
Table 3-1 Civil 3D Tools to be Used for the Types of BIM Objects 
Item 
No. Type of BIM Object Civil 3D Tool to be Used 
1. Manhole, gully, chamber, pit, outlet, 
etc. 
Part Builder 
2. Gravity pipe and culvert Part Builder 
3. Pressure pipe, fitting, valve, pipe 
accessory, etc. 
Content Catalog Editor 
4. Channel, trench, pipe/culvert of 
irregular shape, etc. 
Subassembly Composer 
5. Carriage way, footway, cycleway 
and other pavements 
Subassembly Composer 
6. Kerb, edging, concrete backing, 
barrier, etc. 
Subassembly Composer 
3.2. Use of Civil 3D Object Style for 2D Presentation 
3.2.1. In Civil 3D, 2D symbols cannot be em bedded in BIM objects. To handle 2D 
presentation, Civil 3D Object  Style would be used for the types of Civil 3D BIM 
objects.  
3.2.2. Civil 3D Object Style includes general at tributes for handling 2D symbol for BIM 
object, object colour, visibility of object components, object fill patterns, etc. Below 
is an example of settings Object Style for a drainage manhole. 
a) 2D presentation of drainage manhole could be set under tabs of “Plan”, 
“Profile” and “Section”. 2D symbol could be defined in the “Structure” under 
“Plan” tab as illustrated in the figure below. 
 
P58

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-3 
Figure 3-1 Setting of Structure Style for 2D Symbol 
 
 
b) Layer, color, line type, line scale, line weight and visibility of object 
components could be set in “Component display” under “Display” tab as 
illustrated in the figure below: 
Figure 3-2 Setting of Component Display 
 
 
 
P59

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-4 
3.3. Use of Civil 3D Object Style for 3D Presentation 
3.3.1. In Civil 3D, Civil 3D Object Style would be  used for setting the 3D presentation of 
Civil 3D BIM objects. To pres ent the finalised 3D models, the visibility of finalised 
objects could be switched on. Reference data generated during modelling process could 
be switched off. Below is an example of switching on visibility for a drainage manhole. 
 
Figure 3-3 Setting of Structure Style for 3D Presentation 
 
 
 
  
P60

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-5 
4. Insertion of Civil 3D BIM Objects into BIM Models 
For the two types of Civil 3D BIM objects, subassemblies and pipes catalog, the steps 
for insertion of Civil 3D BIM objects in to BIM model using the import function are 
described in the sections below.  
4.1. Subassemblies 
4.1.1. A .pkt file is a subassembly file for cr eating assemblies and corridor in Civil 3D. 
Autodesk Subassembly Composer should be used for creating subassemblies. Except 
the layout of the subassemblies, the super elevation, target and component parameters 
can be set when creating a subassembly. All parameters can be exported to Civil 3D.  
4.1.2. In Civil 3D, “Import Subassemblies” button can be found in “Insert” tab to import 
the .pkt file. 
Figure 4-1 “Import Subassemblies” Panel 
 
 
4.1.3. Search the .pkt file which needs to be im ported via “Source File”. New tool palette 
can be created in “Tool Palette” to organise those subassemblies by project. 
.    
Figure 4-2 Input Source File for “Import Subassemblies”  
\ 
 
P61

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-6 
4.1.4. To utilise the subassemblies file, turn on the “Tool Palettes” after creating an 
assembly. Drag the subassemblies into assembly. Then create a corridor by using the 
same assembly. 
Figure 4-3 "Tool Palettes" Panel 
 
 
 
  
P62

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-7 
4.2. Pipes Catalog 
4.2.1. “Pipes Catalog” is stored in a folder which contains all required structures and pipes. 
The required structures and pipes should be created by Part Builder, a built-in creator 
in Civil 3D that generates five types of file (.bak, .bmp, .xml, .dwg, .xml.bak) for one 
component. The component with all structure and pipes should be saved at the folder 
path below or (similar): 
 
Figure 4-4 Files for "Pipes Catalog" 
C:\ProgramData\Autodesk\C3D 20XX\enu\Pipes Catalog 
 
 
4.2.2. To importing pipes catalog into Civil 3D: 
a) Move the customized pipe/structure folder into “Pipes Catalog” or into “Metric 
Pipe/Structure Catalog”. The five file types should be moved into the same 
folder. 
 
b) Set the “Pipe Network Catalog” to the folder which stored the five file types. 
 
Figure 4-5 Set "Pipe Network Catalog" 
 
 
 
 
 
 
 
 
 
P63

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-8 
c) Regenerate the pipes cata log by using the command 
“PARTCATALOGREGEN”. 
Figure 4-6 Pipe Network Catalog Settings 
 
 
d) The structures and pipes should be adde d to Pipe Network after importing the 
pipe catalog using the following commands:  
“Edit Network” > “Select Parts List” > “Add part family” in both Pipe and 
Structures tab. Right click the part just added into the list >“Add part size” > 
tick “Add all sizes”. 
Figure 4-7 Edit Network Parts List 
 
 
 
 
 
 
 
 
 
P64

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-9 
e) The properties of Part Size Creator are as follows: 
Figure 4-8 Properties of Part Size Creator 
 
 
4.3. Pressure Pipes Catalog 
4.3.1. Different from pipes catalog,  pressure pipes catalog should be created using .sqlite 
format with different creation procedures.  
4.3.2. The “Pressure Pipes Catalog” is stor ed in “C:\ProgramData\Autodesk\C3D 
2020\enu\Pressure Pipes Catalog\Metric”. 
The default catalog includes: 
Figure 4-9 Default Catalog 
 
 
4.3.3. Inside a folder, the parts stored in two folders: DWG and IMG. 
Figure 4-10 Each Folder stored with below Two Folders 
 
 
 
 
P65

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-10 
4.3.4. In DWG folder, the .dwg drawings are typically not identifiable by default names. 
 
Figure 4-11 Default Names of the Drawings in the DWG Folder 
 
 
4.3.5. The IMG folder contains images (in .png formats) whose names match the 
corresponding .dwg files.  
Figure 4-12 Images in IMG Folder 
 
 
 
 
 
P66

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-11 
4.3.6. Creating a Pressure Pipe Fitting in Civil 3D 
To create a new part, Civil 3D’s “Content Catalog Editor” could be used to create a 
database. “Content Catalog Editor” is a plug-in for Civil 3D, it is not a function or a 
panel in Civil 3D. To open the “Content Catalog Editor”, type “Content Catalog 
Editor” in the Window Search panel. Refer to below steps (a to p) for details. 
 
a) Draw lines to represent the run and branch.  
 
 
 
b) Copy lines to prepare for 3D model creation. 
 
 
 
c) Convert the original lines into a block to display a single line fitting.  
 
 
 
 
 
 
 
 
 
 
 
P67

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-12 
d) Type “BLOCK”. When block definition window pops up, define the part’s name.  
 
 
 
e) Pick the intersection point for the base point.  
 
 
 
 
 
 
 
 
 
 
 
 
P68

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-13 
f) Select the original lines as Objects and click “convert to block”.  
 
 
 
g) After the block is created, return to th e copied lines and draw few lines to 
represent the thickness of the flanges.  
 
 
h) Create circles with inner diameter and outer diameter for the body. Then, create 
three more circles for the flanges.  
 
P69

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-14 
i) Before forming the model, save the drawing as a .dwg into the “Pressure Pipes 
Catalog” first. It is suggested to crea te a new custom catalog instead of saving 
into the default catalog.  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
P70

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-15 
j) Back in the drawing, right click on the panel (as shown in Figure j-1) to choose 
the “Modelling” function (Figure j-2), and use “Sweep” function (Figure j-3) to 
create the 3D model.  
Figure j-1 
 
Figure j-2 
 
 
Figure j-3 for the Sweep function toolbar: 
 
 
 
 
 
 
 
 
 
 
 
 
P71

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-16 
k) Select the sweep objects (circles) first; then select the sweep path (lines).  
 
 
l) Change to 3D view (Screen l-1). For easier modelling, type “MOVE”, set the 
base point center to the flange object (Screen l-2), and move the flanges center 
to the end of the wye (Screen l-3).  
 
Screen l-1
 
 
P72

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-17 
Screen l-2 
 
 
 
Screen l-3 
 
 
P73

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-18 
The result after moving the flanges to the object is as follows: 
 
  
P74

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-19 
m) Change the view to “Realistic”, and us e the “Subtract” function to connect all 
the parts. Select all outer cylinder first (Figure m-1) then select the inner cylinder 
for subtraction (Figure m-2).  
 
The display panel view is as follows: 
 
 
The subtract toolbar is as follows: 
 
  
P75

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-20 
Screen m-1 
 
 
 
Screen m-2 
 
  
P76

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-21 
The result after subtracting the inner cylinder is as follows: 
 
Realistic: 
 
 
Wireframe: 
 
 
 
 
 
 
 
P77

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-22 
n) Move the block (Created in Step f) center to the 3D object.  
 
 
o) Under “Insert” Panel, select “Connection Point” tab, and insert the connection 
point into the objects. 
 
P78

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-23 
p) Type “PUBLISHPARTCONTENT” command and select the object (Figure p-1) 
and block (Figure p-2). Define the meas uring unit (Figure p-3) and part type 
(Figure p-4). Save the content file in the same “Custom_Catalog” folder. 
 
Screen p-1 
 
 
Screen p-2 
 
 
P79

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-24 
Screen p-3  
 
 
Screen p-4 
 
 
 
P80

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-25 
4.3.7. Using “Content Catalog Editor” to Create .sqlite File. 
a) In “Content Catalog Editor”, create a new file and import the content file (Figure 
below). The attributes should be input properly to complete the importing. 
Figure 4-13 Panel of “Content Catalog Editor” 
 
b) Import a part to content catalog under Catalog File: 
Figure 4-14 Configure General Information for Importing a Part 
 
 
 
 
 
P81

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-26 
c) Configure part type information: 
Figure 4-15 Configure Part Type Information 
 
 
 
 
  
P82

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-27 
d) Configure model properties: 
Figure 4-16 Configure Model Properties 
 
 
 
  
P83

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-28 
e) Review and update connection point information: 
Figure 4-17 Review and Update Connection Point Information 
 
  
P84

DEVB BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS APPENDIX V 
 
 
V-29 
f) After input the attributes, save as a new .sqlite file. The .sqlite file name should 
be same with the customed Catalog. 
Figure 4-18 Save the Content Catalog file 
 
 
g) This pressure pipe fitt ing can be reused for ot her projects by sharing 
the .sqlite, .dwg and Content Catalog File.  
 
4.3.8. Incorporating the Revit BIM Model into Civil 3D 
Revit BIM models could be incorporated into Civil 3D for authoring and coordination 
purposes. The steps are as follows: 
a) Export Revit BIM models to *.dwg 3D solids. 
b) In Civil 3D, open the *.dwg 3D solids and then inse rt Connection Points.  
“Connection Point” tab is under “Insert” Panel (refer to step o of Section 4.3.1). 
c) Use command “PUBLISHPARTCONTENT” to publish a *.content file (refer 
to step p of Section 4.3.1). 
d) In “Content Catalog Editor”, import the *.content file to “Pressure Network” 
content and customize the required attributes. 
 
 
 
P85
