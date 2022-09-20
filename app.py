from datetime import datetime
from flask import request, abort
from flask_api import status
from flask_restful import Resource
from settings import app, api
from models import TasksToDo, db
from arguments import task_put_args, task_delete_args, task_patch_args


class ToDoList(Resource):
    def __init__(self):
        self.user_name, self.task_id = request.args.get("user_name", ""), request.args.get("id", "")

    def get(self):
        """
        ---
        properties:
          - in: path
            name: username
            type: string
            required: false
          - in: path
            name: task_id
            type: integer
            required: false
        responses:
          200:
            description: Tasks (all or by user_name or/and by task_id)
            schema:
              id: Tasks
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
                title:
                  type: string
                  description: The title of the task
                  default: Buy a bread
                id:
                  type: integer
                  description: The id of the task
                  default: 1
                description:
                  type: string
                  description: The description of the task
                  default: Buy bread in a supermarket
                responsible:
                  type: string
                  description: The responsible for the task
                  default: Steven Wilson
                creation_time:
                  type: string
                  description: The day of creation of the task
                  default: 2022-09-17 17:12:25.278511
          404:
            description: Task(s) not found
            schema:
              id: Error_404
              properties:
                error:
                  type: string
                  description: Error 404
                  default: Task(s) not found
        """
        tasks = self._get_tasks()
        self._is_exist_in_db(tasks)
        result = self._prepare_task_to_show(tasks)
        return result, status.HTTP_200_OK

    def _get_tasks(self):
        if self.user_name:
            tasks = TasksToDo.query.filter_by(user_name=self.user_name).all()
        elif self.task_id:
            tasks = TasksToDo.query.filter_by(id=self.task_id).all()
        elif self.user_name and self.task_id:
            tasks = TasksToDo.query.filter_by(id=self.task_id, user_name=self.user_name).all()
        else:
            tasks = TasksToDo.query.all()
        return tasks

    def put(self):
        """
        ---
        parameters:
        - in: body
          name: task
          description: The task to create.
          schema:
            type: object
            required:
              - user_name
              - title
              - description
              - responsible
            properties:
              user_name:
                type: string
                description: The name of the user
                default: Steven Wilson
              title:
                type: string
                description: The title of the task
                default: Buy bread
              description:
                type: string
                description: The description of the task
                default: Buy bread in a supermarket
              responsible:
                type: string
                description: The responsible for the task
                default: Steven Wilson
        responses:
          200:
            description: Task has been created
            schema:
              id: Task has been created
              properties:
                result:
                  type: string
                  description: <PUT Task has been created>
                  default: <PUT Task has been created>
        """
        args = task_put_args.parse_args()
        self._create_task(args)
        return {"result": "<PUT Task has been created>"}, status.HTTP_200_OK

    @staticmethod
    def _create_task(args):
        user_name, title, description = args["user_name"], args["title"], args["description"]
        responsible = args["responsible"]
        task = TasksToDo(user_name, title, description, responsible, datetime.now())
        db.session.add(task)
        db.session.commit()

    def delete(self):
        """
        ---
        parameters:
        - in: body
          name: task
          description: Task to delete.
          schema:
            type: object
            required:
              - user_name
              - task_id
            properties:
              user_name:
                type: string
                description: The name for the user
                default: Steven Wilson
              task_id:
                type: integer
                description: The id for the task
                default: 1
        responses:
          200:
            description: Task has been deleted
            schema:
              id: Task has been deleted
              properties:
                result:
                  type: string
                  description: <DELETE Task has been deleted>
                  default: <DELETE Task has been deleted>
          404:
            description: Task(s) not found
            schema:
              id: Error_404
              properties:
                error:
                  type: string
                  description: Error 404
                  default: Task(s) not found
        """
        args = task_delete_args.parse_args()
        self._delete_task(args)
        return {"result": "<DELETE Task has been deleted>"}, status.HTTP_200_OK

    def _delete_task(self, args):
        if args["id"]:
            task = TasksToDo.query.filter_by(id=args["id"], user_name=args["user_name"]).first()
        else:
            task = TasksToDo.query.filter_by(user_name=args["user_name"]).first()
        self._is_exist_in_db(task)
        db.session.delete(task)
        db.session.commit()

    def patch(self):
        """
        ---
        parameters:
        - in: body
          name: task
          description: Task to update.
          schema:
            type: object
            required:
              - user_name
              - task_id
            properties:
              user_name:
                type: string
                description: The name for the user
                default: Steven Wilson
              task_id:
                type: integer
                description: The id for the task
                default: 1
              title:
                type: string
                description: The title of the task
                default: Buy bread
              description:
                type: string
                description: The description of the task
                default: Buy bread in a supermarket
              responsible:
                type: string
                description: The responsible for the task
                default: Steven Wilson
        responses:
          200:
            description: Task has been updated
            schema:
              id: Task has been updated
              properties:
                result:
                  type: string
                  description: <PATCH Task has been updated>
                  default: <PATCH Task has been updated>
          404:
            description: Task(s) not found
            schema:
              id: Error_404
              properties:
                error:
                  type: string
                  description: Error 404
                  default: Task(s) not found
        """
        args = task_patch_args.parse_args()
        self._update_task(args)
        return {"result": "<PATCH Task has been updated>"}, status.HTTP_200_OK

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
            abort(status.HTTP_404_NOT_FOUND, {"error": "Task(s) not found"})


api.add_resource(ToDoList, "/todolist")

if __name__ == "__main__":
    app.run()
