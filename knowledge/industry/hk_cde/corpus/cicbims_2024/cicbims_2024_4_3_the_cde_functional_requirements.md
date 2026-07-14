---
source_file: output/HK Standard/CIC BIM Standards General 2024/CIC BIM Standards General
  (Version 2024).pdf
doc_id: cicbims_2024
section_id: cicbims_2024_4_3_the_cde_functional_requirements
title: 4.3 The CDE Functional Requirements
page_start: 115
page_end: 117
authority: CICBIMS 2024 §4.3
priority: high
language: en
source_url: hk_cde://cicbims_2024/cicbims_2024_4_3_the_cde_functional_requirements
---

# 4.3 The CDE Functional Requirements

4 Common Data Environment [aligned with ISO 19650] 
 
115 
 
4.3 The CDE Functional Requirements 
 
4.3.1 CDE Functional Sections as Locations or States 
The purpose of each functional section of the CDE  is to remove any ambiguity regarding 
the state of information and what it may be used for. Key to this is the role- based security 
which control information visibility and access rights. These enforces the workflows and 
therefore the associated trust within the information provided.  
 
Different solutions deal with these technology challenges in different ways. The two main 
methods of identifying different environments are:  
 
• Location based folders: and 
• Role based security states using meta data (attributes). 
 
The use of folders as containers to control access security was the traditional approach 
that represent the windows desktop workflow and traditional security -based requirements. 
This methodology is used to move files from folder to folder as the files progresses through 
the workflow. Each folder had the appropriate security controlling who had access, tasks 
they were entitled to undertake etc. The solution on completion of a specific task would 
trigger the moving of the file to the next folder, changing the security, access, and visibility.  
 
Whilst the technology needs for this approach are less onerous this often requires a 
manual process of moving files where the second revision of a file (Drawing 1 Rev P2) 
when released requires the first revision (Drawing 1 Rev P1) to be moved to the Archive 
section or it should  be overwritten. This often also required the creation of date related 
folders as duplicates of files were not allowed. The current version of the file should  be 
stored in the shared section whilst historic versions should  need to be moved to the 
Archive. This often leads to duplication of files in multiple locations with a possibility of 
these becoming out of sync.  
 
 
Figure 29 Folder approach to CDE Shared and Archive 
The alternate approach is to use a State based approach where specific meta data 
(attributes), instead of locations, control how security is applied, and these identify the 
workflow position, controlling the access and visibility etc. This solution relies on the 
complexity of the technology to resolve these security, access, and visibility rights, with the 
removal of the files from the supporting technology sometimes be problematic. The 
advantage here is that all files, current and history exist in their original locations and 
therefore, security regarding file access along with no duplication.

4 Common Data Environment [aligned with ISO 19650] 
 
 
116 
 
 
Figure 30 State based approach to CDE Shared and Archive as defined in ISO 19650 
 
In the S tate based approach as shown in Figure 30, a new revision of the Drawing 1 file is 
shared into the same location as the previous revisions of Drawing 1. All reference links 
are automatically controlled, and the archive journal is updated with the authorisations and 
approvals that have been undertaken. The shared section includes the current version of 
Drawing 1 (P3) as well as all historical versions (P1 & P2)  
 
The use of folders allows the CDE approach to be carried out as a manual process, but the 
workflows are limited to the competence and diligence of the individuals undertaking the 
information management functions. The State based approach should ensure that 
information is not duplicated and allows all information to existing in a single repository.  
 
Depending upon the approach choice made, the solutions would need to be able to meet 
each of the specific functional requirement challenges common to the different stage 
workflows. Whilst for a single project, specific stage solution common approaches that 
each of these brings as well as dealing with the Functional Requirements of CDE  
 
The Functional Requirements of a CDE include:  
 
a. Data to be stored in a secure cloud-based or on-premises environment.  Appointing Party 
/ Client shall take note of the location of data centre that host the data when cyber 
security is a concern to a project , whether the data centre has to be or not necessary to 
be within the boundary of Hong Kong; 
b. Provide a user-customisable security access right control and management system;  
c. Provide a user-customisable sectional / categorisable structure;  
d. Provide a workflow for managing information process; including 
o Provide file version / revision control (Section 4.4.8 and 4.4.9 referred); 
o Provide file status codes to support suitability of use (Section 4.4.2 referred); 
o Provide file authorisation codes to support workflows for  (Section 4.4.3 and 4.4.4 
referred): 
 Check, Review and Approve process (Section 4.2.5 referred); 
 Review and Approval (Design review) process (Section 4.2.8 referred); 
 Review and Authorisation process (Section 4.2.8 referred); 
 Review and Accept process (Section 4.2.9 referred); 
e. Provide a user-customisable workflow for document submission and approval; 
f. Support uploading, downloading, Information Models  and documentation to facilitate 
retrieval of document attributes to support the CDE processes, including as a minimum – 
the document identifier (number), title, revision, version, and status codes (suitability); 
g. Support review, comment, and mark -up procedures for Information Models in the 
agreed proprietary and open file delivery formats and versions as documented in the 
BEP;

4 Common Data Environment [aligned with ISO 19650] 
 
117 
 
h. Support review, comment, and mark -up procedures for Documentation formats and 
versions as documented in the BIM Project Execution Plan; 
i. Allow access from portable devices and web applications; 
j. Contained encryption for data security; 
k. Provide sufficient capacity to store all files throughout the project stages and operate 
properly as requested by the Appointing Party / Client; 
l. Installed with anti -virus software and maintained with updated security patches by the 
operating system or environment that the CDE resides on.; 
m. Provide dashboards for presenting the BIM progress information to the different levels of 
users; 
n. Provide an issue tracking system, including the issue registration, logging, update, and 
email notification to the selected user account; 
o. Provide off-site backup of all project files including Information Models, documents and 
data; 
p. Provide a feature of project archive that all project files and information shall be archived 
in Appointing Party’s / Client’s preferred media and transferred to the Appointing Party / 
Client upon the completion of the design stage and construction stage respectively or as 
and when requested by the Appointing Party / Client  during the contract period (Section 
4.6 referred);  
q. Provide a full audit trail of the information stored in the CDE.  
 
 
Additional Functional requests may include:  
 
• Retrieving of the attributes and information from the Information Models  in an open 
format (not limited to .IFC) on the CDE; 
• Provide a feature of comparing Information Models from different versions / revisions and 
automated identification of differences; 
• Provide a feature of linkage between different Information Models , 2D drawings and 
project documents within the CDE; 
• Support the use and import of information delivery manuals (IDMs *) for identifying 
workflow requirements  in accordance to open BIM approach 
(*https://technical.buildingsmart.org/standards/information-delivery-manual/) ; and 
• Allow electronic signature (e-signature).
