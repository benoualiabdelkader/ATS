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
        """Converts Markdown content into a clean, professional ATS-friendly PDF file."""
        if not HAS_REPORTLAB:
            # Fallback placeholder if reportlab is missing
            output_pdf_path.write_bytes(b"%PDF-1.4 PDF export requires reportlab package.")
            return

        doc = SimpleDocTemplate(
            str(output_pdf_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Custom styles
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=4
        )

        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=2
        )

        h2_style = ParagraphStyle(
            'CustomH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor('#1e3a8a'),
            spaceBefore=8,
            spaceAfter=4,
            textTransform='uppercase'
        )

        bullet_style = ParagraphStyle(
            'CustomBullet',
            parent=body_style,
            leftIndent=12,
            bulletIndent=4,
            spaceAfter=3
        )

        story = []

        lines = md_content.splitlines()
        for line in lines:
            line_str = line.strip()
            # Replace unicode dashes with safe ASCII hyphens for PDF font encoding
            line_str = line_str.replace("–", "-").replace("—", " - ")

            if not line_str:
                story.append(Spacer(1, 3))
                continue

            if line_str.startswith("# "):
                text = line_str[2:].strip()
                story.append(Paragraph(text, title_style))
                story.append(Spacer(1, 2))
            elif line_str.startswith("## "):
                text = line_str[3:].strip()
                story.append(Spacer(1, 4))
                story.append(Paragraph(text, h2_style))
                story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#3b82f6'), spaceBefore=1, spaceAfter=4))
            elif line_str.startswith("### "):
                text = line_str[4:].strip()
                p_text = f"<b>{text}</b>"
                story.append(Paragraph(p_text, body_style))
            elif line_str.startswith("- ") or line_str.startswith("* "):
                raw_text = line_str[2:].strip()
                # Format bold text
                formatted_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", raw_text)
                formatted_text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", formatted_text)
                story.append(Paragraph(f"• {formatted_text}", bullet_style))
            elif line_str.startswith("---"):
                story.append(Spacer(1, 4))
            else:
                formatted_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line_str)
                formatted_text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", formatted_text)
                formatted_text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2" color="#2563eb">\1</a>', formatted_text)
        doc.build(story)

    def export_tex_to_pdf(self, tex_content: str, output_pdf_path: Path) -> bool:
        """Compiles LaTeX source code into native text-embedded PDF using pdflatex."""
        import subprocess
        import shutil

        pdflatex_cmd = shutil.which("pdflatex")
        target_dir = output_pdf_path.parent
        tex_file = target_dir / (output_pdf_path.stem + ".tex")
        tex_file.write_text(tex_content, encoding="utf-8")

        if pdflatex_cmd:
            try:
                subprocess.run(
                    [pdflatex_cmd, "-interaction=nonstopmode", f"-output-directory={target_dir}", str(tex_file)],
                    cwd=str(target_dir),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=30
                )
                # Cleanup temp TeX build artifacts
                for ext in [".aux", ".log", ".out"]:
                    temp_artifact = target_dir / (output_pdf_path.stem + ext)
                    if temp_artifact.exists():
                        temp_artifact.unlink()
                return True
            except Exception as e:
                print(f"[Warning] pdflatex compilation failed: {e}")

        # Fallback to ReportLab if pdflatex execution fails
        self.export_md_to_pdf(tex_content, output_pdf_path)
        return False

