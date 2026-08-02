# System Architecture & Documentation

## Overview
The **Career-Application-Agent** is a personal AI Career Operating System designed to ingest candidate experience data from `myself/`, parse target Job Descriptions from `opportunities/`, build a semantic knowledge graph, and generate ATS-optimized application packages with zero hallucination.

---

## Workspace Directory Structure

```
Career-Application-Agent/
├── docs/                           # Documentation & External Reference Guides
│   ├── ARCHITECTURE.md
│   └── Wonsulting Resume Template Guide.docx
│
├── engine/                         # Core Python Processing Engine
│   ├── __init__.py
│   ├── app.py                      # FastAPI Web UI Dashboard
│   ├── ats_evaluator.py           # ATS Compatibility Scorer (0-100%)
│   ├── cli.py                      # Typer CLI Entrypoint
│   ├── config.py                   # Pydantic Settings & Environment
│   ├── generator.py                # Document Synthesis Engine
│   ├── jd_parser.py                # Job Description Parser
│   ├── matcher.py                  # Semantic Graph Matcher & Gap Analysis
│   ├── memory.py                   # Ingestion & Knowledge Graph Builder
│   ├── models.py                   # Pydantic Schemas
│   ├── pdf_exporter.py             # Markdown to PDF Compiler
│   ├── pipeline.py                 # Pipeline Orchestrator
│   └── researcher.py               # Strategic Company Research
│
├── myself/                         # Candidate Permanent Memory Base
│   ├── profile.txt
│   ├── education.txt
│   ├── experience.txt
│   ├── skills.txt
│   ├── certificates.txt
│   ├── volunteering.txt
│   ├── achievements.txt
│   ├── awards.txt
│   ├── publications.txt
│   ├── hackathons.txt
│   ├── conferences.txt
│   ├── languages.txt
│   ├── references.txt
│   ├── links.txt
│   ├── personal_statement.txt
│   ├── interests.txt
│   └── projects/
│       ├── adaptive_blended_assessment.txt
│       ├── baki.txt
│       └── edgequant.txt
│
├── opportunities/                  # Generated Opportunity Packages
│   └── Google_AI_Engineer/
│       ├── job_description.txt
│       ├── generated_metadata.json
│       ├── 01_cv/
│       ├── 02_cover_letter/
│       ├── 03_motivation_letter/
│       ├── 04_emails_and_messaging/
│       ├── 05_analysis_and_research/
│       ├── 06_interview_prep/
│       └── 07_portfolio_and_mapping/
│
├── prompts/                        # System Prompts for Pipeline Steps
│   ├── ats_evaluator_prompt.txt
│   ├── company_research_prompt.txt
│   ├── cover_letter_prompt.txt
│   ├── cv_generator_prompt.txt
│   ├── gap_analysis_prompt.txt
│   ├── interview_prep_prompt.txt
│   └── jd_parser_prompt.txt
│
├── templates/                      # Clean Markdown Templates & CSS Styles
│   ├── pdf_styles.css
│   ├── perfect_ats_cv_template.md
│   ├── professional_cv_template.md
│   ├── resume_type_checker.md
│   └── student_cv_template.md
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Processing Pipeline Steps

1. **Memory Ingestion**: `MemoryManager` recursively reads text files from `myself/` and builds a candidate `SemanticKnowledgeGraph`.
2. **JD Parsing**: `JDParser` extracts core criteria, technical skills, years of experience, responsibilities, and culture signals from `job_description.txt`.
3. **Semantic Matching**: `Matcher` computes percentage match, rank-orders evidence, and outputs `ats_keywords.txt` and `gap_analysis.md`.
4. **Strategic Research**: `CompanyResearcher` synthesizes company strategic goals and hiring signals into `company_research.md`.
5. **Document Synthesis**: `DocumentGenerator` produces 11 grounded Markdown application documents.
6. **ATS Audit**: `ATSEvaluator` scores ATS compatibility against Workday, Greenhouse, Lever, Taleo, and iCIMS rules.
7. **PDF Compilation**: `PDFExporter` renders single-column, ATS-friendly PDFs for all generated documents.
