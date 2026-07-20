---
source_file: output/HK Standard/CIC BIM Standard/CIC Production of BIM Object Guide
  - General Requirements (2021).pdf
doc_id: cic_object_guide_2021
section_id: cic_object_guide_2021_6_3_property_naming
title: 6.3 Property Naming
page_start: 15
page_end: 15
authority: CIC BIM Object Guide 2021 §6.3
authority_type: standard
normative_weight: recommended
discipline: bim_objects
lifecycle_stage: project
publication_year: 2021
software: null
priority: high
language: en
source_url: hk_cde://cic_object_guide_2021/cic_object_guide_2021_6_3_property_naming
---

# 6.3 Property Naming

CIC PRODUCTION OF BIM OBJECT GUIDE 
12 
Present Format Usage Data Type Example Remark 
Single Value Description 
Only 
Text / 
Numerical 
Creator Name (Mr. Chan) 
Net Weight (40 kg) 
 
Single Value Calculation Numerical Dimension (200 mm)  
List Value Description 
Only 
Text Colour Option (Black, White) 
Optional Wattage / Lumen 
(13/1055, 33/4000) 
 
List Value Calculation Numerical Optional S ize (3000mm 
3500mm 4000mm) 
If restricted by the system, consider 
breaking to a separate property or BIM 
object type. 
Range Value Description 
Only 
Text Allowable Setting Value (-4ºC ~ 
0ºC) 
 
Range Value Calculation Numerical Input Voltage (100V~230V) Range value shall be separated into 
two properties to represent its lower 
bound and upper bound values. 
 
 
6.3 Property Naming 
1. The BIM object property shall use Camel Case and title casing for parameter naming, e.g. Coefficient of Performance; 
Point of Shipment. 
2. The BIM object property shall use descriptive naming.  The name shall describe the property’s meaning or definition 
rather than describing the product component. 
3. The BIM object property shall not be ended with a space or full stop.  
4. The BIM object property should be named as short as possible. 
5. The BIM object property should avoid abbreviation and truncation in cases where there is no unambiguous definition 
or industrial consensus. 
6. The BIM object property should use the most common descriptor for a group as the first part of the name so that the 
property can be sorted logically (e.g., Filter Face Area; Filter Efficiency). 
7. The BIM object property shall avoid using symbols in property naming. 
8. The BIM object property naming with boolean (YES/NO) data types shall b e named such that they clearly imply a 
YES/NO value is returned, e.g. Is Energy Efficient, Show Hoods.
