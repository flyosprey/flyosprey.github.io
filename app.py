from flask import request, abort
from flask_api import status
from flask_restful import Resource
from datetime import datetime
from settings import app, api
from models import TasksToDo, db
from arguments import task_put_args, task_delete_args, task_patch_args


class ToDoList(Resource):
    def __init__(self):
        self.user_name, self.task_id = request.args.get("user_name", ""), request.args.get("id", "")

    def get(self):
        tasks = self._get_tasks()
        self._is_exist_in_db(tasks)
        result = self._prepare_task_to_show(tasks)
        return result, status.HTTP_200_OK

    def _get_tasks(self):
        tasks = None
        if self.user_name:
            tasks = TasksToDo.query.filter_by(user_name=self.user_name).all()
        elif self.task_id:
            tasks = TasksToDo.query.filter_by(id=self.task_id).all()
        elif self.user_name and self.task_id:
            tasks = TasksToDo.query.filter_by(id=self.task_id, user_name=self.user_name).all()
        return tasks

    def put(self):
        args = task_put_args.parse_args()
        self._create_task(args)
        return "<POST Task has been created>", status.HTTP_200_OK

    @staticmethod
    def _create_task(args):
        user_name, title, description = args["user_name"], args["title"], args["description"]
        responsible = args["responsible"]
        task = TasksToDo(user_name, title, description, responsible, datetime.now())
        db.session.add(task)
        db.session.commit()

    def delete(self):
        args = task_delete_args.parse_args()
        self._delete_task(args)
        return "<DELETE task has been deleted>", status.HTTP_200_OK

    def _delete_task(self, args):
        if args["id"]:
            task = TasksToDo.query.filter_by(id=args["id"], user_name=args["user_name"]).first()
        else:
            task = TasksToDo.query.filter_by(user_name=args["user_name"]).first()
        self._is_exist_in_db(task)
        db.session.delete(task)
        db.session.commit()

    def patch(self):
        args = task_patch_args.parse_args()
        self._update_task(args)
        return "<PATCH Task has been updated>", status.HTTP_200_OK

    def _update_task(self, args):
        task = TasksToDo.query.filter_by(id=args["id"], user_name=args["user_name"])
        self._is_exist_in_db(task.first())
        task.update(args)
        db.session.commit()

    @staticmethod
    def _prepare_task_to_show(tasks) -> dict:
        result = {"result": []}
        for task in tasks:
            task_to_show = {"id": task.id, "user_name": task.user_name, "title": task.title,
                            "description": task.description, "responsible": task.responsible,
                            "creation_time": str(task.creation_time)}
            result["result"].append(task_to_show)
        return result

    @staticmethod
    def _is_exist_in_db(obj):
        if not obj:
            abort(status.HTTP_404_NOT_FOUND, "There are no required tasks")


api.add_resource(ToDoList, "/todolist")

if __name__ == "__main__":
    app.run()
