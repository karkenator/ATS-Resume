# ATS Resume Style Reference

Extracted from sample: `David Gabriel.docx`

## Page Layout
- Page size: 8.5" x 11" (US Letter)
- Margins: 0.5" all sides (top, bottom, left, right)

## Resume Structure (in order)
1. **Name** (Title style)
2. **Job Title** (Subtitle style) — e.g., "Senior Software Engineer | Senior .NET Engineer"
3. **Contact Info** (Contact style) — phone, email, LinkedIn, GitHub (tab-separated)
4. **Profile/Summary** (Heading 1 + Normal)
5. **Skills** (Heading 1 + Heading 2 subcategories + Normal lists)
6. **Work Experience** (Heading 1 + entries)
7. **Education** (Heading 1 + entries)

## Typography

### Title (Name)
- Font: **Noto Sans**, 28pt
- Color: `#1F4E79`
- Line spacing: 1.0
- Spacing after: 12pt (152400 EMU)

### Subtitle (Job Title)
- Font: **Noto Sans**, 14pt
- Color: `#5A5A5A`
- Spacing after: 12pt

### Contact
- Font: **Verdana**, 10pt
- Spacing after: 8pt (101600 EMU)
- Tab-separated values (email | phone | LinkedIn | GitHub)

### Heading 1 (Section Headers: PROFILE, SKILLS, WORK EXPERIENCE, EDUCATION)
- Font: **Noto Sans**, 16pt
- Color: `#1F4E79`
- ALL CAPS (caps property enabled)
- Bottom border: single line, 6/8pt, color `#1F4E79`
- Spacing before: 12pt (240 twentieths = 152400 EMU)
- Keep with next: true

### Heading 2 (Company Name + Role / Skill Category)
- Font: **Merriweather**, 12pt
- Bold: true
- Spacing before: 8pt (101600 EMU)
- Spacing after: 0

### Heading 3 (Period + Location)
- Font: **Noto Sans**, 11pt
- Color: `#595959`
- Spacing before: 2pt (25400 EMU)
- Spacing after: 2pt (25400 EMU)

### Normal (Body text / Skill lists / Profile paragraph)
- Font: inherits theme (default), 10.5pt
- Spacing after: 4pt (50800 EMU)
- Skills in profile paragraph: **bold** for keyword emphasis

### List Paragraph (Bullet points under Work Experience)
- Inherits Normal style (10.5pt)
- Left indent: 720 twips (0.5")
- Bulleted list
- Each bullet: 25-30 words (~2 lines)

## Color Palette
| Usage | Hex | Description |
|-------|-----|-------------|
| Name / Section headers | `#1F4E79` | Dark blue |
| Subtitle | `#5A5A5A` | Medium gray |
| Period/Location | `#595959` | Medium gray |
| Body text | Default (black) | Standard |

## Bullet Point Rules
- Latest/most recent company: most bullet points (e.g., 18 for primary role)
- Subsequent companies: fewer bullets (e.g., 11, 9, 9)
- Each bullet starts with a strong action verb
- Each bullet: 25-30 words
- Keywords from job description are matched and incorporated

## Skills Section Structure
Skills grouped by category using Heading 2:
- Programming Languages
- Technology-specific groups (e.g., "C/C++ & C#", "JavaScript & TypeScript & UI")
- Database
- Cloud Platforms
- Others
- Soft Skills

Each category lists comma-separated technologies as Normal text.
