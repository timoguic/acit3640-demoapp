import random
import uuid
from pathlib import Path

from flask import Flask, render_template

import checks
from config import DATABASE_URL, SHARED_FOLDER_PATH
from db import db
from models import Student

app = Flask(__name__, instance_path=Path(".").resolve())

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

if not DATABASE_URL.startswith("sqlite"):
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"connect_args": {"connect_timeout": 2}}

db.init_app(app)


@app.context_processor
def inject_config():
    return dict(db_url=DATABASE_URL, shared_folder=Path(SHARED_FOLDER_PATH).resolve())


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/create_record", methods=["POST"])
def create_record():
    name = f"Student {random.randint(1000, 9999)}"
    student_id = "A" + "".join([str(random.randint(0, 9)) for _ in range(7)])
    student = Student(name=name, student_id=student_id)
    db.session.add(student)
    db.session.commit()
    return render_template(
        "base.html", messages=[(f"Student {student_id} created", "OK!")]
    )


@app.route("/create_tables", methods=["POST"])
def create_tables():
    db.create_all()
    return render_template("base.html", messages=[("Database created", "OK!")])


@app.route("/create_files", methods=["POST"])
def create_file():
    path = Path(SHARED_FOLDER_PATH)
    contents = str(random.randint(1000, 9999))
    filename = f"{uuid.uuid4()}.acit3640"
    with open(path / filename, "w") as fp:
        fp.write(contents)

    return render_template("base.html", messages=[(f"File {filename} created", "OK!")])


@app.route("/", methods=["POST"])
def check():
    messages = []
    funcs = [
        ("Database connection", checks.db_connection),
        ("Tables", checks.check_tables),
        ("Data", checks.check_data),
        ("Shared folder", checks.check_files),
        ("Check files", checks.list_files),
    ]

    messages = [(label, func()) for label, func in funcs]

    return render_template("base.html", messages=messages)


if __name__ == "__main__":
    app.run(debug=True, port=5123)
