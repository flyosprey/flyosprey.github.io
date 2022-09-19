from settings import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class TasksToDo(db.Model):
    id = db.Column("task_id", db.Integer, primary_key=True)
    user_name = db.Column("user_id", db.String, nullable=False)
    title = db.Column("task_title", db.String, nullable=False)
    description = db.Column("task_description", db.String(200), nullable=True)
    responsible = db.Column("responsible_of_task", db.String(120), nullable=True)
    creation_time = db.Column("creation_time", db.DateTime, nullable=False)

    def __init__(self, user_name, title, description, responsible, creation_time):
        self.user_name = user_name
        self.title = title
        self.description = description
        self.responsible = responsible
        self.creation_time = creation_time
