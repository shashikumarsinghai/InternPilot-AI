def rank_internships(evaluated_internships):
    """
    Rank evaluated internships from best match to lowest match.
    """

    ranked = sorted(
        evaluated_internships,
        key=lambda item: item.get("match_score", 0),
        reverse=True
    )

    for position, internship in enumerate(ranked, start=1):
        internship["rank"] = position

    return ranked


if __name__ == "__main__":

    sample_results = [
        {
            "title": "Python Developer Intern",
            "match_score": 70
        },
        {
            "title": "AI/ML Intern",
            "match_score": 92
        },
        {
            "title": "Frontend Developer Intern",
            "match_score": 61
        }
    ]

    results = rank_internships(sample_results)

    print("\n===================================")
    print("       Ranked Internships")
    print("===================================\n")

    for internship in results:
        print(
            f"#{internship['rank']} "
            f"{internship['title']} "
            f"({internship['match_score']}%)"
        )