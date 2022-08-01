from crypt import methods
from functools import wraps
from typing import Optional
from math import ceil
from sys import exc_info
from flask import Flask, request, abort, jsonify, make_response
from flask_cors import CORS
from settings import DB_NAME, DB_PASSWORD, DB_USER, SECRET_KEY
from models import Question, Category, User
from flask_migrate import Migrate
from flask import Flask
from db import db
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt 
import uuid

database_path = F'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}'

def create_app(test_config=None):
    QUESTIONS_PER_PAGE = 10
    
    app = Flask(__name__)
    app.debug = True
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = SECRET_KEY
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
    
    # Authentication decorator
    def token_required(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = None
            print(request.headers['x-access-token'])
            # ensure the jwt-token is passed with the headers
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token: # throw error if no token provided
                return make_response(jsonify({"message": "A valid token is missing!"}), 401)
            try:
            # decode the token to obtain user public_id
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user = User.query.filter_by(public_id=data['public_id']).first()
            except:
                return make_response(jsonify({"message": "Invalid token!"}), 401)
            # Return the user information attached to the token
            return f(current_user, *args, **kwargs)
        return decorator
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

       

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # user signup route
    # register route
    @app.route('/signup', methods=['POST'])
    def signup_user(): 
        data = request.get_json() 
        hashed_password = generate_password_hash(data['password'], method='sha256')
        
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password)
            db.session.add(new_user) 
            db.session.commit() 

            return jsonify({'message': 'registered successfully'}), 201
        else:
            return make_response(jsonify({"message": "User already exists!"}), 409)


    # user login route
    @cross_origin
    @app.route('/login', methods=['POST'])
    def login():
        auth = request.get_json()
        if not auth or not auth.get('username') or not auth.get('password'):
            return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic-realm= "Login required!"'})

        user = User.query.filter_by(username=auth['username']).first()
        if not user:
            return make_response('Could not verify user!', 401, {'WWW-Authenticate': 'Basic-realm= "No user found!"'})

        if check_password_hash(user.password, auth.get('password')):
            token = jwt.encode({'public_id': str(user.public_id)}, app.config['SECRET_KEY'], 'HS256')
            return make_response(jsonify({'token': token}), 201)

        return make_response('Could not verify password!', 403, {'WWW-Authenticate': 'Basic-realm= "Wrong Password!"'})




    #get all categories
    @cross_origin
    @app.route('/categories', methods=['GET'])
    @token_required
    def get_categories(current_user):
        try:
            categories: list[Category] = Category.query.all()
            return jsonify({
                "success": True,
                "categories": [category.format() for category in categories]
            })
        except:
            print(exc_info())
            abort(500)

    #get all questions
    @cross_origin
    @app.route('/questions', methods=['GET'])
    @token_required
    def get_questions(current_user):
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

    #delete question
    @cross_origin
    @app.route('/questions', methods=['DELETE'])
    @token_required
    def delete_question(current_user):
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

    #insert question
    @cross_origin
    @app.route('/questions', methods=['POST'])
    @token_required
    def insert_question(current_user):
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
   
    #search questions
    @cross_origin
    @token_required
    @app.route('/questions/search', methods=['POST'])
    def search_question(current_user):
        try:
            search_term = request.get_json()['term']
            questions = Question.query.filter(Question.question.ilike(F"%{search_term}%")).all()
            return jsonify({
                "success": True,
                "questions": [question.format() for question in questions]
            })
        except:
            abort(404)

    #get category questions
    @cross_origin
    @app.route('/category/<int:category_id>', methods=['GET'])
    @token_required
    def get_question_based_on_category(category_id, current_user):
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

    
    #get random question
    @cross_origin
    @app.route('/questions/random', methods=['POST'])
    @token_required
    def get_random_questions(current_user):
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

