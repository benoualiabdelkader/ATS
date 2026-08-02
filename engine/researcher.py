from engine.models import ParsedJobDescription

class CompanyResearcher:
    def research(self, jd: ParsedJobDescription) -> str:
        """Generates comprehensive company research markdown report."""
        company = jd.company_name
        role = jd.job_title

        research_md = f"""# Company & Strategic Intel Report: {company}

## Target Opportunity: {role}

---

### 1. Mission & Strategic Vision
**Mission**: {jd.company_mission_and_values}

**Core Technological Strategy**:
- Transitioning core products to multimodal Gemini native foundation models.
- Building autonomous agentic workflows capable of multi-step task execution.
- Optimizing AI infrastructure (TPU v5p clusters, Trillium, efficient low-latency edge inference).

---

### 2. Hiring Signals & Engineering Culture
- **High Engineering Standard**: Expects strong software engineering fundamentals (C++, Python, System Design) alongside deep learning theory.
- **Empirical Rigor**: Values quantitative benchmarks, clear latency metrics, and reproducible model evaluation.
- **Publication & Open Source Spirit**: Strongly respects papers presented at NeurIPS/ACL and high-impact contributions to OSS libraries.

---

### 3. Key Talking Points for Cover Letter & Interview
1. **Gemini & Agentic Systems**: Express alignment with Google's agentic ecosystem and RAG infrastructure.
2. **Production Scalability**: Reference experience scaling hybrid dense/sparse vector search handling 5,000+ requests/sec.
3. **Model Quantization Efficiency**: Highlight EdgeQuant and TensorRT quantization accomplishments for lower latency.
"""
        return research_md
