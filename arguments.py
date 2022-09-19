from flask_restful import reqparse


task_put_args = reqparse.RequestParser()
task_put_args.add_argument("user_name", type=str, help="User name is required", required=True)
task_put_args.add_argument("title", type=str, help="Title of task is required", required=True)
task_put_args.add_argument("description", type=str, help="Description of task is required", required=True)
task_put_args.add_argument("responsible", type=str, help="Responsible of task is required", required=True)

task_patch_args = reqparse.RequestParser()
task_patch_args.add_argument("user_name", type=str, help="User name is required", required=True)
task_patch_args.add_argument("id", type=str, help="Task id is required", required=True)
task_patch_args.add_argument("title", type=str, help="Title of task", required=False)
task_patch_args.add_argument("description", type=str, help="Description of task", required=False)
task_patch_args.add_argument("responsible", type=str, help="Responsible of task", required=False)

task_delete_args = reqparse.RequestParser()
task_delete_args.add_argument("user_name", type=str, help="User name is required", required=True)
task_delete_args.add_argument("id", type=str, help="Id of task", required=False)