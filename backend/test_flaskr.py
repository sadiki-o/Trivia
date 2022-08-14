import unittest
import json
from app import create_app


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    TEST_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJkYmUwM2ZhNy1iMDgwLTRlZjQtOGM4MS0zMGJkYjMzMGE0ZjEifQ.NTzJSyoGMIfHs4mcPspfgH0hwcU6fWcQvFp4Fn1Bf8A"

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories_success(self):
        """ get categories test success """
        res = self.client().get(
            "/api/v1.0/categories",
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_questions_success(self):
        """ get questions test success """
        res = self.client().get(
            "/api/v1.0/questions",
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertIsInstance(data["pages"], int)

    def test_get_questions_failure(self):
        """ get questions test failure """
        res = self.client().get(
            "/api/v1.0/questions?page=1000",
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_question_success(self):
        """ delete question test success """
        res = self.client().delete(
            "/api/v1.0/questions",
            json={"question_id": 2},
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["question"])

    def test_delete_question_failure(self):
        """ delete question test failure """
        res = self.client().delete(
            "/api/v1.0/questions",
            json={"question_id": 2000},
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_insert_question_success(self):
        """ insert question test sucess """
        res = self.client().post(
            "/api/v1.0/questions",
            json={
                "question": "What is the biggest planet?",
                "answer": "Jupiter",
                "difficulty": 2,
                "category_id": 1
            },
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["question"])

    def test_insert_question_failure(self):
        """ insert question test failure """
        res = self.client().post(
            "/api/v1.0/questions",
            json={
                "answer": "Jupiter",
                "difficulty": 2,
                "category_id": "string instead of number"
            },
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_search_question_sucess(self):
        """ search question test success """
        res = self.client().post(
            "/api/v1.0/questions/search",
            json={
                "term": "title",
            },
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreater(len(data["questions"]), 0)

    def test_search_question_no_results(self):
        """ search question test no results """
        res = self.client().post(
            "/api/v1.0/questions/search",
            json={
                "term": "some random things asydgaud",
            },
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 0)

    def test_get_questions_based_on_category_success(self):
        """ get question based on category test success """
        res = self.client().get(
            "/api/v1.0/category/2",
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["category"])
        self.assertGreaterEqual(len(data["questions"]), 0)
        self.assertIsInstance(data["pages"], int)

    def test_get_questions_based_on_category_failure(self):
        """ get question based on category test failure """
        res = self.client().get(
            "/api/v1.0/category/10000",
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_quizz_questions_without_category(self):
        """ get quizz questions without category """
        res = self.client().post(
            "/api/v1.0/questions/random",
            json={
                "previous": [1, 2, 8],
            },
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreaterEqual(len(data["questions"]), 0)

    def test_get_quizz_questions_with_category(self):
        """ get quizz questions with category """
        res = self.client().post(
            "/api/v1.0/questions/random",
            json={
                "category_id": 2,
                "previous": [1, 2, 8],
            },
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreaterEqual(len(data["questions"]), 0)
        self.assertIsInstance(data["category"], int)

    def test_get_quizz_questions_with_nonexistant_category(self):
        """ get quizz questions with nonexistant category """
        res = self.client().post(
            "/api/v1.0/questions/random",
            json={
                "category_id": 1020002,
                "previous": [1, 2, 8],
            },
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_quizz_questions_with_bad_data(self):
        """ get quizz questions with bad data """
        res = self.client().post(
            "/api/v1.0/questions/random",
            json={
                "category": "sda",
                "previous": [1, 2, 8, "sd"],
            },
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

        res = self.client().post(
            "/api/v1.0/questions/random",
            json={
                "category": 2,
            },
            headers={
                "x-access-token": self.TEST_TOKEN
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
