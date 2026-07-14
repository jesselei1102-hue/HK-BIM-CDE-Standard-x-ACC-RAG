---
source_file: output/HK Standard/CIC BIM Standards General 2024/CIC BIM Standards General
  (Version 2024).pdf
doc_id: cicbims_2024
section_id: cicbims_2024_4_4_8_revision
title: 4.4.8 Revision
page_start: 126
page_end: 126
authority: CICBIMS 2024 §4.4.8
priority: high
language: en
source_url: hk_cde://cicbims_2024/cicbims_2024_4_4_8_revision
---

# 4.4.8 Revision

4 Common Data Environment [aligned with ISO 19650] 
 
 
126 
 
Example Model File Naming  = BIMS20 20-CIC-ZZ-01-AR_AA- M3-001 
(Architectural  AA 3D Model for 1 st floor of CIC’s BIMS2020 project, number 001) 
 
Example Drawing File Naming  = BIMS2020- CIC-ZZ-01-AR_AA-DR-001 
(Drawing for GBP Submission for 1 st floor of CIC’s BIMS2020 project)  
 
The file naming shall NOT include a revision status.  
Revisions shall be tracked using metadata added to the models or by the BIM Coordinator 
in a change management register, or automatically by CDE.  
 
4.4.8 Revision 
The ‘revision’ is a file property defined in the splash screen of a model file or the title block 
of a drawing sheet and should  also be defined in the document repository when the file is 
uploaded. The revision shows the iterative nature of the information as it progresses to 
completeness.  
 
The revision is required to track the progression of a file or document to its completion and 
authorisation. The revision needs to be part of the attributed metadata, but not a part of the 
file name. If it is included in the file name, then it effectively becomes another document 
when concatenated, and it cannot be tracked effectively. This is specifically an issue with 
linked reference files where the automatic updating of reference is paramount to the 
process. In a database solution, the metadata can be used to track and retrieve the files or 
documents in the most efficient manner.  
 
Revisions are divided into two main categories of P reliminary (P) and Construction (C). 
Preliminary revisions start at P01 and Construction revisions start at C01.  
 
4.4.9 Version 
The version is a subdivision of the revision and shows the iterative progress of the 
development  file during Work in Progress (WIP) and before confirmed release to ‘Shared’.  
 
If it is necessary to track the iterative nature of the file, which may include design options 
or elements awaiting design / coordination resolutions or Appointing Party's / Client’s 
decisions. Any extracted file for sketches, comment or review needs to know what revision 
/ version it belongs too. It may be necessary to share various versions of the file for 
Appointing Party's / Client’s decision regarding appropriate options etc. Any decision 
should be confirmed by sharing the confirmed version without the version codes to 
acknowledge this is the accepted Revision.  
 
In a database solution, it should be necessary to track versions when the extracted data is 
modified and reconnected to the spatial file. Tracking and updating should  be a constant 
activity, and the changing of attached properties or attributes to a file may be carried out 
without changing the graphical or spatial nature of the file. Versions should  then need to be 
included in any file references included.  
 
The ‘Revision  and ‘Version’ numbers are allocated as follows:  
 
• During WIP (Status S0), preliminary revisions and versions are P01.1, P01.2, or P02.1, 
P02.2, etc; 
• Before ‘authorised for construction’ (Status S1-Sn), preliminary revisions are P01, P02, 
P03, etc; and  
• Once ‘authorised for construction’ (Status A), revisions are C01, C02, C03, etc.
