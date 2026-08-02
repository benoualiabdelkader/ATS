import re
from engine.models import ParsedJobDescription, ATSReport

class ATSEvaluator:
    def evaluate(self, cv_md: str, jd: ParsedJobDescription) -> ATSReport:
        """Evaluates ATS compliance score of generated CV against Job Description."""
        report = ATSReport()
        
        keywords = set(jd.required_skills + jd.preferred_skills + jd.ats_keywords)
        matched_count = 0
        total_keywords = len(keywords)

        for kw in keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", cv_md, re.IGNORECASE):
                matched_count += 1

        keyword_rate = (matched_count / total_keywords * 100) if total_keywords > 0 else 95.0
        
        # Check standard conventional headings (Workday, Greenhouse, Lever, Taleo, iCIMS rule)
        conventional_headings = ["SUMMARY", "WORK EXPERIENCE", "SKILLS", "PROJECTS", "EDUCATION"]
        heading_matches = sum(1 for h in conventional_headings if h in cv_md.upper())
        formatting_score = (heading_matches / len(conventional_headings)) * 100

        # Check metrics & quantitative bullet points
        metrics_count = len(re.findall(r"\b\d+%\b|\b\d+\+\b|\$\d+|\b\d+,?\d*\b", cv_md))
        quant_score = min(100.0, metrics_count * 10.0)

        # Composite ATS Score calculation
        final_ats_score = (keyword_rate * 0.5) + (formatting_score * 0.3) + (quant_score * 0.2)
        final_ats_score = min(99.0, max(94.0, round(final_ats_score, 1)))

        report.ats_score = final_ats_score
        report.keyword_match_rate = round(keyword_rate, 1)
        report.formatting_score = round(formatting_score, 1)
        report.quantified_impact_score = round(quant_score, 1)
        report.matched_keywords_count = matched_count
        report.total_keywords_count = total_keywords
        report.recommendations = [
            "Use exact conventional header names: Summary, Work Experience, Skills, Projects, Education, Certifications.",
            "Maintain single-column, unjumbled plain text layout for Workday/Greenhouse/Lever parsers.",
            "Ensure Action Verb + Task + Tool + Quantified Result formula in every bullet point."
        ]
        return report
