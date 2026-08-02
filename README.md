# Career-Application-Agent (Personal AI Career Operating System)

An elite, local AI Career Application Agent designed to automatically generate world-class, ATS-optimized application packages from any Job Description (JD).

---

## Key Features

- **Permanent Candidate Memory (`myself/`)**: Ingests and cross-references all personal text files (`profile.txt`, `experience.txt`, `education.txt`, `skills.txt`, `certificates.txt`, `projects/`, `publications.txt`, etc.).
- **Zero-Hallucination Grounding**: Every CV, cover letter, email, and statement strictly uses verifiable facts, dates, and metrics from `myself/`.
- **Knowledge Graph & Semantic Matcher**: Dynamically maps candidate project evidence and skill nodes against job requirements to calculate match scores and perform gap analysis.
- **ATS Optimization (Target 95%+)**: Automatic keyword placement, standard section headers, clean layout, and quantitative metric enforcement.
- **Complete 18-Artifact Output Suite**: Produces a full application folder inside `opportunities/<Opportunity_Name>/` for every job opportunity:
  1. `job_description.txt`
  2. `company_research.md`
  3. `ats_keywords.txt`
  4. `gap_analysis.md`
  5. `tailored_cv.md`
  6. `tailored_cv.pdf`
  7. `cover_letter.md`
  8. `cover_letter.pdf`
  9. `motivation_letter.md`
  10. `motivation_letter.pdf`
  11. `short_email.md`
  12. `follow_up_email.md`
  13. `linkedin_message.md`
  14. `interview_notes.md`
  15. `interview_questions.md`
  16. `portfolio_projects.md`
  17. `project_mapping.md`
  18. `application_checklist.md`
  19. `generated_metadata.json`

- **Dual Control Interfaces**:
  - **CLI**: Fast execution via Typer.
  - **FastAPI Web Dashboard**: Interactive browser GUI.

---

## Directory Structure

```
Career-Application-Agent/
├── myself/                       # Personal knowledge base (Permanent Memory)
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
│       ├── baki.txt
│       ├── adaptive_blended_assessment.txt
│       └── project3.txt
│
├── opportunities/
│   └── Google_AI_Engineer/
│       └── job_description.txt
│
├── templates/
├── prompts/
├── engine/
│   ├── config.py
│   ├── models.py
│   ├── memory.py
│   ├── jd_parser.py
│   ├── matcher.py
│   ├── researcher.py
│   ├── generator.py
│   ├── ats_evaluator.py
│   ├── pdf_exporter.py
│   ├── cli.py
│   └── app.py
├── pyproject.toml
└── README.md
```

---

## Usage Instructions

### 1. Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Inspect Candidate Memory
To verify your personal knowledge base in `myself/`:
```bash
python -m engine.cli inspect-memory
```

### 3. Generate Application Package for an Opportunity
Create a folder inside `opportunities/` (e.g. `opportunities/Google_AI_Engineer/`) and place `job_description.txt` inside it. Then run:
```bash
python -m engine.cli run --opp Google_AI_Engineer
```

### 4. Launch Interactive Web Dashboard
To view and manage your applications in the browser:
```bash
python -m engine.cli gui
```
Open [http://localhost:8000](http://localhost:8000) in your browser.
