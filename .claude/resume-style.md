# ATS Resume Style Reference

## Page Layout
- Page size: 8.5" x 11" (US Letter)
- Margins: 0.5" all sides
- **Total: 2 pages**

## Page Layout Structure (2 Pages)
- **Page 1:** Name, Title, Contact, Profile, Skills, Work Experience header + first company (dynamic bullet count fills page)
- **Page 2:** Remaining experiences (8-10 bullets each to fill page) + Education
- Hard page break after first experience only

## Typography

**Single font:** Calibri (DOCX) / Helvetica (PDF)

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Name | 28pt | Normal | `#1F4E79` |
| Job Title | 14pt | Normal | `#5A5A5A` |
| Contact / URLs | 10pt | Normal | Black |
| Section Headers | 16pt | Bold, ALL CAPS | `#1F4E79` |
| Company + Role | 12pt | Bold | Black |
| Period + Location | 11pt | Normal | `#595959` |
| Skills (per line) | 10.5pt | Category bold, skills normal | Black |
| Body / Summary | 10.5pt | Normal | Black |
| Bullet Points | 10.5pt | Normal (keywords bold) | Black |

## Section Header Style
- 16pt Bold, ALL CAPS, `#1F4E79`
- Bottom border: thin line, color `#1F4E79`
- Spacing before: 6pt, after: 2pt
- Keep with next: true

## Skills Section Format
Compact — one line per category, wrapping as needed:
```
**Programming Languages:** JavaScript, TypeScript, Python, GraphQL, HTML5, CSS3
**JavaScript & TypeScript:** React, Redux, Node.js, Express.js, Next.js, Jest, Tailwind CSS
**AI & Machine Learning:** RAG, LangChain, Prompt Engineering, Large Language Models, OpenAI
```

Skills selected from `backend/data/master_skills.json`:
- **Programming Languages:** always JS, TS, Python, HTML5, CSS3 + job-matched
- **JS/TS:** core frameworks (React, Redux, Node.js, Express.js, Next.js, Jest, Bootstrap, Tailwind CSS, jQuery) + job-matched
- **Python:** core frameworks (Flask, Django, FastAPI, Pytest) + job-matched
- **AI:** full category if AI-focused job, minimal (RAG, LangChain, Prompt Engineering, LLMs, OpenAI) otherwise
- **All others:** only job-matched skills from master list

## Bullet Point Rules
- First company: **dynamic count** (fills remainder of page 1, typically 8-12)
- Subsequent companies: **7-10 bullets** each (fills page 2)
- Each bullet: 25-30 words (~2 lines)
- Strong action verb start, distinct projects, real-world hands-on work
- Keywords from job description bolded
- Even older companies should weave in modern tech context

## Bullet Indent
- Left indent: 360 twips (0.5"), hanging: 180 twips
- Bullet character: Unicode bullet (U+2022), Calibri font

## Spacing Guidelines (tight to fit 2 pages)
- Minimize all spacing — 0-2pt between elements
- Section headers: 6pt before, 2pt after
- Bullets: 0pt before, 0pt after
- Company heading: 4pt before
- No large gaps anywhere
