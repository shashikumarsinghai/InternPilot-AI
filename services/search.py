import os
import re

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing from your .env file.")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def detect_location(title, content, requested_location):
    text = f"{title} {content}".lower()

    if "remote" in text:
        return "Remote"

    requested_location = requested_location.strip()

    if requested_location and requested_location.lower() in text:
        return requested_location

    indian_cities = [
        "delhi",
        "noida",
        "greater noida",
        "gurgaon",
        "gurugram",
        "bangalore",
        "bengaluru",
        "mumbai",
        "pune",
        "hyderabad",
        "chennai",
        "kolkata",
        "jaipur",
        "ahmedabad",
        "lucknow",
        "chandigarh",
        "indore",
        "bhopal",
        "kochi",
    ]

    for city in indian_cities:
        if city in text:
            return city.title()

    if "india" in text:
        return "India"

    return "Unknown"


def is_useful_internship_result(title, content, url=""):
    """
    Filter out generic articles, list pages, guides and
    pages that are unlikely to represent an actual internship.
    """

    title_text = str(title).lower().strip()
    content_text = str(content).lower().strip()
    url_text = str(url).lower().strip()

    text = f"{title_text} {content_text}"

    # Clearly generic / informational pages
    unwanted_patterns = [
        "internship ideas",
        "best internships",
        "top internships",
        "how to get an internship",
        "how to land a",
        "internship guide",
        "internship tips",
        "career advice",
        "internship opportunities for students",
        "internship programs list",
        "internship list",
        "internships list",
        "top 3 internships",
        "application process",
        "eligibility, skills",
        "free certificate",
        "certificate & apply",
    ]

    if any(pattern in title_text for pattern in unwanted_patterns):
        return False

    # Generic job/list pages
    generic_title_patterns = [
        "machine learning intern jobs",
        "ai and ml internship jobs",
        "ai/ml internship jobs",
        "internship job vacancies",
        "internship jobs and vacancies",
        "internship jobs in india",
        "internship vacancies",
        "jobs in india",
        "job vacancies",
        "job listings",
        "job search",
        "browse internships",
        "browse jobs",
        "internships & fresher roles",
    ]

    if any(pattern in title_text for pattern in generic_title_patterns):
        return False

    # Generic article/list pages based on URL
    generic_url_patterns = [
        "/career-advice/",
        "/career-advice",
        "/blog/",
        "/blog",
        "/guides/",
        "/guide/",
        "/article/",
        "/articles/",
    ]

    if any(pattern in url_text for pattern in generic_url_patterns):
        return False

    # Very strong signal that the page is informational rather than a posting
    article_patterns = [
        "how to apply",
        "how to get",
        "how to land",
        "eligibility criteria",
        "application process",
        "internship tips",
        "internship guide",
        "career guide",
    ]

    if any(pattern in title_text for pattern in article_patterns):
        return False

    return True


def build_search_query(role, location, skills=None, experience="student"):
    """
    Build a search query dynamically from the user's requirements.
    """

    role = role.strip()
    location = location.strip()

    query_parts = [
        f"{role} internship"
    ]

    if skills:
        cleaned_skills = [
            str(skill).strip()
            for skill in skills
            if str(skill).strip()
        ]

        if cleaned_skills:
            query_parts.append(
                " ".join(cleaned_skills)
            )

    if experience:
        query_parts.append(experience)

    if location:
        query_parts.append(location)

    query_parts.append("2026")

    return " ".join(query_parts)


def search_internships(
    role="software engineering",
    location="India",
    experience="student",
    skills=None,
    max_results=8
):
    """
    Search for current internship opportunities using Tavily.

    Supports any role and any skills supplied by the user.
    """

    query = build_search_query(
        role=role,
        location=location,
        skills=skills,
        experience=experience
    )

    print(f"\nSearch Query: {query}")

    try:
        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results * 3,
            include_answer=False,
            include_raw_content=False,
        )

    except Exception as e:
        print(f"Search error: {e}")
        return []

    results = []

    for item in response.get("results", []):

        title = str(
            item.get("title", "")
        ).strip()

        content = str(
            item.get("content", "")
        ).strip()

        url = str(
            item.get("url", "")
        ).strip()

        score = item.get("score", 0)

        if not title or not url:
            continue

        if not is_useful_internship_result(
            title,
            content,
            url
        ):
            continue

        internship_location = detect_location(
            title,
            content,
            location
        )

        results.append({
            "title": title,
            "content": content,
            "url": url,
            "score": score,
            "location": internship_location,
        })

        if len(results) >= max_results:
            break

    return results


if __name__ == "__main__":

    print("\n===================================")
    print("      InternPilot AI Search")
    print("===================================\n")

    test_results = search_internships(
        role="data science",
        location="India",
        experience="student",
        skills=[
            "Python",
            "Pandas",
            "SQL"
        ],
        max_results=8
    )

    print(
        f"\nFound {len(test_results)} results:\n"
    )

    for index, internship in enumerate(
        test_results,
        start=1
    ):
        print(
            f"{index}. "
            f"{internship['title']}"
        )

        print(
            f"   Location: "
            f"{internship['location']}"
        )

        print(
            f"   URL: "
            f"{internship['url']}"
        )

        print(
            f"   Score: "
            f"{internship['score']}"
        )

        print()