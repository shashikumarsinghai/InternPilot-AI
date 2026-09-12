import os
from dotenv import load_dotenv

from strands import Agent, tool
from strands.models.mistral import MistralModel

from services.search import search_internships


load_dotenv()


# ============================================================
# TOOL 1: SEARCH INTERNSHIPS
# ============================================================

@tool
def find_internships(
    role: str = "software engineering",
    location: str = "India"
) -> str:
    """
    Search the web for current internship opportunities.

    Args:
        role: The internship role the student is looking for.
        location: The preferred internship location.

    Returns:
        Internship search results with title, URL and description.
    """

    results = search_internships(
        role=role,
        location=location,
        experience="student",
        max_results=8
    )

    if not results:
        return "No internship opportunities were found."

    formatted_results = []

    for index, item in enumerate(results, start=1):
        formatted_results.append(
            f"""
INTERNSHIP {index}
Title: {item.get("title", "Unknown")}
URL: {item.get("url", "N/A")}
Relevance Score: {item.get("score", 0)}
Description: {item.get("content", "No description available")}
"""
        )

    return "\n".join(formatted_results)


# ============================================================
# STRANDS AGENT
# ============================================================

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError(
        "MISTRAL_API_KEY is missing from your .env file."
    )


model = MistralModel(
    api_key=MISTRAL_API_KEY,
    model_id="ministral-3b-2512",
    temperature=0.2,
    max_tokens=2000
)


SYSTEM_PROMPT = """
You are InternPilot AI, an intelligent internship assistant for students.

Your job is to help students discover and evaluate internship opportunities.

You can:

1. Search for current internship opportunities.
2. Understand the student's requested role and location.
3. Explain why an internship may be useful.
4. Compare internship opportunities.
5. Give clear, structured recommendations.

IMPORTANT RULES:

- Never invent an internship.
- Use the search tool when the user asks for internships.
- Prefer current web search results.
- Clearly provide internship titles and URLs.
- Do not claim that a student is eligible unless enough information is available.
- If important student information is missing, mention what information would improve the recommendation.
- Keep responses practical and student-friendly.

Your goal is to reduce the time students spend searching for internships.
"""


agent = Agent(
    model=model,
    tools=[find_internships],
    system_prompt=SYSTEM_PROMPT
)


# ============================================================
# MAIN FUNCTION
# ============================================================

def run_agent(user_request: str) -> str:
    """
    Send a request to InternPilot AI and return the agent response.
    """

    if not user_request or not user_request.strip():
        return "Please tell me what kind of internship you are looking for."

    try:
        response = agent(user_request)

        return str(response)

    except Exception as e:
        print(f"Agent error: {e}")
        return (
            "Sorry, I could not process your request right now. "
            "Please try again."
        )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("\n===================================")
    print("       InternPilot AI Agent")
    print("===================================\n")

    print("Testing Strands Agent...\n")

    result = run_agent(
        "Find software engineering internships "
        "for students in India."
    )

    print("\nAgent Response:\n")
    print(result)