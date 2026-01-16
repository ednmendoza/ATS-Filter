from typing import Dict, Any, List
import re
from datetime import datetime
from .jd_extract import extract_jd_signals, extract_keywords
from .platform_profiles import get_platform_profile


def calculate_keyword_score(resume_text: str, jd_keywords: List[str]) -> float:
    """Calculate keyword match score (0-1)"""
    if not jd_keywords:
        return 0.0
    
    resume_lower = resume_text.lower()
    matches = sum(1 for keyword in jd_keywords if keyword.lower() in resume_lower)
    
    return min(matches / len(jd_keywords), 1.0)


def calculate_title_score(resume_text: str, jd_text: str) -> float:
    """Calculate title alignment score (0-1)"""
    # Extract job title from JD (simple heuristic)
    jd_lines = jd_text.split('\n')[:10]  # Check first 10 lines
    jd_title = None
    
    for line in jd_lines:
        if any(word in line.lower() for word in ['engineer', 'developer', 'architect', 'manager', 'lead']):
            jd_title = line.strip()
            break
    
    if not jd_title:
        return 0.5  # Neutral if can't detect
    
    # Extract titles from resume
    resume_lines = resume_text.split('\n')[:50]
    resume_titles = []
    
    for line in resume_lines:
        if any(word in line.lower() for word in ['engineer', 'developer', 'architect', 'manager', 'lead']):
            resume_titles.append(line.strip())
    
    if not resume_titles:
        return 0.3  # Low score if no titles found
    
    # Simple similarity check
    jd_title_lower = jd_title.lower()
    for resume_title in resume_titles:
        resume_title_lower = resume_title.lower()
        # Check for common words
        jd_words = set(jd_title_lower.split())
        resume_words = set(resume_title_lower.split())
        common_words = jd_words.intersection(resume_words)
        
        if len(common_words) >= 2:
            return 0.8  # Good match
        elif len(common_words) >= 1:
            return 0.5  # Partial match
    
    return 0.3  # Low match


def calculate_age_proxy_risk(resume_text: str) -> float:
    """Calculate age proxy risk (0-1, higher = more risk)"""
    # Look for graduation dates, very old experience dates
    text_lower = resume_text.lower()
    
    # Find years (1980-2024)
    years = re.findall(r'\b(19[89]\d|20[0-2]\d)\b', resume_text)
    
    if not years:
        return 0.1  # Low risk if no dates
    
    years_int = [int(y) for y in years if y.isdigit()]
    if not years_int:
        return 0.1
    
    oldest_year = min(years_int)
    current_year = datetime.now().year
    
    # Risk increases if oldest year is before 2000
    if oldest_year < 2000:
        years_old = current_year - oldest_year
        if years_old > 30:
            return 0.8  # High risk
        elif years_old > 20:
            return 0.5  # Medium risk
        else:
            return 0.2  # Low risk
    
    return 0.1  # Low risk


def calculate_overqual_risk(resume_text: str, jd_signals: Dict[str, Any]) -> float:
    """Calculate overqualification risk (0-1, higher = more risk)"""
    jd_seniority = jd_signals.get("seniority", "unspecified")
    resume_lower = resume_text.lower()
    
    # Check for senior indicators in resume
    senior_terms = ['senior', 'lead', 'principal', 'architect', 'director', 'vp', 'cto']
    resume_has_senior = any(term in resume_lower for term in senior_terms)
    
    # Risk if resume is senior but JD is junior
    if resume_has_senior and jd_seniority == "junior":
        return 0.7  # High risk
    elif resume_has_senior and jd_seniority == "mid":
        return 0.3  # Medium risk
    elif not resume_has_senior and jd_seniority == "senior":
        return 0.2  # Low risk (underqualified, not overqualified)
    
    return 0.1  # Low risk


def calculate_survivability_score(
    resume_text: str,
    jd_text: str,
    platform: str
) -> Dict[str, float]:
    """
    Calculate comprehensive survivability score.
    
    Formula:
    Survivability = (KeywordScore × Wk) + (TitleScore × Wt) + (Recency × Wr)
                   - (AgeRisk × 0.1) - (OverQualRisk × 0.1)
    """
    # Extract JD signals
    jd_signals = extract_jd_signals(jd_text)
    jd_keywords = jd_signals.get("top_terms", [])
    
    # Get platform weights
    platform_profile = get_platform_profile(platform)
    wk = platform_profile["keyword_weight"]
    wt = platform_profile["title_weight"]
    wr = platform_profile["recency_weight"]
    
    # Calculate individual scores
    keyword_score = calculate_keyword_score(resume_text, jd_keywords)
    title_score = calculate_title_score(resume_text, jd_text)
    
    # Recency score (simplified - can be enhanced with actual dates)
    recency_score = 0.7  # Default, can be calculated from experience dates
    
    # Risk scores
    age_risk = calculate_age_proxy_risk(resume_text)
    overqual_risk = calculate_overqual_risk(resume_text, jd_signals)
    
    # Calculate survivability
    survivability = (
        (keyword_score * wk) +
        (title_score * wt) +
        (recency_score * wr) -
        (age_risk * 0.1) -
        (overqual_risk * 0.1)
    )
    
    # Clamp to 0-1
    survivability = max(0.0, min(1.0, survivability))
    
    return {
        "keyword_score": round(keyword_score, 2),
        "title_score": round(title_score, 2),
        "age_proxy_risk": round(age_risk, 2),
        "overqual_risk": round(overqual_risk, 2),
        "survivability": round(survivability, 2)
    }
