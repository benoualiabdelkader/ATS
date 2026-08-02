from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class CandidateProfile(BaseModel):
    profile_summary: str = ""
    contact_info: Dict[str, str] = Field(default_factory=dict)
    education: List[str] = Field(default_factory=list)
    experience: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    certificates: List[str] = Field(default_factory=list)
    projects: Dict[str, str] = Field(default_factory=dict)
    volunteering: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    awards: List[str] = Field(default_factory=list)
    publications: List[str] = Field(default_factory=list)
    hackathons: List[str] = Field(default_factory=list)
    conferences: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)
    links: List[str] = Field(default_factory=list)
    personal_statement: str = ""
    interests: List[str] = Field(default_factory=list)
    raw_files: Dict[str, str] = Field(default_factory=dict)

class SemanticKnowledgeGraph(BaseModel):
    candidate_name: str = ""
    core_domains: List[str] = Field(default_factory=list)
    skill_nodes: Dict[str, List[str]] = Field(default_factory=dict)  # skill -> supporting project/exp
    project_nodes: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    experience_nodes: List[Dict[str, Any]] = Field(default_factory=list)
    publication_nodes: List[str] = Field(default_factory=list)
    certificate_nodes: List[str] = Field(default_factory=list)

class ParsedJobDescription(BaseModel):
    company_name: str = "Target Company"
    job_title: str = "Target Role"
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    years_experience: str = ""
    education_level: str = ""
    key_responsibilities: List[str] = Field(default_factory=list)
    ats_keywords: List[str] = Field(default_factory=list)
    action_verbs: List[str] = Field(default_factory=list)
    company_mission_and_values: str = ""
    priority_domains: List[str] = Field(default_factory=list)

class MatchScore(BaseModel):
    overall_match_percentage: float = 0.0
    skill_breakdown: Dict[str, float] = Field(default_factory=dict)
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    strongest_projects: List[str] = Field(default_factory=list)
    strongest_experiences: List[str] = Field(default_factory=list)

class ATSReport(BaseModel):
    ats_score: float = 0.0
    keyword_match_rate: float = 0.0
    formatting_score: float = 0.0
    quantified_impact_score: float = 0.0
    matched_keywords_count: int = 0
    total_keywords_count: int = 0
    recommendations: List[str] = Field(default_factory=list)

class GeneratedMetadata(BaseModel):
    opportunity_name: str
    target_company: str
    target_role: str
    timestamp: str
    ats_score: float
    grounding_verified: bool = True
    match_score: float
    generated_files: List[str] = Field(default_factory=list)
