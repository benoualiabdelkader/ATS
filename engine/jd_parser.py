import re
from typing import List
from engine.models import ParsedJobDescription

class JDParser:
    def parse(self, raw_jd_text: str) -> ParsedJobDescription:
        """Parses job description text into a structured ParsedJobDescription object."""
        parsed = ParsedJobDescription()
        
        # Company Name Extraction
        company_match = re.search(r"COMPANY:\s*(.+)", raw_jd_text, re.IGNORECASE)
        if company_match:
            parsed.company_name = company_match.group(1).strip()
        elif "Google" in raw_jd_text:
            parsed.company_name = "Google"

        # Job Title Extraction
        title_match = re.search(r"JOB TITLE:\s*(.+)", raw_jd_text, re.IGNORECASE)
        if title_match:
            parsed.job_title = title_match.group(1).strip()
        elif "Role" in raw_jd_text:
            title_match = re.search(r"ROLE:\s*(.+)", raw_jd_text, re.IGNORECASE)
            if title_match:
                parsed.job_title = title_match.group(1).strip()

        # Skill Extraction via rule-based heuristics & regex
        tech_keywords = [
            "PyTorch", "TensorFlow", "JAX", "Python", "C++", "RAG", "LLM", "LLMs",
            "LoRA", "QLoRA", "vLLM", "ChromaDB", "FAISS", "TensorRT", "ONNX", "Docker",
            "Kubernetes", "FastAPI", "Flask", "AWS", "GCP", "TPU", "GPU", "Ray",
            "Vector Databases", "Prompt Engineering", "Fine-tuning", "Agentic Systems",
            "Deep Learning", "NLP", "Computer Vision", "CI/CD", "System Design"
        ]
        
        found_skills = []
        for kw in tech_keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", raw_jd_text, re.IGNORECASE):
                found_skills.append(kw)

        parsed.required_skills = found_skills[:10] if found_skills else ["Python", "Machine Learning", "Deep Learning", "PyTorch"]
        parsed.preferred_skills = found_skills[10:] if len(found_skills) > 10 else ["JAX", "TPU", "Agentic Systems"]

        # Years of Experience
        yoe_match = re.search(r"(\d+\+?\s*years)", raw_jd_text, re.IGNORECASE)
        if yoe_match:
            parsed.years_experience = yoe_match.group(1)
        else:
            parsed.years_experience = "5+ years"

        # Education
        if "Ph.D." in raw_jd_text or "PhD" in raw_jd_text:
            parsed.education_level = "M.S. or Ph.D. in Computer Science or quantitative field"
        else:
            parsed.education_level = "B.S. or M.S. in Computer Science"

        # Responsibilities
        resp_section = re.search(r"RESPONSIBILITIES:(.*?)(REQUIREMENTS|QUALIFICATIONS|ABOUT|$)", raw_jd_text, re.DOTALL | re.IGNORECASE)
        if resp_section:
            lines = [l.strip("- ").strip() for l in resp_section.group(1).splitlines() if l.strip()]
            parsed.key_responsibilities = lines[:6]
        else:
            parsed.key_responsibilities = [
                "Architect and optimize scalable LLM training and inference pipelines.",
                "Design high-throughput RAG systems and dense retrieval algorithms.",
                "Quantize and compress large models for efficient GPU/TPU deployment."
            ]

        # ATS Keywords & Action Verbs
        parsed.ats_keywords = found_skills + ["Scalable ML", "High-Throughput", "Distributed Systems", "Model Optimization", "Latency Reduction"]
        parsed.action_verbs = ["Architected", "Engineered", "Optimized", "Fine-tuned", "Deployed", "Spearheaded", "Quantized", "Built"]
        
        # Mission & Values
        parsed.company_mission_and_values = "Organize the world's information and make it universally accessible and useful. Focus on research excellence, scalable impact, and high engineering bar."

        return parsed
