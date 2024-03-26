import random
import uuid

from pathlib import Path

from flask import Flask, render_template

from checks import get_checks_output

from config import DATABASE_URL, SHARED_FOLDER_PATH, HOSTNAME
from db import db
from models import Student

app = Flask(__name__, instance_path=Path(".").resolve())

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

if not DATABASE_URL.startswith("sqlite"):
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"connect_args": {"connect_timeout": 2}}

db.init_app(app)


@app.context_processor
def inject_config():
    return dict(
        hostname=HOSTNAME,
        db_url=DATABASE_URL,
        shared_folder=Path(SHARED_FOLDER_PATH).resolve(),
        checks=get_checks_output(),
    )

@app.route("/create_record", methods=["POST"])
def create_record():
    name = f"Student {random.randint(1000, 9999)}"
    student_id = "A" + "".join([str(random.randint(0, 9)) for _ in range(7)])
    try:
        student = Student(name=name, student_id=student_id)
        db.session.add(student)
        db.session.commit()
        message = (f"Student {student_id} created", "OK!")
    except Exception as e:
        message = (f"Failed to create student {student_id}!", str(e))
    
    return render_template("base.html", message=message)


@app.route("/create_tables", methods=["POST"])
def create_tables():
    db.create_all()
    return render_template("base.html", messages=[("Database created", "OK!")])


@app.route("/create_files", methods=["POST"])
def create_file():
    path = Path(SHARED_FOLDER_PATH)
    contents = str(random.randint(1000, 9999))
    filename = f"{uuid.uuid4()}.acit3640"
    try:
        with open(path / filename, "w") as fp:
            fp.write(contents)
        message = (f"File {filename} created", "OK!")
    except Exception as e:
        message = (f"Failed to create file {filename}!", str(e))

    return render_template("base.html", message=message)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True, port=5123)
