import os
import json

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY is missing from your .env file.")

client = Mistral(api_key=MISTRAL_API_KEY)


def extract_required_skills(title, description):
    """
    Use Mistral to identify the skills actually required
    by an internship, regardless of the role.
    """

    text = f"""
Internship Title:
{title}

Internship Description:
{description}
"""

    prompt = f"""
You are an expert technical recruiter.

Analyze the internship information below and identify the
technical and professional skills that are actually relevant
to the internship.

{ text }

Rules:
- Extract skills only from the provided information.
- Do not invent skills.
- Support ANY internship role.
- Skills can include programming languages, frameworks,
  libraries, databases, cloud platforms, tools, technologies,
  software, methodologies, and relevant professional skills.
- Return only a JSON array of strings.
- Keep skill names concise.
- If no clear skills are mentioned, return [].

Example format:
["Python", "Pandas", "SQL", "Machine Learning"]

Return ONLY valid JSON.
"""

    try:
        response = client.chat.complete(
            model="ministral-3b-2512",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300
        )

        content = response.choices[0].message.content.strip()

        # Remove accidental markdown code fences
        if content.startswith("```"):
            content = content.replace("```json", "")
            content = content.replace("```", "")
            content = content.strip()

        skills = json.loads(content)

        if not isinstance(skills, list):
            return []

        cleaned_skills = []

        for skill in skills:
            if isinstance(skill, str) and skill.strip():
                cleaned_skills.append(skill.strip())

        return cleaned_skills

    except Exception as e:
        print(f"Skill extraction error: {e}")
        return []


def evaluate_internship(internship, student_profile):

    student_skills = {
        skill.strip().lower()
        for skill in student_profile.get("skills", [])
        if isinstance(skill, str) and skill.strip()
    }

    student_location = (
        str(student_profile.get("location", ""))
        .strip()
        .lower()
    )

    student_experience = (
        str(student_profile.get("experience", ""))
        .strip()
        .lower()
    )

    title = str(internship.get("title", "")).strip()
    description = str(internship.get("content", "")).strip()
    internship_location = str(
        internship.get("location", "")
    ).strip()

    # --------------------------------------------------
    # 1. DYNAMIC SKILL DETECTION
    # --------------------------------------------------

    required_skills = extract_required_skills(
        title,
        description
    )

    required_skills_lower = {
        skill.lower(): skill
        for skill in required_skills
    }

    matched_skills = []
    missing_skills = []

    for skill_lower, original_skill in required_skills_lower.items():

        if skill_lower in student_skills:
            matched_skills.append(original_skill)

        else:
            # Also support partial matching.
            # Example:
            # student has "machine learning"
            # internship requires "machine learning"
            if any(
                skill_lower in student_skill
                or student_skill in skill_lower
                for student_skill in student_skills
            ):
                matched_skills.append(original_skill)
            else:
                missing_skills.append(original_skill)

    # --------------------------------------------------
    # 2. SKILL SCORE
    # --------------------------------------------------

    if required_skills:

        skill_score = (
            len(matched_skills)
            / len(required_skills)
        ) * 100

    else:
        # If no skills were clearly mentioned,
        # do not punish the internship.
        skill_score = 60

    # --------------------------------------------------
    # 3. LOCATION SCORE
    # --------------------------------------------------

    full_text = (
        f"{title} "
        f"{description} "
        f"{internship_location}"
    ).lower()

    is_remote = "remote" in full_text

    if is_remote:

        location_score = 100

    elif not internship_location:

        location_score = 50

    elif (
        student_location
        and (
            student_location in internship_location.lower()
            or internship_location.lower() in student_location
        )
    ):

        location_score = 100

    elif (
        student_location
        and student_location in full_text
    ):

        location_score = 100

    else:

        location_score = 40

    # --------------------------------------------------
    # 4. EXPERIENCE SCORE
    # --------------------------------------------------

    student_level_keywords = [
        "student",
        "intern",
        "internship",
        "fresher",
        "entry level",
        "entry-level",
        "graduate",
        "undergraduate",
    ]

    experience_match = any(
        keyword in full_text
        for keyword in student_level_keywords
    )

    if not student_experience:

        experience_score = 70

    elif experience_match:

        experience_score = 100

    else:

        experience_score = 60

    # --------------------------------------------------
    # 5. FINAL MATCH SCORE
    # --------------------------------------------------

    overall_score = (
        (skill_score * 0.60)
        + (location_score * 0.25)
        + (experience_score * 0.15)
    )

    overall_score = round(overall_score)

    # --------------------------------------------------
    # 6. RECOMMENDATION
    # --------------------------------------------------

    if overall_score >= 80:

        recommendation = "Excellent Match"

    elif overall_score >= 65:

        recommendation = "Good Match"

    elif overall_score >= 50:

        recommendation = "Possible Match"

    else:

        recommendation = "Low Match"

    return {
        "title": title,
        "url": internship.get("url", ""),
        "match_score": overall_score,
        "skill_score": round(skill_score),
        "location_score": round(location_score),
        "experience_score": round(experience_score),
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation,
    }


if __name__ == "__main__":

    print("\n===================================")
    print("     InternPilot AI Evaluator")
    print("===================================\n")

    sample_internship = {
        "title": "Data Science Intern",
        "content": """
        We are looking for a Data Science Intern.
        Candidates should have experience with Python,
        Pandas, SQL and Machine Learning.
        Knowledge of Power BI is a plus.
        """,
        "location": "India",
        "url": "https://example.com/data-science"
    }

    sample_student = {
        "skills": [
            "Python",
            "Pandas",
            "SQL"
        ],
        "location": "India",
        "experience": "student"
    }

    result = evaluate_internship(
        sample_internship,
        sample_student
    )

    print("Required Skills:")
    print(result["required_skills"])

    print("\nMatched Skills:")
    print(result["matched_skills"])

    print("\nMissing Skills:")
    print(result["missing_skills"])

    print("\nSkill Score:")
    print(result["skill_score"])

    print("\nOverall Match:")
    print(result["match_score"])

    print("\nRecommendation:")
    print(result["recommendation"])