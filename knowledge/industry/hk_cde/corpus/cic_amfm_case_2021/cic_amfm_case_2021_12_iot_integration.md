---
source_file: output/HK Standard/CIC BIM for Asset Management and Facility Management
  Case Sharing 2021.pdf
doc_id: cic_amfm_case_2021
section_id: cic_amfm_case_2021_12_iot_integration
title: 12. IoT Integration
page_start: 32
page_end: 32
authority: CIC AM/FM Case Sharing 2021 §12.
authority_type: case_study
normative_weight: reference
discipline: am_fm
lifecycle_stage: operations
publication_year: 2021
software: null
priority: normal
language: en
source_url: hk_cde://cic_amfm_case_2021/cic_amfm_case_2021_12_iot_integration
---

# 12. IoT Integration

Page 32 of 46 
 
12. IoT Integration 
 
RESTful (JSON) was the format used for the integration between BIM Model and IoT sensors . The data 
exchange is bi-directional. The IoT Platform would send sensor readings to Planon, and Planon will then 
trigger to IoT Platform to send data ad-hocly.  
 
 
 
 
 
 
 
 
 
 
 
 
 
12.1. IoT Platform to Planon  
• Change of Value 
When the change of value is detected by the IoT Platform, it will send the updated meter reading 
to Planon via “Send Meter Readings” service type. 
 
• Keep alive 
When the point failure is detected by the IoT Platform, it will notify Planon and update the Meter 
status to ‘Active’ status via “Keep Alive” service type.  
 
12.2. Data field definition 
• Send Meter Readings 
The IoT Platform calls this service to create readings. This can be for On/Off, Single value and 
IEQ types. 
 
• Keep Alive 
The IoT Platform calls this service to update meter status. 
 
  
 
 
Web service 
Web service 
Planon 
Cloud 
IoT Platform 
Cloud 
Meter readings 
Ad-hoc Query 
Send email 
notification
