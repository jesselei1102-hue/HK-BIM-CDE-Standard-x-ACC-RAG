---
source_file: output/HK Standard/CIC BIM Standard/CIC Production of BIM Object Guide
  - General Requirements (2021).pdf
doc_id: cic_object_guide_2021
section_id: cic_object_guide_2021_6_level_of_information_lod_i_requirements
title: 6 Level of Information (LOD-I) Requirements
page_start: 14
page_end: 14
authority: CIC BIM Object Guide 2021 §6
authority_type: standard
normative_weight: recommended
discipline: bim_objects
lifecycle_stage: project
publication_year: 2021
software: null
priority: high
language: en
source_url: hk_cde://cic_object_guide_2021/cic_object_guide_2021_6_level_of_information_lod_i_requirements
---

# 6 Level of Information (LOD-I) Requirements

CIC PRODUCTION OF BIM OBJECT GUIDE 
11 
6 Level of Information (LOD-I) 
Requirements 
This section defines the non-geometrical requirements (information) contained within a BIM object, including aspects such as 
property, value, units and property naming convention. 
6.1 General 
1. The BIM object shall contain properties that are suitably assigned as type  or instance / component.  All instance 
of the BIM object in the project will be affected by the type property.  The instance / component property can be 
customised for each instance of the BIM object in the project. 
2. The BIM object shall contain minimum information for the purpose of phasing, e.g. placeholder (space occupation) 
at the design phase, coordination at the construction phase and reality reflection at the facility management phase. 
3. Unless otherwise required, t he BIM object shall not include undefined values .  Every additional property shall be 
completed and shall not include unset or undefined values. 
4. The BIM object may contain additional information which helps to describe the product. 
5. The BIM object shall use appropriate units of measurements.  Basically, millimetre (mm) is the most commonly used 
unit in local practice.  The units of measurements shall be consistent with the EMSD Building Information Modelling 
for Asset Management (BIM-AM) Standards and Guidelines.  Any units of measurements which are not stated in the 
document shall be based on the International System of Units (SI). 
6. Field names of attributes shall be in English to ensure information exchange and extraction. For values of the field, 
non-English language may exist and is allowed due to project -specific needs or manufacturing location outside of 
HKSAR. For example, common names for plants in Chinese may be used instead of Latin botanical names. Based 
on the origin of building products and equipment, brand names and locations in native language may be used.  
 
6.2 Property / Parameter 
1. The BIM object property shall provide accurate information. 
2. The BIM object property shall  be an unambiguous definition  to facilitate consistent  BIM object selection and 
submission between different stages.  Besides any default property provided by the BIM platform, additional BIM 
object properties shall have a consistent order of definition, property name and unit. These method of referencing is 
suggested to all BIM developer s to increase information exchange at different stages in a project, although it is 
recognised that certain BIM developers will have variations in accordance to their needs based on project and client 
requirements. 
3. The BIM object property shall not include user defined parameter s with the same name as the system bui lt-in 
parameters. Using a prefix such as departmental abbreviation code to differentiate the system buil t-in parameters 
from the user-defined parameters. 
4. The BIM object property assists in describing its geometrical and non-geometrical characteristics. The property value 
may be presented as a single value, list value or range value.  However, the BIM platform system may have 
restrictions in assigning a property value, e.g. only a single value is allowed for each numerical data item, or only 
numerical data is all owed to be added in an arithmetic formula.  The following table gives guidance for choos ing a 
suitable data type and format for assigning BIM object property values;
