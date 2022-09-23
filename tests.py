import json
import logging
import unittest
from app import app


class FlaskTest(unittest.TestCase):
    def test_put_200(self):
        data = {"user_name": "John", "title": "Go to the gym", "description": "Train chest in the gym",
                "responsible": "John"}
        tester = app.test_client(self)
        response = tester.put("/todolist", data=json.dumps(data), headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"result" in response.data)

    def test_put_400(self):
        tester = app.test_client(self)
        data = {"user_name": "John", "title": "Go to the gym", "description": "Train chest in the gym",
                "responsible": "John"}
        test_data = {**data}
        for key in data:
            del test_data[key]
            response = tester.put("/todolist", data=json.dumps(data))
            self.assertEqual(response.status_code, 400)

    def test_get_200(self):
        tester = app.test_client(self)
        response = tester.get("/todolist")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"result" in response.data)

    def test_patch_200(self):
        tester = app.test_client(self)
        response_get_200 = tester.get("/todolist")
        data = {"user_name": "John", "title": "Go to the gym", "description": "Train chest in the gym",
                "responsible": "John", "id": response_get_200.json["result"][-1]["id"]}
        test_data = {**data}
        headers = {"Content-Type": "application/json"}
        for key in data:
            if key not in ("user_name", "id"):
                del test_data[key]
                response_patch_200 = tester.patch("/todolist", data=json.dumps(test_data), headers=headers)
                logging.warning(test_data)
                self.assertEqual(response_patch_200.status_code, 200)
                self.assertEqual(response_patch_200.content_type, "application/json")
                self.assertTrue(b"result" in response_patch_200.data)

    def test_patch_400(self):
        tester = app.test_client(self)
        response_get_200 = tester.get("/todolist")
        data = {"user_name": "John", "title": "Go to the gym", "description": "Train chest in the gym",
                "responsible": "John", "id": response_get_200.json["result"][-1]["id"]}
        test_data = {**data}
        for key in data:
            if key in ("user_name", "id"):
                del test_data[key]
                response_patch_200 = tester.patch("/todolist", data=json.dumps(test_data))
                self.assertEqual(response_patch_200.status_code, 400)

    def test_delete_200_and_get_patch_404(self):
        tester = app.test_client(self)
        response_get_200 = tester.get("/todolist")
        data = {"user_name": "John", "id": response_get_200.json["result"][-1]["id"]}
        headers = {"Content-Type": "application/json"}
        response_delete = tester.delete("/todolist", data=json.dumps(data), headers=headers)
        self.assertEqual(response_delete.status_code, 200)
        self.assertEqual(response_delete.content_type, "application/json")
        self.assertTrue(b"result" in response_delete.data)

        deleted_task_id = response_get_200.json["result"][-1]["id"]
        deleted_user_name = response_get_200.json["result"][-1]["user_name"]
        response_get_404 = tester.get(f"/todolist?user_name={deleted_user_name}&id={deleted_task_id}")
        self.assertEqual(response_get_404.status_code, 404)
        self.assertEqual(response_get_404.content_type, "application/json")
        self.assertTrue(b"error" in response_get_404.data)

        response_get_404 = tester.patch("/todolist", data=json.dumps(data), headers=headers)
        self.assertEqual(response_get_404.status_code, 404)
        self.assertEqual(response_get_404.content_type, "application/json")
        self.assertTrue(b"error" in response_get_404.data)

    def test_delete_400(self):
        tester = app.test_client(self)
        response_get_200 = tester.get("/todolist")
        data = {"user_name": "John", "id": response_get_200.json["result"][-1]["id"]}
        headers = {"Content-Type": "application/json"}
        for key in data:
            test_data = {**data}
            del test_data[key]
            response_delete = tester.delete("/todolist", data=json.dumps(test_data), headers=headers)
            self.assertEqual(response_delete.status_code, 400)


if __name__ == '__main__':
    unittest.main()
