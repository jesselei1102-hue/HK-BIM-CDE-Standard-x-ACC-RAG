---
source_file: output/HK Standard/DEVB BIM Harmonisation Guidelines for WDs (v3_0) with
  All Appendices.pdf
doc_id: devb_harmonisation_v3
section_id: devb_harmonisation_v3_loin_implementation
title: LOIN IMPLEMENTATION
page_start: 33
page_end: 37
authority: DEVB BIM Harmonisation v3.0 §LOIN
authority_type: standard
normative_weight: mandatory
discipline: general
lifecycle_stage: project
publication_year: 2023
software: null
priority: high
language: en
source_url: hk_cde://devb_harmonisation_v3/devb_harmonisation_v3_loin_implementation
---

# LOIN IMPLEMENTATION

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS LOIN IMPLEMENTATION 
 
24 
5. LOIN Implementation 
 
To enable information exchange using the GBDR, WDs shall follow the subsequent 
principles when authoring BIM files. 
5.1. Aligned BIM Standards 
5.1.1. The Guidelines should serve as the aligned standards for information exchange.    
 
5.2. BEP  
5.2.1. Referring to Section 2.1.2, BEP should incorporate requirements from asset owner. BEP 
should specify the BIM standards, guidelines and their applicable version for the 
project, . 
5.2.2. BEP should be authored in accordance with  departmental BEP templates or DEVB’s 
BEP reference template (if the former is unavailable) . In addition, BEP should 
document the following: 
a) Information owner’s identification; 
b) Project information requirements (e.g. element-specific LOD-I attributes in table 
or list formats); 
c) Project-specific federation strategy; and 
d) Project-specific codes for BIM model naming (e.g. project code(s), location 
codes). 
 
5.3. BIM Modelling Setting 
5.3.1. Coordinate System 
All BIM files shall be authored and annotat ed directly with reference to the Hong 
Kong 1980 Grid (HK 1980 Grid) and Hong Kong Principal Datum (HKPD). 
5.3.2. Model Unit 
The model unit in all BIM fi les should be metric (e.g., in millimetres (mm) for 
buildings or in metres (m) for infrastructure projects) and based on a decimal system. 
5.3.3. BIM Template 
Project-specific BIM template could be pr epared for the software commonly used. 
The template could include: 
a) Coordinate system and unit setting; 
b) Setting for drawing generation; and 
c) Common attributes. 
5.3.4. Mandatory Requirements for BIM modelling 
P33

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS LOIN IMPLEMENTATION 
25 
a) Use the object at the CIC BIM Objects lib rary, instead of creating own object, as
far as practicable to ma
intain the consistency, such as inserting point and BIM
attributes of the object.
b) If new object is developed, register the obj ect file in the CIC BIM objects library
timely.
c) Do not add user defined parameter with the same name as the system built-in
parameters. Use a prefix such as departmental abbreviation code to differentiate the
system built-in parameters from the user-defined parameters.
d) Linked files will not be exported to IFC by default, keep them in the native file
format for conversion, if needed.
e) Use the common object types for modelling.  For example, objec t type as listed
below could be used when modelling in Civil 3D:
Item no. 
Recommended object type Remark 
1 Tin surface - These object types can
be exported to IFC
- Technical details of
these types can be
maintained when
exporting to IFC
2 Pipe 
3 Structure 
4 Pressure pipe 
5 Fittin g 
6 Appurtenance 
7 3D solid (Extracted from corridor) 
f) Do not add IFC classes in the user defined attribu
te as this will mix up the mapping
to IFC conversion.
g) Only objects exist in the last phase will be  exported to IFC by default.  Do not set
the Properties - “Phase Created” and “Pha se Demolished” to the same value,
otherwise it would be treated  as temporary or not exis t feature and will not be
exported to IFC.
h) When preparing IFC for submission to the GBDR, Reference View v1.2 in
ArchiCAD, OpenBuildings Designer, and Revit; or Coordination View v2.0 in
Civil 3D should be set as Model View Definitions.
5.4. LOD-G 
5.4.1. LOD-G Requirements 
The table below describes LOD-G requi rements of LOD 100 to 500 which are 
consistent with the principles of CIC BI M Standards (the latest version). LOD-G 
refers to the graphical re presentation which deals wi th geometric representation, 
symbology, and visualisation. This is genera lly related to the deliverable (scale of 
documentation) which controls the graphical precision of the elements represented. 
This in turn enables identification of which parts of the objects can be disregarded 
or simplified while keeping the object functional to meet the BIM Uses. 
P34

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS LOIN IMPLEMENTATION 
26 
Table 5-1 LOD-G Definition 
LOD-G Description 
100 The model element is graphically represented within the model by a 
symbol or generic representation or rough 3D shape. 
200 The model element is graphically represented within the model as a 
generic system, object or assembly with approximate quantities, 
assumed size, shape, location, and orientation. The assumed spaces 
required for access and maintenance shall be indicated. 
300 The model element is graphically represented within the model as a 
specific system, object or assembly in terms of quantity, size, shape, 
location, and orientation. The model shall include details of the 
spaces required for handling installation, operation and maintenance, 
and the interface details for checking and coordinating with other 
models / objects. 
400 The model element is graphically represented within the model as a 
specific system, object or assembly in terms of quantity, size, shape, 
location, and orientation with detailing for fabrication, assembly, 
and installation. 
500 Not used. 
Refer to the latest version of CIC BIM Standards - General for 
details.  
5.4.2. Overlapping Elements  
Overlapping elements should be avoi ded and minimised. When overlapping 
elements cannot be eliminated, the reason and associated para meter for filtering 
should be documented in the BEP. 
5.4.3. Large Spanning Continuous Elements  
Model elements spanning over one level (e.g. wa
lls spanning over 1 storey high) or 
across buildings (e.g. floor plates spanni ng between buildings through connection 
bridges) should be split into separate model elements, unless otherwise specified in 
the BEP. 
5.4.4. Complex Geometry 
For constructability, especially for design-stage considerations, complex geometries 
such as two-way curves and non-uniform rational basis spline surfaces shall be 
avoided whenever possible. When comple x geometries cannot be eliminated, its 
modelling method shall be documented in BEP. 
5.4.5. Room 
P35

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS LOIN IMPLEMENTATION 
 
27 
To facilitate spatial id entification, drawing genera tion and subsequent mapping 
works for spatial data (e.g. display of room tags), room should be modelled as far as 
practicable for spaces  bounded by architectural and structural elements, such as 
public access area of Government buildings . It may also be modelled by either 
manually assigning the centre point or drawing an enclosed boundary. 
5.4.6. Operation and Maintenance Space 
For building services and mechanical t ype of BIM elements, the operation and 
maintenance space are concerned information for asset owner. It is suggested to 
model the operation and maintenance space for these kinds of BIM elements, such 
as control panel/switch box with panel door, vent relief valv e (VRV) unit with 
control valve set, etc.  
 
5.5. LOD-I 
5.5.1. LOD-I Grouping 
Attributes (LOD-I) could be grouped by general properties, design properties, 
classification properties (e.g.  OmniClass), manufacturer ’s equipment properties, 
condition properties and verification pr operty. Under each grouping, the list of 
attributes may differ due to WDs’ LOD -I requirements. The creation methods of 
attributes for BIM objects would vary by software. Refer to Appendix VI for details. 
5.5.2. Project Information 
To facilitate conversion engine’s processes, all relevant project information (such as 
Organisation Name, Project Issue Date, Client Name, Project Address, Project Name 
and Project Number) should be inputted in all BIM files as part  of the LOD-I for 
metadata extraction and geolocation. Refer to Appendix VI which shows the project 
information input methods of Revit and Civil 3D.  
5.5.3. BIM Attributes (Attributes) 
BIM models and BIM objects should be au thored with required general properties 
and attributes. Refer to Appendix VI for details. 
5.5.4. Language 
Unless specifically required by the BEP, all project information and attributes should 
be in the English language. 
 
5.6. Appearance 
5.6.1. Within each WD, model elements’ shading colours shall follow RGB codes specified 
based on the prevailing systems in WDs’ guid elines for design authoring. For 3D 
coordination, WDs’ own colour standards may be adopted. Deviations, if any, should 
be documented in BEP. 
5.6.2. For interdepartmental 3D coordination betw een WDs, colour appearance should be 
based on Discipline (Field 5.1 of the nami ng convention) as specified in Section 4.2. 
P36

BIM HARMONISATION GUIDELINES 
FOR WORKS DEPARTMENTS LOIN IMPLEMENTATION 
28 
GBDR will be capable of setting the colour  appearance of various Disciplines in 
accordance with Tables 5-2 and 5-3. 
Table 5-2 Colour Appearance by Discipline for Underground Utilities 
Codes Discipline Colour (RGB) Reference Colour 
Appearance 
CD Chilled Water Distribution 0-255-0 ArchSD, 
EMSD 
FO Sewerage 255-0-0 DSD 
FW Fresh Water System 228-232-225 WSD 
GS Gas Supply 255-0-255 N/A 
IR Irrigation 0-255-255 ArchSD, 
EMSD 
PS Electrical Power Supply 93-173-115 DSD, WSD 
RW Raw Water System 77-166-190 WSD 
SD Stormwater Drainage 0-0-255 DSD 
SW Salt Water System 106-108-60 WSD 
TC Telecommunicat ion 230-205-255 N/A 
WR Recycled Water System 0-128-255 ArchSD, 
EMSD 
Table 5-3 Colour Appearance by Discipline for Above-grade 
Codes Discipline Colour 
(RGB) Reference Colour 
Appearance 
AR Architectural 255-255-255 N/A 
BS Building Services 255-128-0 N/A 
EL Electrical 93-173-115 DSD, WSD 
FS Fire Services 255-0-0 ArchSD, 
EMSD 
LA Landscape 0-255-0 N/A 
ME  Mechanical 233-193-0 DSD 
RD Road 191-191-191 N/A 
SF Site Formation 226-183-120 N/A 
SL Slope 143-91-63 N/A 
ST Structural 119-104-93 DSD 
P37
