from pathlib import Path
from typing import Dict, List
import re
from engine.config import MYSELF_DIR
from engine.models import CandidateProfile, SemanticKnowledgeGraph

class MemoryManager:
    def __init__(self, myself_dir: Path = MYSELF_DIR):
        self.myself_dir = myself_dir

    def load_candidate_profile(self) -> CandidateProfile:
        """Reads all text files inside myself/ recursively and builds candidate profile."""
        profile = CandidateProfile()
        if not self.myself_dir.exists():
            return profile

        # Scan root files
        for txt_file in self.myself_dir.glob("*.txt"):
            content = txt_file.read_text(encoding="utf-8").strip()
            name = txt_file.stem
            profile.raw_files[name] = content

            lines = [line.strip() for line in content.splitlines() if line.strip()]
            if name == "profile":
                profile.profile_summary = content
            elif name == "education":
                profile.education = lines
            elif name == "experience":
                profile.experience = lines
            elif name == "skills":
                profile.skills = lines
            elif name == "certificates":
                profile.certificates = lines
            elif name == "volunteering":
                profile.volunteering = lines
            elif name == "achievements":
                profile.achievements = lines
            elif name == "awards":
                profile.awards = lines
            elif name == "publications":
                profile.publications = lines
            elif name == "hackathons":
                profile.hackathons = lines
            elif name == "conferences":
                profile.conferences = lines
            elif name == "languages":
                profile.languages = lines
            elif name == "references":
                profile.references = lines
            elif name == "links":
                profile.links = lines
            elif name == "personal_statement":
                profile.personal_statement = content
            elif name == "interests":
                profile.interests = lines

        # Scan projects subfolder
        projects_dir = self.myself_dir / "projects"
        if projects_dir.exists():
            for proj_file in projects_dir.glob("*.txt"):
                profile.projects[proj_file.stem] = proj_file.read_text(encoding="utf-8").strip()

        # Scan extra subfolder
        extra_dir = self.myself_dir / "extra"
        if extra_dir.exists():
            for extra_file in extra_dir.glob("*.txt"):
                profile.raw_files[f"extra_{extra_file.stem}"] = extra_file.read_text(encoding="utf-8").strip()

        return profile

    def build_knowledge_graph(self, profile: CandidateProfile) -> SemanticKnowledgeGraph:
        """Cross-references skills, projects, certifications, and experience into a knowledge graph."""
        graph = SemanticKnowledgeGraph()
        
        # Extract candidate name from profile.txt (supports "FULL NAME:" and "NAME:" keys)
        for line in profile.profile_summary.splitlines():
            line_stripped = line.strip()
            if line_stripped.upper().startswith("FULL NAME:"):
                graph.candidate_name = line_stripped.split(":", 1)[1].strip()
                break
            elif "NAME:" in line_stripped.upper() and not line_stripped.upper().startswith("PREFERRED"):
                graph.candidate_name = line_stripped.split(":", 1)[1].strip()
                break
        if not graph.candidate_name:
            graph.candidate_name = "Candidate"

        # Build skill nodes mapping skill -> supporting context
        all_text = " ".join(profile.raw_files.values())
        
        known_skills = []
        for line in profile.skills:
            if ":" in line:
                _, items = line.split(":", 1)
                known_skills.extend([s.strip() for s in items.split(",") if s.strip()])
            else:
                known_skills.extend([s.strip() for s in line.split(",") if s.strip()])

        for skill in set(known_skills):
            evidence = []
            pattern = re.compile(re.escape(skill), re.IGNORECASE)
            
            # Check experience
            for exp in profile.experience:
                if pattern.search(exp):
                    evidence.append(f"Experience: {exp[:100]}...")
            
            # Check projects
            for proj_name, proj_content in profile.projects.items():
                if pattern.search(proj_content):
                    evidence.append(f"Project [{proj_name}]")
                    
            # Check certs
            for cert in profile.certificates:
                if pattern.search(cert):
                    evidence.append(f"Certificate: {cert}")

            graph.skill_nodes[skill] = evidence if evidence else ["Stated in core skills profile"]

        # Build project nodes
        for proj_name, proj_content in profile.projects.items():
            graph.project_nodes[proj_name] = {
                "title": proj_name.replace("_", " ").title(),
                "content": proj_content
            }

        graph.publication_nodes = profile.publications
        graph.certificate_nodes = profile.certificates

        return graph

    def determine_candidate_type(self, profile: CandidateProfile) -> str:
        """Determines whether candidate should use 'STUDENT' or 'PROFESSIONAL' template structure."""
        exp_text = " ".join(profile.experience).lower()
        if "lead" in exp_text or "senior" in exp_text or "architect" in exp_text or len(profile.experience) >= 6:
            return "PROFESSIONAL"
        
        edu_text = " ".join(profile.education).lower()
        if "present" in edu_text or "2025" in edu_text or "2026" in edu_text or "student" in edu_text:
            return "STUDENT"
            
        return "PROFESSIONAL"

