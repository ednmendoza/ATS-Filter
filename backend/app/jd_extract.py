import json
import re
from typing import Dict, Any, List
from collections import Counter
from .config import settings


def extract_keywords(text: str, top_n: int = 20) -> List[str]:
    """Extract top keywords from job description"""
    # Common technical terms (can be expanded)
    tech_terms = [
        'azure', 'aws', 'gcp', 'terraform', 'kubernetes', 'docker',
        'python', 'java', 'javascript', 'typescript', 'react', 'node',
        'sql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
        'ci/cd', 'jenkins', 'gitlab', 'github', 'agile', 'scrum',
        'microservices', 'api', 'rest', 'graphql', 'grpc',
        'linux', 'bash', 'shell', 'ansible', 'puppet', 'chef',
        'bgp', 'ospf', 'networking', 'security', 'firewall',
        'ml', 'machine learning', 'ai', 'data science', 'analytics'
    ]
    
    text_lower = text.lower()
    words = re.findall(r'\b[a-z]+\b', text_lower)
    
    # Count occurrences
    word_counts = Counter(words)
    
    # Filter for tech terms and common important words
    important_words = []
    for word in word_counts.most_common(100):
        if word[0] in tech_terms or len(word[0]) > 4:
            important_words.append(word[0])
    
    return important_words[:top_n]


def detect_seniority(text: str) -> str:
    """Detect seniority level from job description"""
    text_lower = text.lower()
    
    senior_indicators = ['senior', 'sr.', 'lead', 'principal', 'architect', 'staff', 'expert']
    mid_indicators = ['mid-level', 'mid level', 'intermediate', 'experienced']
    junior_indicators = ['junior', 'jr.', 'entry', 'associate', 'intern']
    
    senior_count = sum(1 for term in senior_indicators if term in text_lower)
    mid_count = sum(1 for term in mid_indicators if term in text_lower)
    junior_count = sum(1 for term in junior_indicators if term in text_lower)
    
    if senior_count > 0:
        return "senior"
    elif mid_count > 0:
        return "mid"
    elif junior_count > 0:
        return "junior"
    else:
        return "unspecified"


def detect_hands_on_bias(text: str) -> bool:
    """Detect if job description emphasizes hands-on work"""
    text_lower = text.lower()
    hands_on_terms = [
        'hands-on', 'hands on', 'hands-on experience', 'coding', 'development',
        'implement', 'build', 'develop', 'write code', 'programming'
    ]
    return any(term in text_lower for term in hands_on_terms)


def detect_fast_paced(text: str) -> bool:
    """Detect if job description mentions fast-paced environment"""
    text_lower = text.lower()
    fast_paced_terms = [
        'fast-paced', 'fast paced', 'fast-moving', 'dynamic', 'startup',
        'rapid growth', 'high growth', 'move fast'
    ]
    return any(term in text_lower for term in fast_paced_terms)


def extract_jd_signals(raw_text: str) -> Dict[str, Any]:
    """
    Extract intelligence signals from job description.
    Returns structured JSON with keywords, seniority, and bias flags.
    """
    top_terms = extract_keywords(raw_text)
    seniority = detect_seniority(raw_text)
    hands_on = detect_hands_on_bias(raw_text)
    fast_paced = detect_fast_paced(raw_text)
    
    return {
        "top_terms": top_terms,
        "seniority": seniority,
        "signals": {
            "hands_on": hands_on,
            "fast_paced": fast_paced
        }
    }
