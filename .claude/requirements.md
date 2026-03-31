# ATS-Friendly Resume Generator Platform

## Overview

This platform will generate an ATS (Applicant Tracking System) friendly resume based on user input, including personal details, work experience, and job description. It will match the job description with the user’s experience and generate a highly tailored, professional resume.

## Requirements

### 1. User Input: 
   The user will provide the following information:
   - **Personal Information:**
     - Contact Info: Email, Phone Number
     - Location
     - LinkedIn URL
     - Portfolio URL
     - GitHub URL
   - **Experience:**
     - Company Name
     - Company URL
     - Period of Employment
   - **Education:**
     - Details about the user’s education (Institution, Degree, Duration, etc.)

### 2. Job Description Input:
   The user will provide the detailed job description, which includes:
   - **Job Description:**
     - Company Name
     - Company URL
     - Responsibilities and requirements mentioned in the job description

### 3. Extracting Key Skills:
   - The platform should **analyze the job description** to extract technical skills, responsibilities, and other important requirements.
   - **Skills Matching:** 
     - The system should match the user’s experience with the skills and requirements from the job description.
     - Look for **specific technologies, methodologies**, and **soft skills** mentioned in the job description.

### 4. Professional Experience Generation:
   - For each company experience, the system will:
     - Use the extracted job description data to generate **professional experience bullet points**.
     - The bullets should match the **job description’s tone** and **requirements**, ensuring a high matching score.
     - **Bullet Count Rule:** The latest company experience should have the **most bullet points** (for example, if there are 3 companies, the bullets would be: 5, 3, 3). 
     - **Word Count:** Each bullet should contain between **25-30 words**, which translates to about **2 lines**.

### 5. Resume Format Generation:
   - **ATS-Friendly Resume:** 
     - Generate a professional and **ATS-compatible resume** in **DOC format**. 
     - The format should be simple and **structured** to ensure it is easily parsed by ATS.
   - You can **research and implement a solution** for generating DOC format files (using Python libraries or an external API).

### 6. Export and PDF Download:
   - **Export Functionality:**
     - Add a section that allows the user to **download the resume** as a **PDF**.
     - Ensure the PDF has a **unique name** for each download.
     - Implement the logic for **file export**, ensuring the downloaded PDF is well-formatted.

## Technical Stack

- **Frontend:** 
  - Vite + React
  - Responsive and modern UI with user-friendly forms to input data
  - Use React components to dynamically display the input fields and preview the resume

- **Backend:**
  - Python (FastAPI)
  - Handle the logic for processing user inputs, generating professional experience bullet points, extracting skills, and generating the resume
  - Use libraries or API calls to handle document generation and PDF creation (such as **python-docx** for DOC generation and **ReportLab** or **WeasyPrint** for PDF)

### Workflow

1. **User Input:** User enters personal details, job description, and experience data.
2. **Skills Extraction:** The system parses the job description to extract key technical skills and job requirements.
3. **Experience Matching:** The system generates professional experience bullets based on the input data and job description.
4. **Resume Generation:** The resume is generated in DOC format, with all the user’s information and tailored job experience.
5. **Export as PDF:** Once the resume is generated, the user can export it as a PDF with a unique name.

### Resume Structure (in order)
1. Summary/Profile
2. Skills (grouped by category)
3. Work Experience
4. Education

### Resume Typography
- Font size for name: 28pt (Noto Sans, color #1F4E79)
- Font size for title: 14pt (Noto Sans, e.g., "Senior Software Engineer")
- Font size for contact/URLs: 10pt (Verdana)
- Font size for section headers: 16pt (Noto Sans, ALL CAPS, #1F4E79, bottom border)
- Font size for content: 10.5pt
- Font size for company period: 11pt (Noto Sans, #595959)
- Font size for company name and role: 12pt (Merriweather, bold)
- Page margins: 0.5" all sides

### Style Reference
- See `.claude/resume-style.md` for complete styling extracted from sample resume
- Sample resume: `/Users/crm/Downloads/David Gabriel.docx`

### AI Integration
- Use Claude API for skills extraction, experience matching, and bullet point generation
- Frontend: Tailwind CSS for styling
- No auth required, session-based only

### Conclusion

This platform will be designed to help users easily create ATS-friendly resumes that match the job descriptions they are applying for, ensuring a high matching score and professional presentation.