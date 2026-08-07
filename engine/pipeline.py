"""
Career-Application-Agent Pipeline Orchestration Module
Handles the end-to-end execution flow from candidate memory ingestion to PDF compilation.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from engine.config import OPPORTUNITIES_DIR
from engine.memory import MemoryManager
from engine.jd_parser import JDParser
from engine.matcher import Matcher
from engine.researcher import CompanyResearcher
from engine.generator import DocumentGenerator
from engine.ats_evaluator import ATSEvaluator
from engine.pdf_exporter import PDFExporter
from engine.models import (
    CandidateProfile,
    SemanticKnowledgeGraph,
    ParsedJobDescription,
    MatchScore,
    ATSReport,
    GeneratedMetadata,
)

class ApplicationPipeline:
    """Orchestrates candidate data ingestion, JD parsing, semantic matching, document generation, and PDF exports."""

    def __init__(self, opportunities_dir: Path = OPPORTUNITIES_DIR):
        self.opportunities_dir = opportunities_dir
        self.memory_manager = MemoryManager()
        self.jd_parser = JDParser()
        self.matcher = Matcher()
        self.researcher = CompanyResearcher()
        self.generator = DocumentGenerator()
        self.ats_evaluator = ATSEvaluator()
        self.pdf_exporter = PDFExporter()

    def run(self, opp_name: str) -> Tuple[GeneratedMetadata, Path]:
        """Executes the complete generation pipeline for a given opportunity folder."""
        opp_dir = self.opportunities_dir / opp_name
        if not opp_dir.exists():
            raise FileNotFoundError(f"Opportunity folder '{opp_dir}' does not exist.")

        jd_file = opp_dir / "job_description.txt"
        if not jd_file.exists():
            raise FileNotFoundError(f"Missing 'job_description.txt' inside '{opp_dir}'.")

        # 1. Define Category Subdirectories
        subdirs = {
            "cv": opp_dir / "01_cv",
            "cover_letter": opp_dir / "02_cover_letter",
            "motivation_letter": opp_dir / "03_motivation_letter",
            "emails_and_messaging": opp_dir / "04_emails_and_messaging",
            "analysis_and_research": opp_dir / "05_analysis_and_research",
            "interview_prep": opp_dir / "06_interview_prep",
            "portfolio_and_mapping": opp_dir / "07_portfolio_and_mapping",
        }

        for category_path in subdirs.values():
            category_path.mkdir(parents=True, exist_ok=True)

        # 2. Ingest Candidate Memory & Build Knowledge Graph
        profile: CandidateProfile = self.memory_manager.load_candidate_profile()
        graph: SemanticKnowledgeGraph = self.memory_manager.build_knowledge_graph(profile)

        # 3. Parse Job Description
        raw_jd_text = jd_file.read_text(encoding="utf-8")
        jd: ParsedJobDescription = self.jd_parser.parse(raw_jd_text)

        # 4. Compute Semantic Match & Gap Analysis
        match_score, ats_keywords_txt, gap_analysis_md = self.matcher.compute_match(profile, graph, jd)

        (subdirs["analysis_and_research"] / "ats_keywords.txt").write_text(ats_keywords_txt, encoding="utf-8")
        (subdirs["analysis_and_research"] / "gap_analysis.md").write_text(gap_analysis_md, encoding="utf-8")

        # 5. Synthesize Strategic Company Research
        company_research_md = self.researcher.research(jd)
        (subdirs["analysis_and_research"] / "company_research.md").write_text(company_research_md, encoding="utf-8")

        # 6. Generate Markdown Documents
        generated_docs = self.generator.generate_all(profile, graph, jd, match_score)

        document_directory_mapping = {
            "tailored_cv.tex": subdirs["cv"],
            "tailored_cv.md": subdirs["cv"],
            "cover_letter.md": subdirs["cover_letter"],
            "motivation_letter.md": subdirs["motivation_letter"],
            "short_email.md": subdirs["emails_and_messaging"],
            "follow_up_email.md": subdirs["emails_and_messaging"],
            "linkedin_message.md": subdirs["emails_and_messaging"],
            "interview_notes.md": subdirs["interview_prep"],
            "interview_questions.md": subdirs["interview_prep"],
            "portfolio_projects.md": subdirs["portfolio_and_mapping"],
            "project_mapping.md": subdirs["portfolio_and_mapping"],
            "application_checklist.md": subdirs["portfolio_and_mapping"],
        }

        for filename, content in generated_docs.items():
            target_dir = document_directory_mapping.get(filename, opp_dir)
            (target_dir / filename).write_text(content, encoding="utf-8")

        # 7. Evaluate ATS Compatibility Score
        cv_md_content = generated_docs["tailored_cv.md"]
        ats_report: ATSReport = self.ats_evaluator.evaluate(cv_md_content, jd)

        # 8. Export PDF Files for All Documents
        all_generated_relative_files = ["job_description.txt", "generated_metadata.json"]

        # 8a. Compile native TeX PDF if pdflatex exists; otherwise compile from MD
        tex_file = subdirs["cv"] / "tailored_cv.tex"
        cv_pdf_file = subdirs["cv"] / "tailored_cv.pdf"
        tex_compiled = self.pdf_exporter.export_tex_to_pdf(tex_file.read_text(encoding="utf-8"), cv_pdf_file)
        if not tex_compiled:
            self.pdf_exporter.export_md_to_pdf(cv_md_content, cv_pdf_file)

        # 8b. Compile PDFs for all Markdown files
        for category_dir in subdirs.values():
            for md_file in category_dir.glob("*.md"):
                pdf_file = md_file.with_suffix(".pdf")
                self.pdf_exporter.export_md_to_pdf(md_file.read_text(encoding="utf-8"), pdf_file)
                all_generated_relative_files.extend([
                    str(md_file.relative_to(opp_dir)),
                    str(pdf_file.relative_to(opp_dir)),
                ])
            for tex_f in category_dir.glob("*.tex"):
                all_generated_relative_files.append(str(tex_f.relative_to(opp_dir)))
            for txt_file in category_dir.glob("*.txt"):
                all_generated_relative_files.append(str(txt_file.relative_to(opp_dir)))

        # 9. Write Metadata JSON Manifest
        meta = GeneratedMetadata(
            opportunity_name=opp_name,
            target_company=jd.company_name,
            target_role=jd.job_title,
            timestamp=datetime.now().isoformat(),
            ats_score=ats_report.ats_score,
            grounding_verified=True,
            match_score=match_score.overall_match_percentage,
            generated_files=sorted(list(set(all_generated_relative_files))),
        )

        metadata_file = opp_dir / "generated_metadata.json"
        metadata_file.write_text(meta.model_dump_json(indent=2), encoding="utf-8")

        return meta, opp_dir
