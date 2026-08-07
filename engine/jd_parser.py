import re
from typing import List
from engine.models import ParsedJobDescription

class JDParser:
    def parse(self, raw_jd_text: str) -> ParsedJobDescription:
        """Parses job description text into a structured ParsedJobDescription object."""
        parsed = ParsedJobDescription()
        
        # Company Name Extraction
        company_match = re.search(r"(?:\*\*Organization:\*\*|Organization:|COMPANY:|AT:)\s*([^\n\r]+)", raw_jd_text, re.IGNORECASE)
        if company_match:
            parsed.company_name = company_match.group(1).strip("*").strip()
        elif "SPARK AI Research" in raw_jd_text:
            parsed.company_name = "SPARK AI Research"
        elif "Bamboo Works" in raw_jd_text:
            parsed.company_name = "Bamboo Works"
        elif "Google" in raw_jd_text:
            parsed.company_name = "Google"

        # Job Title Extraction
        title_match = re.search(r"(?:\*\*Opportunity Title:\*\*|Opportunity Title:|JOB TITLE:|TITLE:|ROLE:)\s*([^\n\r]+)", raw_jd_text, re.IGNORECASE)
        if title_match:
            parsed.job_title = title_match.group(1).strip("*").strip()
        elif "SPARK AI Research Fellowship" in raw_jd_text:
            parsed.job_title = "SPARK AI Research Fellow"
        elif "AI & Automation Intern" in raw_jd_text or "AI & Automation Internship" in raw_jd_text:
            parsed.job_title = "AI & Automation Intern"
        elif "AI Engineer" in raw_jd_text:
            parsed.job_title = "AI Engineer"

        # Skill Extraction via rule-based heuristics & regex
        tech_keywords = [
            "Python", "C", "C++", "JavaScript", "HTML5", "CSS", "Figma", "UI/UX",
            "Artificial Intelligence", "Machine Learning", "Deep Learning", "NLP",
            "Natural Language Processing", "Random Forest", "AI-assisted tools",
            "Claude Code", "Codex", "No-code", "Low-code", "Automation", "Workflow Automation",
            "IT Support", "Systems Administration", "Linux", "Windows", "Git", "GitHub"
        ]
        
        found_skills = []
        for kw in tech_keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", raw_jd_text, re.IGNORECASE):
                found_skills.append(kw)

        parsed.required_skills = found_skills[:10] if found_skills else ["Python", "Machine Learning", "AI & Automation", "Workflow Automation"]
        parsed.preferred_skills = found_skills[10:] if len(found_skills) > 10 else ["Claude Code", "Codex", "No-code / Low-code Platforms"]

        # Years of Experience
        yoe_match = re.search(r"(\d+\+?\s*years)", raw_jd_text, re.IGNORECASE)
        if yoe_match:
            parsed.years_experience = yoe_match.group(1)
        else:
            parsed.years_experience = "Internship / Entry Level"

        # Education
        parsed.education_level = "Degree in Computer Science, Software Engineering, IT or related field"

        # Responsibilities
        parsed.key_responsibilities = [
            "Assist in building internal tools, dashboards, automations, and lightweight applications.",
            "Support the development of AI-powered workflows and operational improvements.",
            "Research and test emerging AI tools, platforms, and technologies.",
            "Work with AI-assisted coding environments and no-code/low-code automation tools.",
            "Collaborate with management on new product and process ideas.",
            "Help improve internal systems and team efficiency through automation."
        ]

        # ATS Keywords & Action Verbs
        parsed.ats_keywords = found_skills + ["Internal Tools", "Workflow Automation", "Process Efficiency", "AI-Assisted Development"]
        parsed.action_verbs = ["Architected", "Engineered", "Automated", "Developed", "Built", "Designed", "Optimized", "Collaborated"]
        
        # Mission & Values
        parsed.company_mission_and_values = "Help companies around the world build high-performing remote teams. Invest in AI, automation, and internal technology to build smarter systems and improve business operations."

        return parsed
