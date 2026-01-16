"""
Example script demonstrating API usage.
Run this after starting the backend server.
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def upload_resume(file_path: str, user_id: str = "test_user") -> dict:
    """Upload a resume file"""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'user_id': user_id}
        response = requests.post(f"{BASE_URL}/resumes/upload", files=files, data=data)
        response.raise_for_status()
        return response.json()


def create_job_description(platform: str, raw_text: str) -> dict:
    """Create a job description"""
    response = requests.post(
        f"{BASE_URL}/jds",
        json={"platform": platform, "raw_text": raw_text}
    )
    response.raise_for_status()
    return response.json()


def compile_variant(resume_id: str, jd_id: str, persona: str, platform: str) -> dict:
    """Compile a resume variant"""
    response = requests.post(
        f"{BASE_URL}/variants/compile",
        json={
            "resume_id": resume_id,
            "jd_id": jd_id,
            "persona": persona,
            "platform": platform
        }
    )
    response.raise_for_status()
    return response.json()


def main():
    """Example workflow"""
    print("ATS Resume Compiler - Example Usage\n")
    
    # Example 1: Upload resume
    print("1. Uploading resume...")
    try:
        resume = upload_resume("example_resume.pdf")  # Replace with actual file
        print(f"   Resume ID: {resume['id']}")
        resume_id = resume['id']
    except FileNotFoundError:
        print("   ⚠️  Resume file not found. Using example resume ID.")
        resume_id = "00000000-0000-0000-0000-000000000001"
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Example 2: Create job description
    print("\n2. Creating job description...")
    jd_text = """
    Senior Software Engineer
    
    We are looking for a Senior Software Engineer with experience in:
    - Python, FastAPI, PostgreSQL
    - Azure cloud services
    - Terraform and infrastructure as code
    - Microservices architecture
    
    Requirements:
    - 5+ years of software development experience
    - Strong problem-solving skills
    - Experience with CI/CD pipelines
    """
    
    try:
        jd = create_job_description("linkedin", jd_text)
        print(f"   JD ID: {jd['id']}")
        print(f"   Extracted signals: {json.dumps(jd['extracted_signals'], indent=2)}")
        jd_id = jd['id']
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Example 3: Compile variants
    print("\n3. Compiling resume variants...")
    personas = ["ic", "architect", "hybrid"]
    platforms = ["linkedin", "indeed", "dice"]
    
    for persona in personas:
        for platform in platforms:
            try:
                variant = compile_variant(resume_id, jd_id, persona, platform)
                scores = variant.get('scores', {})
                survivability = scores.get('survivability', 0) * 100
                print(f"   {persona.upper()} - {platform.upper()}: {survivability:.0f}% survivability")
            except Exception as e:
                print(f"   ❌ Error compiling {persona}-{platform}: {e}")
    
    print("\n✅ Example complete!")
    print(f"   View API docs at: {BASE_URL}/docs")


if __name__ == "__main__":
    main()
