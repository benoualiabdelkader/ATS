"""
Career-Application-Agent Engine Package
AI-Powered Personal Career Operating System
"""

from engine.config import settings
from engine.models import (
    CandidateProfile,
    SemanticKnowledgeGraph,
    ParsedJobDescription,
    MatchScore,
    ATSReport,
    GeneratedMetadata,
)
from engine.memory import MemoryManager
from engine.jd_parser import JDParser
from engine.matcher import Matcher
from engine.researcher import CompanyResearcher
from engine.generator import DocumentGenerator
from engine.ats_evaluator import ATSEvaluator
from engine.pdf_exporter import PDFExporter
from engine.pipeline import ApplicationPipeline

__version__ = "1.0.0"

__all__ = [
    "settings",
    "CandidateProfile",
    "SemanticKnowledgeGraph",
    "ParsedJobDescription",
    "MatchScore",
    "ATSReport",
    "GeneratedMetadata",
    "MemoryManager",
    "JDParser",
    "Matcher",
    "CompanyResearcher",
    "DocumentGenerator",
    "ATSEvaluator",
    "PDFExporter",
    "ApplicationPipeline",
]
