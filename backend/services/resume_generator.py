"""
Resume generator using python-docx for DOCX and fpdf2 for PDF.
Style reference: .claude/resume-style.md
"""

import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from fpdf import FPDF

from models import GenerateResumeResponse, BulletPoint

FONTS_DIR = Path(__file__).parent.parent / "fonts"


# Color constants
DARK_BLUE = RGBColor(0x1F, 0x4E, 0x79)
MEDIUM_GRAY = RGBColor(0x5A, 0x5A, 0x5A)
PERIOD_GRAY = RGBColor(0x59, 0x59, 0x59)


def _set_paragraph_spacing(paragraph, before=None, after=None, line=None):
    pf = paragraph.paragraph_format
    if before is not None:
        pf.space_before = Pt(before)
    if after is not None:
        pf.space_after = Pt(after)
    if line is not None:
        pf.line_spacing = line


def _add_bottom_border(paragraph, color="1F4E79"):
    """Add a bottom border to a paragraph (for section headers)."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="1" w:color="{color}"/>'
        f"</w:pBdr>"
    )
    pPr.append(pBdr)


def _set_font(run, name, size, bold=False, color=None, italic=False, caps=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    if caps:
        run.font.all_caps = True


def _add_name(doc, name):
    """Add name as Title style - 28pt Noto Sans, dark blue."""
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, after=2, line=1.0)
    run = p.add_run(name)
    _set_font(run, "Noto Sans", 28, color=DARK_BLUE)


def _add_title(doc, title):
    """Add job title as Subtitle - 14pt Noto Sans, gray."""
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before=0, after=6)
    run = p.add_run(title)
    _set_font(run, "Noto Sans", 14, color=MEDIUM_GRAY)


def _add_contact(doc, personal_info):
    """Add contact info - 10pt Verdana, tab-separated."""
    parts = []
    if personal_info.email:
        parts.append(personal_info.email)
    if personal_info.phone:
        parts.append(personal_info.phone)
    if personal_info.location:
        parts.append(personal_info.location)

    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before=0, after=2)
    run = p.add_run("  |  ".join(parts))
    _set_font(run, "Verdana", 10)

    # URLs on next line
    urls = []
    if personal_info.linkedin_url:
        urls.append(personal_info.linkedin_url)
    if personal_info.github_url:
        urls.append(personal_info.github_url)
    if personal_info.portfolio_url:
        urls.append(personal_info.portfolio_url)

    if urls:
        p2 = doc.add_paragraph()
        _set_paragraph_spacing(p2, before=0, after=4)
        run2 = p2.add_run("  |  ".join(urls))
        _set_font(run2, "Verdana", 10)


def _add_section_header(doc, title):
    """Add section header - 16pt Noto Sans, dark blue, ALL CAPS, bottom border."""
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before=12, after=4)
    run = p.add_run(title.upper())
    _set_font(run, "Noto Sans", 16, color=DARK_BLUE, caps=True)
    _add_bottom_border(p)
    # Keep with next
    pPr = p._p.get_or_add_pPr()
    pPr.append(parse_xml(f'<w:keepNext {nsdecls("w")}/>'))
    return p


def _add_summary(doc, summary_text):
    """Add profile/summary section with bold keywords."""
    _add_section_header(doc, "Profile")
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, after=4)
    # Parse **bold** markers from summary
    _add_text_with_bold(p, summary_text, font_name="Noto Sans", font_size=10.5)


def _add_text_with_bold(paragraph, text, font_name="Noto Sans", font_size=10.5):
    """Parse text with **bold** markers and add runs accordingly."""
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            _set_font(run, font_name, font_size, bold=True)
        else:
            run = paragraph.add_run(part)
            _set_font(run, font_name, font_size)


def _add_skills(doc, skills):
    """Add skills section with categories."""
    _add_section_header(doc, "Skills")
    for category, skill_list in skills.items():
        # Category heading - Heading 2 style
        p_cat = doc.add_paragraph()
        _set_paragraph_spacing(p_cat, before=4, after=0)
        run = p_cat.add_run(category)
        _set_font(run, "Merriweather", 12, bold=True)

        # Skills list
        p_skills = doc.add_paragraph()
        _set_paragraph_spacing(p_skills, before=0, after=2)
        run = p_skills.add_run(", ".join(skill_list))
        _set_font(run, "Noto Sans", 10.5)


def _add_experience(doc, experiences):
    """Add work experience section."""
    _add_section_header(doc, "Work Experience")
    for exp in experiences:
        # Company and role - Heading 2
        p_company = doc.add_paragraph()
        _set_paragraph_spacing(p_company, before=8, after=0)
        run = p_company.add_run(f"{exp.role}, {exp.company_name}")
        _set_font(run, "Merriweather", 12, bold=True)

        # Period and location - Heading 3
        p_period = doc.add_paragraph()
        _set_paragraph_spacing(p_period, before=2, after=2)
        run = p_period.add_run(f"{exp.period} | {exp.location}")
        _set_font(run, "Noto Sans", 11, color=PERIOD_GRAY)

        # Bullet points
        for bullet in exp.bullets:
            _add_bullet_point(doc, bullet)


def _add_bullet_point(doc, bullet: BulletPoint):
    """Add a bulleted list item with bold keywords."""
    p = doc.add_paragraph()
    _set_paragraph_spacing(p, before=0, after=2)

    # Set list bullet formatting
    pPr = p._p.get_or_add_pPr()
    # Add indent for bullet
    ind = parse_xml(f'<w:ind {nsdecls("w")} w:left="720" w:hanging="360"/>')
    pPr.append(ind)

    # Add bullet character
    numPr = parse_xml(
        f'<w:numPr {nsdecls("w")}>'
        f'  <w:ilvl w:val="0"/>'
        f'  <w:numId w:val="1"/>'
        f"</w:numPr>"
    )
    pPr.append(numPr)

    # Add text with bold keywords
    if bullet.bold_keywords:
        text = bullet.text
        # Build a regex to match any bold keyword
        keywords_sorted = sorted(bullet.bold_keywords, key=len, reverse=True)
        pattern = "|".join(re.escape(kw) for kw in keywords_sorted)
        parts = re.split(f"({pattern})", text, flags=re.IGNORECASE)

        for part in parts:
            if any(part.lower() == kw.lower() for kw in bullet.bold_keywords):
                run = p.add_run(part)
                _set_font(run, "Noto Sans", 10.5, bold=True)
            else:
                run = p.add_run(part)
                _set_font(run, "Noto Sans", 10.5)
    else:
        run = p.add_run(bullet.text)
        _set_font(run, "Noto Sans", 10.5)


def _add_education(doc, education_list):
    """Add education section."""
    _add_section_header(doc, "Education")
    for edu in education_list:
        # Degree and institution - Heading 2
        p_edu = doc.add_paragraph()
        _set_paragraph_spacing(p_edu, before=8, after=0)
        run = p_edu.add_run(f"{edu.degree}, {edu.institution}")
        _set_font(run, "Merriweather", 12, bold=True)

        # Period and location - Heading 3
        p_period = doc.add_paragraph()
        _set_paragraph_spacing(p_period, before=2, after=2)
        run = p_period.add_run(f"{edu.start_date} – {edu.end_date} | {edu.location}")
        _set_font(run, "Noto Sans", 11, color=PERIOD_GRAY)

        if edu.description:
            p_desc = doc.add_paragraph()
            _set_paragraph_spacing(p_desc, after=4)
            run = p_desc.add_run(edu.description)
            _set_font(run, "Noto Sans", 10.5)


def _setup_numbering(doc):
    """Set up bullet list numbering in the document."""
    numbering_part = doc.part.numbering_part
    # Access the numbering XML and add a bullet list definition
    numbering_xml = numbering_part._element

    # Add abstract numbering for bullets
    abstract_num = parse_xml(
        f'<w:abstractNum {nsdecls("w")} w:abstractNumId="0">'
        f'  <w:lvl w:ilvl="0">'
        f'    <w:start w:val="1"/>'
        f'    <w:numFmt w:val="bullet"/>'
        f'    <w:lvlText w:val="\u2022"/>'
        f'    <w:lvlJc w:val="left"/>'
        f"    <w:pPr>"
        f'      <w:ind w:left="720" w:hanging="360"/>'
        f"    </w:pPr>"
        f"    <w:rPr>"
        f'      <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/>'
        f"    </w:rPr>"
        f"  </w:lvl>"
        f"</w:abstractNum>"
    )
    numbering_xml.append(abstract_num)

    num = parse_xml(
        f'<w:num {nsdecls("w")} w:numId="1">'
        f'  <w:abstractNumId w:val="0"/>'
        f"</w:num>"
    )
    numbering_xml.append(num)


def generate_docx(resume_data: GenerateResumeResponse, output_path: Path):
    """Generate a DOCX resume matching the sample style."""
    doc = Document()

    # Set page margins to 0.5" all sides
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    # Setup bullet numbering
    _setup_numbering(doc)

    # Build resume sections
    pi = resume_data.personal_info
    _add_name(doc, pi.full_name)
    _add_title(doc, pi.title)
    _add_contact(doc, pi)
    _add_summary(doc, resume_data.summary)
    _add_skills(doc, resume_data.skills)
    _add_experience(doc, resume_data.experiences)
    _add_education(doc, resume_data.education)

    doc.save(str(output_path))


class ResumePDF(FPDF):
    """Custom PDF class for resume generation."""

    def __init__(self):
        super().__init__(format="letter")
        self.set_margins(12.7, 12.7, 12.7)  # 0.5 inch = 12.7mm
        self.set_auto_page_break(auto=True, margin=12.7)
        # Register Noto Sans font (static builds)
        regular_path = str(FONTS_DIR / "NotoSans-Regular.ttf")
        bold_path = str(FONTS_DIR / "NotoSans-Bold.ttf")
        self.add_font("NotoSans", "", regular_path)
        self.add_font("NotoSans", "B", bold_path)
        self.add_font("NotoSans", "I", regular_path)
        self.add_font("NotoSans", "BI", bold_path)

    def _pdf_text_with_bold_keywords(self, text, keywords, font_name="NotoSans", font_size=10.5):
        """Write text with bold keywords inline."""
        if not keywords:
            self.set_font(font_name, "", font_size)
            self.write(5, text)
            return
        keywords_sorted = sorted(keywords, key=len, reverse=True)
        pattern = "|".join(re.escape(kw) for kw in keywords_sorted)
        parts = re.split(f"({pattern})", text, flags=re.IGNORECASE)
        for part in parts:
            if any(part.lower() == kw.lower() for kw in keywords):
                self.set_font(font_name, "B", font_size)
                self.write(5, part)
            else:
                self.set_font(font_name, "", font_size)
                self.write(5, part)

    def _pdf_text_with_markdown_bold(self, text, font_name="NotoSans", font_size=10.5):
        """Write text with **bold** markers rendered as bold."""
        parts = re.split(r"(\*\*[^*]+\*\*)", text)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                self.set_font(font_name, "B", font_size)
                self.write(5, part[2:-2])
            else:
                self.set_font(font_name, "", font_size)
                self.write(5, part)


def generate_pdf(resume_data: GenerateResumeResponse, output_path: Path):
    """Generate a PDF resume using fpdf2."""
    pdf = ResumePDF()
    pdf.add_page()
    pi = resume_data.personal_info

    # Name - 28pt dark blue
    pdf.set_font("NotoSans", "", 28)
    pdf.set_text_color(0x1F, 0x4E, 0x79)
    pdf.cell(0, 12, pi.full_name, new_x="LMARGIN", new_y="NEXT")

    # Title - 14pt gray
    pdf.set_font("NotoSans", "", 14)
    pdf.set_text_color(0x5A, 0x5A, 0x5A)
    pdf.cell(0, 7, pi.title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Contact - 10pt
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    contact_parts = [p for p in [pi.email, pi.phone, pi.location] if p]
    pdf.cell(0, 5, "  |  ".join(contact_parts), new_x="LMARGIN", new_y="NEXT")

    url_parts = [p for p in [pi.linkedin_url, pi.github_url, pi.portfolio_url] if p]
    if url_parts:
        pdf.cell(0, 5, "  |  ".join(url_parts), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # --- PROFILE ---
    _pdf_section_header(pdf, "PROFILE")
    pdf.set_font("NotoSans", "", 10.5)
    pdf.set_text_color(0, 0, 0)
    pdf._pdf_text_with_markdown_bold(resume_data.summary)
    pdf.ln(6)

    # --- SKILLS ---
    _pdf_section_header(pdf, "SKILLS")
    for category, skill_list in resume_data.skills.items():
        pdf.set_font("NotoSans", "B", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, category, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("NotoSans", "", 10.5)
        pdf.multi_cell(0, 5, ", ".join(skill_list))
        pdf.ln(1)

    # --- WORK EXPERIENCE ---
    _pdf_section_header(pdf, "WORK EXPERIENCE")
    for exp in resume_data.experiences:
        # Company + role
        pdf.set_font("NotoSans", "B", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, f"{exp.role}, {exp.company_name}", new_x="LMARGIN", new_y="NEXT")

        # Period + location
        pdf.set_font("NotoSans", "", 11)
        pdf.set_text_color(0x59, 0x59, 0x59)
        pdf.cell(0, 6, f"{exp.period} | {exp.location}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        # Bullets
        pdf.set_text_color(0, 0, 0)
        for bullet in exp.bullets:
            bullet_x = pdf.l_margin
            pdf.set_x(bullet_x)
            pdf.set_font("NotoSans", "", 10.5)
            pdf.cell(4, 4.5, "\u2022")
            text_x = bullet_x + 6
            pdf.set_x(text_x)
            text_w = pdf.w - pdf.r_margin - text_x
            _pdf_write_with_bold_keywords(pdf, bullet.text, bullet.bold_keywords, text_x, text_w)
            pdf.ln(1)
        pdf.ln(2)

    # --- EDUCATION ---
    _pdf_section_header(pdf, "EDUCATION")
    for edu in resume_data.education:
        pdf.set_font("NotoSans", "B", 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, f"{edu.degree}, {edu.institution}", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("NotoSans", "", 11)
        pdf.set_text_color(0x59, 0x59, 0x59)
        pdf.cell(0, 6, f"{edu.start_date} \u2013 {edu.end_date} | {edu.location}", new_x="LMARGIN", new_y="NEXT")

        if edu.description:
            pdf.set_font("NotoSans", "", 10.5)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 5, edu.description)
        pdf.ln(2)

    pdf.output(str(output_path))


def _pdf_section_header(pdf, title):
    """Draw a section header with bottom border."""
    pdf.set_font("NotoSans", "", 16)
    pdf.set_text_color(0x1F, 0x4E, 0x79)
    y_before = pdf.get_y()
    pdf.cell(0, 9, title, new_x="LMARGIN", new_y="NEXT")
    # Draw bottom border line
    pdf.set_draw_color(0x1F, 0x4E, 0x79)
    pdf.set_line_width(0.5)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(3)


def _pdf_write_with_bold_keywords(pdf, text, keywords, indent_x, width):
    """Write bullet text with bold keywords, handling line wrapping."""
    if not keywords:
        pdf.set_font("NotoSans", "", 10.5)
        pdf.multi_cell(width, 4.5, text)
        return

    keywords_sorted = sorted(keywords, key=len, reverse=True)
    pattern = "|".join(re.escape(kw) for kw in keywords_sorted)
    parts = re.split(f"({pattern})", text, flags=re.IGNORECASE)

    kw_lower = {kw.lower() for kw in keywords}
    for part in parts:
        if not part:
            continue
        is_bold = part.lower() in kw_lower
        pdf.set_font("NotoSans", "B" if is_bold else "", 10.5)
        # write() handles line wrapping automatically
        pdf.write(4.5, part)
    pdf.ln()
