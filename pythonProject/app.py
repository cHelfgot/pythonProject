import os
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(os.environ.get("SURVEY_DATABASE", BASE_DIR / "survey.db"))

app = Flask(__name__)


def get_database() -> sqlite3.Connection:
    database = sqlite3.connect(DATABASE_PATH)
    database.row_factory = sqlite3.Row
    return database


def initialize_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_database() as database:
        database.execute(
            """
            CREATE TABLE IF NOT EXISTS survey_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                understanding_rating INTEGER NOT NULL CHECK (understanding_rating BETWEEN 1 AND 5),
                resolution_rating INTEGER NOT NULL CHECK (resolution_rating BETWEEN 1 AND 5),
                wait_time_rating INTEGER NOT NULL CHECK (wait_time_rating BETWEEN 1 AND 5),
                feedback TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@app.get("/")
def survey():
    return render_template("survey.html")


@app.post("/api/survey")
def submit_survey():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "לא התקבלו נתוני סקר תקינים"}), 400

    rating_fields = (
        "understanding_rating",
        "resolution_rating",
        "wait_time_rating",
    )
    ratings = {}
    for field in rating_fields:
        value = data.get(field)
        if isinstance(value, bool):
            return jsonify({"error": "יש לדרג את כל שאלות החובה בסולם 1 עד 5"}), 400
        try:
            rating = int(value)
        except (TypeError, ValueError):
            return jsonify({"error": "יש לדרג את כל שאלות החובה בסולם 1 עד 5"}), 400
        if rating < 1 or rating > 5:
            return jsonify({"error": "הדירוג חייב להיות בין 1 ל־5"}), 400
        ratings[field] = rating

    feedback = data.get("feedback", "")
    if not isinstance(feedback, str):
        return jsonify({"error": "ההערה אינה תקינה"}), 400
    feedback = feedback.strip()
    if len(feedback) > 1000:
        return jsonify({"error": "ניתן לכתוב עד 1,000 תווים בהערה"}), 400

    with get_database() as database:
        cursor = database.execute(
            """
            INSERT INTO survey_responses (
                understanding_rating,
                resolution_rating,
                wait_time_rating,
                feedback
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                ratings["understanding_rating"],
                ratings["resolution_rating"],
                ratings["wait_time_rating"],
                feedback or None,
            ),
        )

    return jsonify({"success": True, "response_id": cursor.lastrowid}), 201


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


initialize_database()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)
