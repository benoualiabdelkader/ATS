from pathlib import Path
import re

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

class PDFExporter:
    def export_md_to_pdf(self, md_content: str, output_pdf_path: Path):
        """Converts Markdown content into an ATS-optimized PDF matching templete.txt LaTeX styling."""
        if not HAS_REPORTLAB:
            output_pdf_path.write_bytes(b"%PDF-1.4 PDF export requires reportlab package.")
            return

        # Exact margins from templete.txt (0.6in top/bottom = 43.2pt, 0.75in left/right = 54pt)
        doc = SimpleDocTemplate(
            str(output_pdf_path),
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=43.2,
            bottomMargin=43.2
        )

        styles = getSampleStyleSheet()
        
        # Times-Roman styling matching LaTeX mathptmx font in templete.txt
        body_style = ParagraphStyle(
            'LaTeXBody',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=9.5,
            leading=12.5,
            textColor=colors.black,
            spaceAfter=2
        )

        title_style = ParagraphStyle(
            'LaTeXTitle',
            parent=styles['Heading1'],
            fontName='Times-Bold',
            fontSize=18,
            leading=22,
            alignment=1, # Center
            textColor=colors.black,
            spaceAfter=2
        )

        subtitle_style = ParagraphStyle(
            'LaTeXSubtitle',
            parent=body_style,
            fontName='Times-Roman',
            fontSize=10.5,
            leading=13.5,
            alignment=1, # Center
            textColor=colors.black,
            spaceAfter=2
        )

        contact_style = ParagraphStyle(
            'LaTeXContact',
            parent=body_style,
            fontName='Times-Roman',
            fontSize=9,
            leading=12,
            alignment=1, # Center
            textColor=colors.black,
            spaceAfter=6
        )

        h2_style = ParagraphStyle(
            'LaTeXSection',
            parent=styles['Heading2'],
            fontName='Times-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.black,
            spaceBefore=8,
            spaceAfter=2
        )

        entry_style = ParagraphStyle(
            'LaTeXEntry',
            parent=body_style,
            fontName='Times-Bold',
            fontSize=9.5,
            leading=12.5,
            spaceBefore=3,
            spaceAfter=1
        )

        bullet_style = ParagraphStyle(
            'LaTeXBullet',
            parent=body_style,
            leftIndent=14,
            bulletIndent=4,
            spaceAfter=1.5
        )

        story = []
        lines = md_content.splitlines()
        
        header_parsed = False
        is_first_h1 = True

        for i, line in enumerate(lines):
            line_str = line.strip()
            line_str = line_str.replace("–", "--").replace("—", "---")

            if not line_str:
                continue

            if line_str.startswith("# ") and is_first_h1:
                is_first_h1 = False
                name_text = line_str[2:].strip().upper()
                story.append(Paragraph(name_text, title_style))
                
                # Check for sub-header lines (Role & Contact)
                if i + 1 < len(lines) and not lines[i+1].strip().startswith("##") and not lines[i+1].strip().startswith("---"):
                    next_line = lines[i+1].strip()
                    if next_line.startswith("**") and next_line.endswith("**"):
                        role_text = next_line.strip("*").strip()
                        story.append(Paragraph(role_text, subtitle_style))
                    else:
                        story.append(Paragraph(next_line, subtitle_style))
                
                if i + 2 < len(lines) and not lines[i+2].strip().startswith("##") and not lines[i+2].strip().startswith("---"):
                    contact_line = lines[i+2].strip()
                    if "|" in contact_line:
                        formatted_contact = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2" color="#000000"><u>\1</u></a>', contact_line)
                        story.append(Paragraph(formatted_contact, contact_style))
                header_parsed = True
                story.append(Spacer(1, 4))
                continue

            # Skip header lines that were processed above
            if header_parsed and i <= 3 and not line_str.startswith("##") and not line_str.startswith("---") and not line_str.startswith("#"):
                continue

            if line_str.startswith("## "):
                section_title = line_str[3:].strip().upper()
                story.append(Spacer(1, 4))
                story.append(Paragraph(section_title, h2_style))
                story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceBefore=1, spaceAfter=4))
            elif line_str.startswith("### "):
                entry_title = line_str[4:].strip()
                formatted_entry = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", entry_title)
                formatted_entry = re.sub(r"\*(.*?)\*", r"<i>\1</i>", formatted_entry)
                story.append(Paragraph(formatted_entry, entry_style))
            elif line_str.startswith("- ") or line_str.startswith("* "):
                raw_text = line_str[2:].strip()
                formatted_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", raw_text)
                formatted_text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", formatted_text)
                story.append(Paragraph(f"• {formatted_text}", bullet_style))
            elif line_str.startswith("---"):
                continue
            else:
                formatted_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line_str)
                formatted_text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", formatted_text)
                formatted_text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2" color="#000000"><u>\1</u></a>', formatted_text)
                story.append(Paragraph(formatted_text, body_style))

        doc.build(story)

    def export_tex_to_pdf(self, tex_content: str, output_pdf_path: Path) -> bool:
        """Compiles LaTeX source code into native text-embedded PDF if pdflatex is present."""
        import subprocess
        import shutil

        pdflatex_cmd = shutil.which("pdflatex")
        if pdflatex_cmd:
            target_dir = output_pdf_path.parent
            tex_file = target_dir / (output_pdf_path.stem + ".tex")
            tex_file.write_text(tex_content, encoding="utf-8")
            try:
                subprocess.run(
                    [pdflatex_cmd, "-interaction=nonstopmode", f"-output-directory={target_dir}", str(tex_file)],
                    cwd=str(target_dir),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=30
                )
                for ext in [".aux", ".log", ".out"]:
                    temp_artifact = target_dir / (output_pdf_path.stem + ext)
                    if temp_artifact.exists():
                        temp_artifact.unlink()
                return True
            except Exception as e:
                print(f"[Warning] pdflatex compilation failed: {e}")

        return False
