import os
import sys
import json
import random
import webbrowser
import threading
from flask import Flask, render_template, request, redirect

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static")
)

FILE_NAME = "candidates.json"

def load_candidates():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_candidates(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

def convert_experience(exp_input):
    exp_input = exp_input.lower().strip()

    if exp_input == "na":
        return "NA"

    parts = exp_input.split()
    if len(parts) != 2:
        return None

    try:
        number = float(parts[0])
    except ValueError:
        return None

    unit = parts[1]

    if unit in ["year", "years"]:
        return number * 12
    elif unit in ["month", "months"]:
        return number
    return None

def coding_average(candidate):
    return round(
        (candidate["leetcode"] + candidate["codechef"] + candidate["hackerrank"]) / 3,
        2
    )

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add", methods=["GET", "POST"])
def add_candidate():
    if request.method == "POST":
        candidates = load_candidates()

        exp_input = request.form["experience"]
        experience = convert_experience(exp_input)

        if experience is None:
            return "Invalid Experience Format (Use: 2 years / 6 months / NA)"

        while True:
            app_id = random.randint(1000, 9999)
            if all(c["id"] != app_id for c in candidates):
                break

        candidate = {
            "id": app_id,
            "name": request.form["name"].strip(),
            "class10": float(request.form["class10"]),
            "class12": float(request.form["class12"]),
            "cgpa": float(request.form["cgpa"]),
            "projects": int(request.form["projects"]),
            "hackathons_count": int(request.form["hackathons_count"]),
            "hackathon_position": request.form["hackathon_position"].lower(),
            "leetcode": int(request.form["leetcode"]),
            "codechef": int(request.form["codechef"]),
            "hackerrank": int(request.form["hackerrank"]),
            "skills": [s.strip().lower() for s in request.form["skills"].split(",") if s.strip()],
            "experience": experience,
            "experience_input": exp_input
        }

        candidates.append(candidate)
        save_candidates(candidates)
        return redirect("/view")

    return render_template("add.html")

@app.route("/view")
def view():
    candidates = load_candidates()
    for c in candidates:
        c["coding_avg"] = coding_average(c)
    return render_template("view.html", candidates=candidates)

@app.route("/search", methods=["GET", "POST"])
def search():
    candidates = load_candidates()
    result = None
    results = []
    message = None

    if request.method == "POST":
        search_type = request.form["search_type"]
        search_value = request.form["search_value"].strip()

        if search_type == "id":
            try:
                app_id = int(search_value)
                result = next((c for c in candidates if c["id"] == app_id), None)
                if result:
                    result["coding_avg"] = coding_average(result)
                else:
                    message = "Candidate Not Found"
            except ValueError:
                message = "Invalid Application ID"

        elif search_type == "name":
            results = [
                c for c in candidates
                if search_value.lower() in c["name"].lower()
            ]
            for c in results:
                c["coding_avg"] = coding_average(c)

            if not results:
                message = "No Candidate Found With That Name"

    return render_template("search.html", result=result, results=results, message=message)

@app.route("/filter", methods=["GET", "POST"])
def filter_candidates():
    candidates = load_candidates()
    selected = []
    rejected = 0
    report = None

    if request.method == "POST":
        min_class10 = float(request.form["min_class10"])
        min_class12 = float(request.form["min_class12"])
        min_cgpa = float(request.form["min_cgpa"])
        min_projects = int(request.form["min_projects"])
        min_hackathons = int(request.form["min_hackathons"])
        winner_required = request.form["winner_required"].lower()
        min_coding_score = float(request.form["min_coding_score"])
        required_skills = [s.strip().lower() for s in request.form["skills"].split(",") if s.strip()]

        min_exp = convert_experience(request.form["min_exp"])
        if min_exp is None:
            return "Invalid Experience Format in Filter"

        for c in candidates:
            avg_score = coding_average(c)
            skill_match_count = sum(1 for s in required_skills if s in c["skills"])

            academic_ok = (
                c["class10"] >= min_class10 and
                c["class12"] >= min_class12 and
                c["cgpa"] >= min_cgpa
            )

            project_ok = c["projects"] >= min_projects
            hackathon_ok = c["hackathons_count"] >= min_hackathons
            winner_ok = (winner_required == "no" or c["hackathon_position"] == "winner")
            coding_ok = avg_score >= min_coding_score
            skill_ok = (not required_skills or skill_match_count > 0)
            exp_ok = (min_exp == "NA" or (c["experience"] != "NA" and c["experience"] >= min_exp))

            if academic_ok and project_ok and hackathon_ok and winner_ok and coding_ok and skill_ok and exp_ok:
                c["skill_match_count"] = skill_match_count
                c["exp_months"] = 0 if c["experience"] == "NA" else c["experience"]
                c["coding_avg"] = avg_score
                selected.append(c)
            else:
                rejected += 1

        selected.sort(
            key=lambda x: (x["cgpa"], x["skill_match_count"], x["exp_months"], x["coding_avg"]),
            reverse=True
        )

        report = {
            "total": len(candidates),
            "selected": len(selected),
            "rejected": rejected
        }

    return render_template("filter.html", selected=selected, report=report)

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)