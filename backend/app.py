from typing import Optional
from math import ceil
from sys import exc_info
from unicodedata import category
from flask import Flask, request, abort, jsonify, make_response
from flask_cors import CORS
from sqlalchemy import null
from settings import DB_NAME, DB_PASSWORD, DB_USER
from models import Question, Category
from flask_migrate import Migrate
from flask import Flask
from db import db
from flask_cors import CORS, cross_origin

database_path = F'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}'

def create_app(test_config=None):
    QUESTIONS_PER_PAGE = 10
    
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.debug = True

    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)
    migrate.init_app(app, db)

    """
        Paginate Method
    """
    def paginate(collection: list[Question], page: int, pages_count: int):
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        if page < pages_count:
            return [item.format() for item in collection[start: end]] 
        elif page == pages_count: 
            return [item.format() for item in collection[start:]] 
    
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})
   
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @cross_origin
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories: list[Category] = Category.query.all()
            return jsonify({
                "success": True,
                "categories": [category.format() for category in categories]
            })
        except:
            print(exc_info())
            abort(500)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @cross_origin
    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            page = request.args.get('page', 1, type=int)
            questions: list[Question] = Question.query.all()
            pages_count = ceil(len(questions)/QUESTIONS_PER_PAGE)
            if page > pages_count:
                return make_response(jsonify({
                    "success": False,
                    "message":"resource not found"
                    }), 404)
            questions_paginated = paginate(questions, page, pages_count)
            return jsonify({
                "success": True,
                "questions": questions_paginated,
                "total_questions": len(questions)
            })
        except:
            abort(500)    

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @cross_origin
    @app.route('/questions', methods=['DELETE'])
    def delete_question():
        try:
            question_id: int = int(request.get_json()['question_id'])
            question: Question = Question.query.get(question_id)
            if not question_id or not question:
                abort(404)
            question.delete()
            return jsonify({
                "success": True,
                "question": question.format()
            })
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @cross_origin
    @app.route('/questions', methods=['POST'])
    def insert_question():
        try:
            question_ = request.get_json()['question']
            answer = request.get_json()['answer']
            difficulty: int = int(request.get_json()['difficulty'])
            category_id: int = int(request.get_json()['category_id'])

            question = Question(question=question_, answer=answer, difficulty=difficulty, category=category_id)
            question.insert()
            return jsonify({
                "success": True,
                "question": question.format()
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @cross_origin
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            search_term = request.get_json()['term']
            questions = Question.query.filter(Question.question.ilike(F"%{search_term}%")).all()
            return jsonify({
                "success": True,
                "questions": [question.format() for question in questions]
            })
        except:
            abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @cross_origin
    @app.route('/category/<int:category_id>', methods=['GET'])
    def get_question_based_on_category(category_id):
        try:
            questions = db.session.query(Question).filter(Question.category == category_id).all()
            category: Category = Category.query.get(category_id)
            return jsonify({
                "success": True,
                "category": category.format(),
                "questions": [question.format() for question in questions]
            })
        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @cross_origin
    @app.route('/questions/random', methods=['POST'])
    def get_random_questions():
        try:
            category_id: Optional[int] = request.json.get('category')
            print(category_id)
            previous_questions: list[int] = list(request.get_json()['previous'])
            
            if not category_id :
                questions = db.session.query(Question).filter(Question.id.not_in(previous_questions)).all()
                return jsonify({
                    "success": True,
                    "questions": [question.format() for question in questions]
                })
            elif category_id:
                category = Category.query.get(category_id)
                if not category:
                    return make_response(jsonify({
                        "success": False,
                        "message":"resource not found"
                        }), 404)
                questions = db.session.query(Question).filter(Question.category == category_id).filter(Question.id.not_in(previous_questions)).all()
                return jsonify({
                    "success": True,
                    "questions": [question.format() for question in questions],
                    "category": category_id
                })
                
        except:
            abort(400)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "internal error"}),
            500,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400


    @app.errorhandler(422)
    def bad_request(error):
        return jsonify({"success": False, "error": 422, "message": "Unprocessable Entity"}), 422
    
    return app

