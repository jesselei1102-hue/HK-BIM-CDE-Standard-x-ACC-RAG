---
source_file: output/HK Standard/CIC BIM Standard/CIC BIM Standards for Preparation
  of Statutory Plan Submissions Dec2020/CIC BIM Standards for Preparation of Statutory
  Plan Submissions Dec2020.pdf
doc_id: cic_statutory_plans_2020
section_id: cic_statutory_plans_2020_5_3_1_data_driven_bim_object_requirements
title: 5.3.1 Data-driven BIM Object requirements
page_start: 33
page_end: 37
authority: CIC Statutory Plan Submissions 2020 §5.3.1
authority_type: statutory
normative_weight: mandatory
discipline: statutory_submission
lifecycle_stage: statutory
publication_year: 2020
software: null
priority: high
language: en
source_url: hk_cde://cic_statutory_plans_2020/cic_statutory_plans_2020_5_3_1_data_driven_bim_object_requirements
---

# 5.3.1 Data-driven BIM Object requirements

21 
 
Separate submission for hoarding and covered walkway may be required for acceptance by 
BA. The AP/RSE/RGE should refer to essential information to be provided and shown on 
the hoarding and covered walkway plans as required under Code of Practice for Demolition 
of Buildings 2004 and the relevant PNAPs including but not limited to PNAPs APP-21 and 
APP-23.   
5.3.1 Data-driven BIM Object requirements 
The existing building to be demolished should be modelled for the structural system, 
demolition methodology, sequence of demolition, details about the use of mechanical plants, 
and precautionary works and safety measures for the public. 
(Refer to Software User Guides for parameter naming in templates.) 
 BIM Object Graphical 
Information 
Non-graphical 
Information 
Concrete structural 
slab 
• Intelligent Object 
indexed/categorised as 
‘Structural Floor’ with a 
whole piece of Intelligent 
Object for all spans at 
the same floor level 
(ignoring individual 
span) 
• Top of slab should be 
modelled to structural 
floor level 
• Thickness of floor 
should only be the 
thickness of the cast in 
situ part 
• Thickness 
• Rebar size / shape / 
spacing / concrete cover 
• Cantilevered balconies 
or Cantilevered 
structures # 
• Rebar material grade 
/ layer 
Structural beam 
(concrete) 
• Intelligent Object 
indexed/categorised as 
‘Structural Framing’ 
• Structural beam should 
be modelled to the full 
structural size of the 
width and depth 
• Width 
• Depth 
• Rebar size / shape / 
spacing / concrete cover 
• Rebar material grade 
Structural beam 
(steel) 
• Intelligent Object 
indexed/categorised as 
‘Structural Framing’ 
• Structural beam should 
be modelled to the full 
structural size of the 
width, depth and 
thickness of flange/web 
• Width 
• Depth 
• Additional information 
should be provided to 
define the geometry 
(e.g. thickness of 
flange/web) 
• Object mark 
• Type mark 
• Steel grade 
• Steel density 
• Section Physical 
Properties (e.g. 
second moment of 
area, radius of 
gyration etc.)

22 
 
 BIM Object Graphical 
Information 
Non-graphical 
Information 
Structural column 
(concrete) 
• Intelligent Object 
indexed/categorised as 
‘Structural Column’ 
• Structural column 
should be modelled to 
the full structural size of 
length, width and height 
• Length 
• Width 
• Height 
• Rebar size / shape / 
spacing / concrete cover 
• Rebar material grade 
/ steel ratio 
Structural column 
(steel) 
• Intelligent Object 
indexed/categorised as 
‘Structural Column’ 
• Structural Column 
should be modelled to 
the full structural size of 
width, depth, height and 
thickness of flange/web 
• Length 
• Width 
• Height 
• Thickness of flange/web 
• Object mark 
• Type mark 
• Steel grade 
• Steel density 
• Section Physical 
Properties (e.g. 
second moment of 
area, radius of 
gyration etc.) 
Structural wall 
(concrete) 
• Intelligent Object 
indexed/categorised as 
‘Wall’ with identifier for 
‘Structural’ 
• Structural wall should be 
modelled to the full 
structural size of length, 
thickness and height 
• Length 
• Thickness 
• Rebar size / shape / 
spacing / concrete cover 
• Rebar material grade 
/ steel ratio 
Stair (concrete) • Intelligent Object 
indexed/categorised as 
‘Stair’ for all landings 
and flights 
• Top level of landing and 
flight should be 
modelled to the 
structural floor level of 
the item 
• Thickness (landing and 
flight) 
• Rebar size / shape / 
spacing / concrete cover 
• Rebar material grade 
Stair (concrete) • Intelligent Object 
indexed/categorised as 
‘Stair’ for all landing and 
flight 
• Top level of landing and 
flight should be 
modelled to the 
Structural Floor Level of 
the item 
• Rebar should be 
modelled with sufficient 
• Thickness (landing and 
flight) 
• Rebar size / shape / 
spacing / concrete cover 
• Object mark 
• Concrete grade 
• Concrete density 
• Rebar material grade

23 
 
 BIM Object Graphical 
Information 
Non-graphical 
Information 
details for statutory plan 
submission  
Hangers (or 
hanging structures) 
• Intelligent Objects 
indexed/categorised as 
‘Wall’ with identifier for 
‘Hanger’ 
• Hangers should be 
modelled to the full 
structural size of length, 
thickness and height 
• Length 
• Thickness 
• Rebar size / shape / 
spacing / concrete cover 
• Rebar material grade 
/ steel ratio 
Temporary 
supports 
• Intelligent Objects 
indexed/categorised as 
‘Temporary Works’ 
modelled in full size and 
configuration with the 
major elements (e.g. 
vertical members and 
bracings) included 
• Temporary support 
spacing 
• NONE 
Scaffolding, Screen 
covers and 
catchfan 
• Intelligent Objects 
indexed/categorised as 
‘Temporary Works’ 
• Bamboo scaffolding 
should be modelled to 
the overall profile 
showing the location 
and space to be 
occupied. (Details of 
bamboo and its fixing 
are not necessary.) 
• Width • NONE 
Debris chute • Intelligent Objects 
indexed/categorised as 
‘Temporary Works’ 
• Debris chute should be 
modelled to the overall 
profile showing the 
location and space to be 
occupied. (Details of 
debris chute and its 
fixing are not 
necessary.) 
• NONE • NONE 
Hoarding, covered 
walkway and 
catchfan 
• Intelligent Objects 
indexed/categorised as 
‘Site’ 
• Hoardings and covered 
walkway should be 
modelled to the full 
• Footing length 
• Footing width 
• Footing height 
• NONE

24 
 
 BIM Object Graphical 
Information 
Non-graphical 
Information 
geometry of the footing 
base and the geometry 
of the overall profile of 
the hoarding and 
covered walkway 
structure above the 
footing 
Street furniture • Intelligent Objects 
indexed/categorised as 
‘Street Furniture’ 
• The following items 
within the pavement 
area should be modelled 
with Intelligent Objects:   
• Railing 
• Traffic light 
• Fire hydrant 
• Lamp post/lighting mast 
• Pillar box 
• Tram cable 
mast/support 
• Trees along the 
hoarding alignment 
should be represented 
by a point cloud 
produced by laser 
scanning 
• Bus Stop 
• Road Sign 
• Post Box 
• Parking meters 
• NONE • NONE 
CCTV • Intelligent Objects 
indexed/categorised as 
“Site” 
• The intended location, 
elevation and viewing 
direction shall be 
specified 
• Location 
• Height from reference 
level 
• Viewing Direction 
• NONE 
Adjacent Building  • Massing blocks • Building Height 
• Building Extent 
• NONE 
Monitoring 
Instrument 
• Generic Object with a 
symbolic shape and size 
should be modelled and 
added to location at 
• NONE • Marker mark 
• Type

25 
 
 BIM Object Graphical 
Information 
Non-graphical 
Information 
ground or on structure 
where it is intended to 
be installed 
Table 10 
# Refer to Software User Guides for parameter settings in templates. 
 
5.3.2 2D Annotation requirements 
Typical method of demolishing structural elements should be shown in 2D drafting only. 
Type of 2D 
Annotation 
Tag/Symbol/Others Remarks 
Prestressed Concrete 
structure 
Hatch • Hatch linked with the parameter value of 
‘Prestressed Concrete Structure’ in Slab objects 
Cantilever structure Hatch • Hatch linked with the parameter value of 
‘Cantilever Structure’ in Slab objects 
Exit Route Symbol • Symbol to be placed on drawing view to show 
the exit route 
Table 11 
5.3.3 Types of plans to be produced from BIM 
Based on the above requirements, sample drawings to illustrate the preparation of demolition 
plans including general notes, layout plans and sections, details generated by BIM software 
are provided in Appendix A for reference. 
Hoarding, covered walkway and catchfan layout and details should be under separate 
submission. 
5.3.4 BIM Object Presentation Style 
The presentation style defined in table below is for reference only instead of B A’s 
requirements to follow. 
 Projection Cut 
Line Pattern Line Pattern 
Style, 
Colour, 
Thickness 
Style, 
Colour 
Style, Colour 
Thickness 
Style, 
Colour 
Framing plans 
(1:100) 
Slab Solid 
Black 
0.22 mm 
Solid fill, RGB 
255-255-206 
Solid 
Black 
0.22 mm 
None
