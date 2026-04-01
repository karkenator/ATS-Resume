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
     - Use the extracted job description data to generate **project-based professional experience bullet points**.
     - **Each bullet must describe a specific, concrete project or initiative** — NOT generic responsibilities.
     - **Bullet Pattern:** [Action verb] + [specific system/project] + [using technologies] + [to solve problem] + [measurable result]
     - The bullets should match the **job description’s tone** and **requirements**, ensuring a high matching score.
     - **Bullet Count Rule:** The first (most recent) company gets a **dynamic bullet count** to fill remaining space on page 1 (typically 4-8). Subsequent companies get **5–8 bullets** each.
     - **Word Count:** Each bullet should contain between **25-30 words**, which translates to about **2 lines**.
     - **Example bullets:**
       - "Led the migration of legacy .NET Framework 4.8 services to .NET 8 to resolve performance bottlenecks and reduce technical debt by 35%."
       - "Built a Kafka-based event streaming architecture using Java and Spring Boot to replace polling mechanisms, boosting real-time data throughput by 60%."
       - "Created Python-based ETL pipelines using Airflow and Pandas to replace slow SQL Server jobs, cutting nightly data sync duration from 4 hours to 45 minutes."

### Master Skills List

A comprehensive skills catalog is stored in `backend/data/master_skills.json` with categories: Programming Languages, C/C++ & C#, JavaScript & TypeScript, Java & PHP, Python/Go/Ruby, AI & Machine Learning, Database, Cloud Platforms, Others, Soft Skills.

**Skill selection logic** (in `ai_service.py`):
1. Analyze the job description to extract required skills
2. Match extracted skills against the master list and select relevant ones per category
3. **Always include:** JavaScript & TypeScript frameworks + Python/Go/Ruby frameworks (full categories)
4. **AI & Machine Learning:** Full category if job is AI-focused, minimal subset (RAG, LangChain, Prompt Engineering, LLMs, OpenAI) if not
5. **Other categories:** Only skills that match the job description

### 2-Page Layout Requirement

The resume must be exactly 2 pages:
- **Page 1:** Name, Title, Contact, Profile/Summary, Skills, Work Experience header + first (most recent) company with dynamic bullet count (fills remaining page space)
- **Page 2:** Remaining work experiences (5–8 bullets each) + Education

The first experience bullet count is calculated dynamically based on how much vertical space the skills section uses. A hard page break is inserted after the first experience only.

### Font Requirement

Use the most readable, ATS-friendly font:
- **DOCX:** Calibri (universally available in Word, modern sans-serif)
- **PDF:** Helvetica (built-in to ReportLab, visually similar to Calibri/Arial)

All text uses a single font family — no mixing of Noto Sans, Merriweather, Verdana, etc.

### Real-World Experience Requirement

All generated bullet points must describe realistic, hands-on engineering work — specific projects, migrations, system builds, pipeline deployments, infrastructure automation, and API integrations. No generic responsibilities or theoretical language. Every bullet should read as a completed achievement with tangible, measurable impact.

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
- **Font family: Calibri** (DOCX) / **Helvetica** (PDF) — single font throughout
- Font size for name: 28pt (Calibri, color #1F4E79)
- Font size for title: 14pt (Calibri, e.g., "Senior Software Engineer")
- Font size for contact/URLs: 10pt (Calibri)
- Font size for section headers: 16pt (Calibri, ALL CAPS, #1F4E79, bottom border)
- Font size for content: 10.5pt (Calibri)
- Font size for company period: 11pt (Calibri, #595959)
- Font size for company name and role: 12pt (Calibri, bold)
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