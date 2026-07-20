---
source_file: output/HK Standard/CIC BIM Standard/CIC BIM Standards for Preparation
  of Statutory Plan Submissions Dec2020/Appendix 3 CIC BIM User Guide for Preparation
  of Statutory Plan Submissions Revit Dec2020.pdf
doc_id: cic_stat_revit_2020
section_id: cic_stat_revit_2020_4_1_superstructure
title: 4.1 Superstructure
page_start: 19
page_end: 38
authority: CIC Statutory Revit Guide 2020 §4.1
authority_type: software_guide
normative_weight: operational
discipline: statutory_submission
lifecycle_stage: statutory
publication_year: 2020
software: Revit
priority: normal
language: en
source_url: hk_cde://cic_stat_revit_2020/cic_stat_revit_2020_4_1_superstructure
---

# 4.1 Superstructure

13 
4 Creating Model Objects 
 
4.1 Superstructure 
The following objects will be modelled in the structural plan: 
  Slab 
  Column 
  Wall 
  Beam 
  Lift Shaft 
  Staircase 
  Water Tank 
  Reinforcement 
 
 
 
4.1.1 Create a Slab 
Open a structural plan in Revit ➜ Click “Structure” in ribbon ➜ click “Floor” ➜ 
click “Floor: Structural” 
 
In the properties panel, you may choose the specific types of the slab from floor 
family or create by your own. Adjust the value for “Height Offset From Level”.

14 
 
Create the slab by drawing boundary line ➜ select “Span Direction” ➜ click 
“tick”. 
 
 
 
 
 
Repeat the above steps. 
 
 
 
Add level difference symbol and span direction symbol in plan view  (Refer to 
section 7.1.4 Add annotation symbol) 
 
Category Family Type 
Generic 
Annotation 
ANN-GNN-CIC-Level_Difference  / 
Generic 
Annotation 
ANN-GNN-CIC-Span_Direction Two Way Slab - 
2.5mm One Way 
Slab  - 2.5mm 
Cantilever  Slab - 2.5mm

15 
 
 
 
4.1.2 Create Column 
Open a structural plan in Revit ➜ Click “Structure” in ribbon ➜ click “Column”. 
 
In the properties panel, you may choose the specific types of the column from 
column family or create by your own. Adjust the value for “Base Level”, “Base 
Offset”, “Top Level” and “Top Offset”. 
 
In the properties panel, type column mark in “Mark” of identity data. For 
example, C1A was typed for column mark in this case. ➜ Place the column into 
designed location.

16 
Repeat the above steps. 
 
 
 
Add Tag in plan view (Refer to section 7.1.2 Add Tags – Tag by Category) 
 
Category Family Type 
Structural Column ANN-SCG-CIC Mark 
 
 
 
 
4.1.3 Create Wall 
Open a structural plan in Revit ➜ Click “Architecture” in the ribbon ➜ “Build” ➜ 
click “Wall” ➜ click “Wall: Structural”.

17 
In the properties panel, you may choose the specific types of the wall from 
column family or create by your own. 
 
 
In the properties panel, place the wall by setting  base constraint and top 
constraint to demonstrate the floor extension of the wall. Adjust the value for 
“Base Constraint”, “Base Offset”, “Top Constraint” and “Top Offset”. 
 
 
 
Drag the wall from the start point to endpoint. 
 
In the properties panel, type wall mark in “Mark” of identity data. For example, 
W5B was typed for wall mark in this case.

18 
 
 
 
Add Tag in plan view (Refer to section 7.1.2 Add Tags – Tag by Category) 
 
Category Family Type 
Wall ANN-WLG-CIC Mark 
Type Mark 
 
 
4.1.4 Create Beam 
Open a structural plan in Revit ➜ Click “Structure” in ribbon ➜ click “Structure” 
➜ click “Beam” 
 
In the properties panel, you may choose the specific types of the beam from 
beam family or create by your own.

19 
Create the slab by drawing start point and end point ➜ Enter the value for “Start 
Level Offset” and “End Level Offset” or “Z Offset Value” for beam or inverted 
beam in the constraint of properties. 
 
In the properties panel, add beam mark in “Mark” of identity data. For example, 
TB18 was typed for beam mark in this case. 
In Structural group, tick the property “Cantilever” or “Transfer” to identify the 
specific beam. 
 
Add Tag in plan view (Refer to section 7.1.2 Add Tags – Tag by Category) 
 
Category Family Type 
Structural Framing ANN-FRG-CIC-
Rectangular 
Standard

20 
4.1.5 Create Lift Shaft 
Open a structural plan in Revit ➜ Click “Structure” in ribbon ➜ click “Opening” 
➜ click “Shaft” 
 
Create the shaft by drawing boundary line / using detail line on plan ➜ click 
“symbolic line” to create cross indication for shaft ➜ click “tick”. 
 
 
In the properties panel, enter the value for base constraint, base offset, top 
constrain and top offset to control the shaft location and level. 
 
 
4.1.6 Create a Staircase 
Open a structural plan in Revit ➜ Click “Architecture” in ribbon ➜ “Circulation” 
➜ click “Stair”

21 
Click “Run” ➜ Create the staircase by drawing start point to end point, and 
landing on plan ➜ click “tick”. 
In the properties panel, use the base level, top-level and offset to control the 
staircase location and level. 
 
 
 
 
4.1.7 Create a Water Tank 
Open a structural plan in Revit ➜ Click “Structure” in ribbon ➜ “Model” ➜ 
”Component” ➜ click “Model In-Place” 
Select “Generic Models” in the Family Category and Parameters dialogue and fill 
in the name of the water tank.

22 
Draw the water tank by using “Forms” tools. 
 
 
 
 
 
4.1.8 Create Reinforcement (Beam / Column / Wall / Staircase / Water  Tank) 
After the creation of Beam, Column, Wall, Staircase ➜ Open a structural plan in 
Revit ➜ right click the plan in project browser ➜ click “Duplicate View” to 
duplicate the plan ➜ click “Duplicate” 
 
 
Create column rebar plan ➜ click “View” ➜ “Graphics” ➜ click “Visibility/ 
Graphics” to show the column and rebar in plan only.

23 
Unclick all items, except “Structural Column” and “Structural Rebar” in Visibility/ 
Graphics window ➜click “Apply” ➜ click “OK”. 
 
 
Only column is shown on the screen. 
 
 
Select a column ➜ click “Reinforcement” in ribbon ➜ click “Rebar”.

24 
Select the “Placement Plane” in R ibbon ➜ select “current work plane / near 
cover reference / far cover reference” to place the rebar plane. 
 
Create a stirrup ➜ In the properties panel, you may choose the specific rebar 
bar and rebar shape from rebar family or create by your own.

25 
 
 
 
Change the rebar spacing in rebar set of Ribbon . 
 
Change the quantity of rebar and direction in rebar set of Ribbon . 
 
Repeat the above step for mains and links.  
 
Repeat the above steps for Beam and Wall.

26 
Add Tag in plan view/ section view  (Refer to section 7.1.2 Add Tags –  Tag by 
Category) 
 
Category Family Type 
Structural 
Rebar 
ANN-RBG-CIC

27 
4.1.9 Create Reinforcement (Path) 
After the creation of Slab ➜ Click “Structure” in ribbon ➜ “Reinforcement” ➜ 
Click “Path” 
 
Select the floor ➜ Sketch the line of the path on the floor.

28 
In the properties panel, fill in the information of “Layout Rule”, “Additional Offset”, 
“Face”, “Bar Spacing”, “Primary Bar – Type”, “Primary Bar – Length”, “Primary 
Bar – Shape”, “Primary Bar – Start Hook”, “Primary Bar – End Hook”. 
For “Rebar Layer”, fill in T1/T2/B1/B2, etc. 
 
Select the structural path reinforcement symbol. In the properties panel, select  
“ANN-PHG-CIC-Symbol (Top)” for top layer rebar and “ANN-PHG-CIC-Symbol 
(Bottom)” for bottom layer rebar. 
 
 
Add path reinforcement symbol in plan view  
Click “Annotation” in ribbon ➜ ”Symbol” ➜ click “Path”. 
 
Select between “Top” or “Bottom” for a different layer of the rebar.

29 
 
Add Tag in plan view (Refer to section 7.1.2 Add Tags – Tag by Category) 
 
Category Family Type 
Structural Path 
Reinforcement  
ANN-PHG-CIC-
Tag 
Standard

30 
4.1.10 Create Reinforcement (Area) 
After the creation of Slab ➜ Click “Structure” in ribbon ➜ “Reinforcement” ➜ 
Click “Area” 
 
Select the floor ➜ sketch the boundary of slab to form a closed loop  
 
A parallel line symbol indicates the major direction edge of the area 
reinforcement. 
For major direction, tick “Top Major Direction” and “Bottom Major Direction” in 
the properties panel. Select the “Top Major Bar Type” and “Top Major Spacing”. 
Set the value of “Bottom Major Bar Type “and “Bottom Major Spacing”,

31 
 
Copy the previous Structural Area Reinforcement object and paste “Aligned to 
the Same Place” as the rebars for minor direction. 
For minor direction, tick “Top Minor Direction” and “Bottom Minor Direction” in 
the properties panel. Sele ct the “Top Minor Bar Type” and “Top Minor Spacing”. 
Set the value of “Bottom Minor Bar Type “, “Bottom Minor Spacing”, “Additional 
Top Cover Offset” and “Additional Bottom Cover Offset”.

32 
Go to 3D View, there are four layers of rebars. Select the first layer of rebars and 
add “T1” to Comments in the properties panel. Select the second layer of rebars 
and add “T2” to Comments. For  the bottom layer of rebar, add “B2” to 
Comments for the third layer and add “B1” to Comments for the fourth layer. 
 
 
Add Tag in plan view (Refer to section 7.1.2 Add Tags – Tag by Category) 
 
Category Family Type 
Structural Area 
Reinforcement 
ANN-ARG-CIC Major / Minor
