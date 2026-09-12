import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from services.agent import run_agent
from services.search import search_internships
from services.evaluator import evaluate_internship
from services.ranker import rank_internships
from services.tracker import (
    save_tracked_internship,
    get_tracked_internships,
    update_internship_status,
    remove_tracked_internship,
)


load_dotenv()


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "FLASK_SECRET_KEY",
    "internpilot-dev-secret"
)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# AI AGENT
# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "success": False,
            "error": "Please enter a message."
        }), 400

    response = run_agent(message)

    return jsonify({
        "success": True,
        "response": response
    })


# ============================================================
# INTERNSHIP SEARCH
# ============================================================

@app.route("/api/search", methods=["POST"])
def search():

    data = request.get_json(silent=True) or {}

    role = data.get(
        "role",
        "software engineering"
    ).strip()

    location = data.get(
        "location",
        "India"
    ).strip()

    skills = data.get(
        "skills",
        []
    )

    if not isinstance(skills, list):
        skills = []

    if not role:
        role = "software engineering"

    if not location:
        location = "India"

    results = search_internships(
        role=role,
        location=location,
        experience="student",
        skills=skills,
        max_results=8
    )

    return jsonify({
        "success": True,
        "count": len(results),
        "results": results
    })


# ============================================================
# EVALUATE INTERNSHIP
# ============================================================

@app.route("/api/evaluate", methods=["POST"])
def evaluate():

    data = request.get_json(silent=True) or {}

    internship = data.get("internship", {})
    student_profile = data.get("student_profile", {})

    if not internship:
        return jsonify({
            "success": False,
            "error": "Internship data is required."
        }), 400

    result = evaluate_internship(
        internship,
        student_profile
    )

    return jsonify({
        "success": True,
        "evaluation": result
    })


# ============================================================
# SEARCH + EVALUATE + RANK
# ============================================================

@app.route("/api/recommend", methods=["POST"])
def recommend():

    data = request.get_json(silent=True) or {}

    role = data.get(
        "role",
        "software engineering"
    ).strip()

    location = data.get(
        "location",
        "India"
    ).strip()

    student_profile = data.get(
        "student_profile",
        {}
    )

    if not isinstance(student_profile, dict):
        student_profile = {}

    skills = student_profile.get(
        "skills",
        []
    )

    if not isinstance(skills, list):
        skills = []

    if not role:
        role = "software engineering"

    if not location:
        location = "India"

    # --------------------------------------------------------
    # STEP 1: Search
    # --------------------------------------------------------

    internships = search_internships(
        role=role,
        location=location,
        experience="student",
        skills=skills,
        max_results=8
    )

    if not internships:
        return jsonify({
            "success": True,
            "count": 0,
            "results": [],
            "message": "No internships found."
        })

    # --------------------------------------------------------
    # STEP 2: Evaluate
    # --------------------------------------------------------

    evaluated = []

    for internship in internships:

        evaluation = evaluate_internship(
            internship,
            student_profile
        )

        evaluated.append(evaluation)

    # --------------------------------------------------------
    # STEP 3: Rank
    # --------------------------------------------------------

    ranked = rank_internships(
        evaluated
    )

    return jsonify({
        "success": True,
        "count": len(ranked),
        "results": ranked
    })


# ============================================================
# TRACKER - GET
# ============================================================

@app.route("/api/tracker", methods=["GET"])
def tracker():

    internships = get_tracked_internships()

    return jsonify({
        "success": True,
        "count": len(internships),
        "results": internships
    })


# ============================================================
# TRACKER - SAVE
# ============================================================

@app.route("/api/tracker", methods=["POST"])
def track():

    data = request.get_json(silent=True) or {}

    internship = data.get(
        "internship",
        {}
    )

    if not internship:
        return jsonify({
            "success": False,
            "error": "Internship data is required."
        }), 400

    saved = save_tracked_internship(
        internship
    )

    if saved:

        return jsonify({
            "success": True,
            "message": "Internship saved successfully."
        })

    return jsonify({
        "success": False,
        "message": "Internship is already being tracked."
    })


# ============================================================
# TRACKER - UPDATE STATUS
# ============================================================

@app.route("/api/tracker/status", methods=["PUT"])
def tracker_status():

    data = request.get_json(silent=True) or {}

    url = data.get(
        "url",
        ""
    ).strip()

    status = data.get(
        "status",
        "Saved"
    ).strip()

    if not url:
        return jsonify({
            "success": False,
            "error": "Internship URL is required."
        }), 400

    allowed_statuses = [
        "Saved",
        "Applied",
        "Interview",
        "Rejected",
        "Offer"
    ]

    if status not in allowed_statuses:

        return jsonify({
            "success": False,
            "error": "Invalid status."
        }), 400

    updated = update_internship_status(
        url,
        status
    )

    if not updated:

        return jsonify({
            "success": False,
            "error": "Internship not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "Status updated successfully."
    })


# ============================================================
# TRACKER - DELETE
# ============================================================

@app.route("/api/tracker", methods=["DELETE"])
def delete_tracker():

    data = request.get_json(silent=True) or {}

    url = data.get(
        "url",
        ""
    ).strip()

    if not url:
        return jsonify({
            "success": False,
            "error": "Internship URL is required."
        }), 400

    removed = remove_tracked_internship(
        url
    )

    if not removed:

        return jsonify({
            "success": False,
            "error": "Internship not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "Internship removed successfully."
    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print("\n===================================")
    print("        InternPilot AI")
    print("===================================")
    print("         Server Starting...")
    print("===================================\n")

    app.run(
        debug=False,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )