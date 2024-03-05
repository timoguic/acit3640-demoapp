from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from db import db


class Student(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(80))
    student_id = mapped_column(String(80))
