import json
import os
from datetime import datetime


TRACKER_FILE = "tracked_internships.json"


def load_tracked_internships():
    """Load saved internships from the tracker file."""

    if not os.path.exists(TRACKER_FILE):
        return []

    try:
        with open(TRACKER_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_tracked_internship(internship):
    """Save an internship to the tracking list."""

    tracked = load_tracked_internships()

    # Prevent duplicate internships
    existing_urls = {
        item.get("url")
        for item in tracked
    }

    if internship.get("url") in existing_urls:
        return False

    internship_data = {
        "title": internship.get("title", "Unknown Internship"),
        "url": internship.get("url", ""),
        "match_score": internship.get("match_score", 0),
        "status": "Saved",
        "saved_at": datetime.now().isoformat()
    }

    tracked.append(internship_data)

    with open(TRACKER_FILE, "w", encoding="utf-8") as file:
        json.dump(
            tracked,
            file,
            indent=4,
            ensure_ascii=False
        )

    return True


def update_internship_status(url, status):
    """Update the status of a tracked internship."""

    tracked = load_tracked_internships()

    for internship in tracked:

        if internship.get("url") == url:
            internship["status"] = status

            with open(
                TRACKER_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    tracked,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return True

    return False


def get_tracked_internships():
    """Return all tracked internships."""

    return load_tracked_internships()


def remove_tracked_internship(url):
    """Remove an internship from the tracker."""

    tracked = load_tracked_internships()

    updated = [
        internship
        for internship in tracked
        if internship.get("url") != url
    ]

    if len(updated) == len(tracked):
        return False

    with open(
        TRACKER_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            updated,
            file,
            indent=4,
            ensure_ascii=False
        )

    return True


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    sample_internship = {
        "title": "AI/ML Intern",
        "url": "https://example.com/ai-intern",
        "match_score": 92
    }

    print("\n===================================")
    print("       Internship Tracker")
    print("===================================\n")

    saved = save_tracked_internship(
        sample_internship
    )

    print(f"Saved: {saved}")

    print("\nTracked internships:\n")

    for internship in get_tracked_internships():
        print(
            f"{internship['title']} | "
            f"{internship['status']} | "
            f"{internship['match_score']}%"
        )