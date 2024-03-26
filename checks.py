import uuid
from pathlib import Path

from sqlalchemy import inspect

from config import SHARED_FOLDER_PATH
from db import db
from models import Student

def get_checks_output():
    funcs = [
        ("Database connection", db_connection),
        ("Tables", check_tables),
        ("Data", check_data),
        ("Shared folder", check_files),
        ("Check files", list_files),
    ]

    messages = [(label, func()) for label, func in funcs]
    return messages

def db_connection():
    try:
        db.engine.connect()
    except Exception as e:
        return str(e).strip()

    return "OK!"


def check_tables():
    try:
        data = inspect(db.engine).get_table_names()
    except Exception as e:
        return str(e).strip()

    return "\n".join([f"- {data}" for data in data]) if data else "No tables found!"


def check_data():
    try:
        records = db.session.execute(db.select(Student)).scalars()
    except Exception as e:
        return str(e).strip()

    return (
        "\n".join([f"--> {record.name} (ID {record.student_id})" for record in records])
        if records
        else "No data found!"
    )


def check_files():
    path = Path(SHARED_FOLDER_PATH)
    if not path.exists():
        return f"Path {path} does not exist!"

    if not path.is_dir():
        return f"{path} is not a directory!"

    try:
        rand_file = str(uuid.uuid4())
        with open(path / rand_file, "w") as fp:
            fp.write("Test")
        (path / rand_file).unlink()
    except Exception as e:
        return str(e).strip()

    return "OK!"


def list_files():
    path = Path(SHARED_FOLDER_PATH)
    try:
        filenames = [f"- {file}" for file in path.iterdir() if file.is_file()]
        return "\n".join(filenames) if len(filenames) else "No files found!"
    except Exception as e:
        return str(e).strip()
