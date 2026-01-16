from typing import Dict, Any, List
import re
from .jd_extract import extract_jd_signals
from .platform_profiles import get_platform_profile


def extract_resume_sections(resume_text: str) -> Dict[str, str]:
    """Extract basic sections from resume text"""
    sections = {
        "summary": "",
        "skills": "",
        "experience": "",
        "education": ""
    }
    
    # Simple section detection (can be enhanced)
    text_lower = resume_text.lower()
    
    # Look for common section headers
    summary_patterns = [r'summary', r'profile', r'objective', r'overview']
    skills_patterns = [r'skills', r'technical skills', r'competencies']
    experience_patterns = [r'experience', r'work history', r'employment', r'professional experience']
    education_patterns = [r'education', r'academic', r'qualifications']
    
    lines = resume_text.split('\n')
    current_section = None
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        if any(re.search(pattern, line_lower) for pattern in summary_patterns):
            current_section = "summary"
        elif any(re.search(pattern, line_lower) for pattern in skills_patterns):
            current_section = "skills"
        elif any(re.search(pattern, line_lower) for pattern in experience_patterns):
            current_section = "experience"
        elif any(re.search(pattern, line_lower) for pattern in education_patterns):
            current_section = "education"
        elif current_section and line.strip():
            sections[current_section] += line + "\n"
    
    return sections


def find_matching_skills(resume_text: str, jd_keywords: List[str]) -> List[str]:
    """Find skills in resume that match JD keywords"""
    resume_lower = resume_text.lower()
    matching = []
    
    for keyword in jd_keywords:
        if keyword.lower() in resume_lower:
            matching.append(keyword)
    
    return matching


def create_persona_summary(persona: str, resume_sections: Dict[str, str], jd_signals: Dict[str, Any]) -> str:
    """Create persona-based summary"""
    if persona == "ic":
        focus = "hands-on technical implementation"
    elif persona == "architect":
        focus = "system design and technical leadership"
    elif persona == "hybrid":
        focus = "technical leadership with hands-on implementation"
    else:
        focus = "technical expertise"
    
    # Use existing summary if available, otherwise create basic one
    existing_summary = resume_sections.get("summary", "").strip()
    if existing_summary:
        # Enhance existing summary with persona focus
        return f"{existing_summary}\n\nSpecializing in {focus}."
    else:
        return f"Experienced professional specializing in {focus}."


def compile_resume_variant(
    resume_text: str,
    jd_text: str,
    persona: str,
    platform: str
) -> str:
    """
    Compile ATS-optimized resume variant.
    
    Rules:
    - Never invent skills
    - Only reuse content already present
    - Emphasize JD-matching terms only if found in resume
    """
    # Extract JD signals
    jd_signals = extract_jd_signals(jd_text)
    jd_keywords = jd_signals.get("top_terms", [])
    
    # Extract resume sections
    resume_sections = extract_resume_sections(resume_text)
    
    # Find matching skills
    matching_skills = find_matching_skills(resume_text, jd_keywords)
    
    # Create persona-based summary
    summary = create_persona_summary(persona, resume_sections, jd_signals)
    
    # Build compiled resume
    compiled_parts = []
    
    # Summary section
    compiled_parts.append("SUMMARY")
    compiled_parts.append("=" * 50)
    compiled_parts.append(summary)
    compiled_parts.append("")
    
    # Skills section (emphasize matching skills)
    if resume_sections.get("skills") or matching_skills:
        compiled_parts.append("SKILLS")
        compiled_parts.append("=" * 50)
        if matching_skills:
            # List matching skills first
            compiled_parts.append(", ".join(matching_skills))
            compiled_parts.append("")
        if resume_sections.get("skills"):
            compiled_parts.append(resume_sections["skills"])
        compiled_parts.append("")
    
    # Original resume content (unchanged)
    compiled_parts.append("EXPERIENCE")
    compiled_parts.append("=" * 50)
    if resume_sections.get("experience"):
        compiled_parts.append(resume_sections["experience"])
    else:
        # Fallback: use original text
        compiled_parts.append(resume_text)
    compiled_parts.append("")
    
    # Education
    if resume_sections.get("education"):
        compiled_parts.append("EDUCATION")
        compiled_parts.append("=" * 50)
        compiled_parts.append(resume_sections["education"])
        compiled_parts.append("")
    
    return "\n".join(compiled_parts)
