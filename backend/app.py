from functools import wraps
import random
from typing import Optional
from math import ceil
from sys import exc_info
from flask import Flask, request, abort, jsonify, make_response
from flask_cors import CORS
from settings import DB_NAME, DB_PASSWORD, DB_USER, SECRET_KEY
from models import Question, Category, Rating, User
from flask_migrate import Migrate
from flask import Flask
from db import db
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid


database_path = F'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}'


def create_app(test_config=None):
    QUESTIONS_PER_PAGE = 8
    API_VERSION = 'v1.0'

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
    def paginate(collection: list, page: int, pages_count: int):
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        if page < pages_count:
            return collection[start: end]
        elif page == pages_count:
            return collection[start:]

    # Authentication decorator
    def token_required(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = None
            # ensure the jwt-token is passed with the headers
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token:  # throw error if no token provided
                return make_response(jsonify({"message": "A valid token is missing!"}), 401)
            try:
                # decode the token to obtain user public_id
                data = jwt.decode(
                    token, app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user: User = User.query.filter_by(
                    public_id=data['public_id']).first()
            except:
                return make_response(jsonify({"message": "Invalid token!"}), 401)
            # Return the user information attached to the token
            return f(current_user, *args, **kwargs)
        return decorator

    CORS(app, supports_credentials=True) # CORS set-up

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # verify token route

    @cross_origin
    @app.route(F'/api/{API_VERSION}/verify', methods=['POST'])
    def verify_token():
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:  # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            # decode the token to obtain user public_id
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user: User = User.query.filter_by(
                public_id=data['public_id']).first()
            return jsonify({'user': current_user.format()})
        except:
            return make_response(jsonify({"message": "Invalid token!"}), 401)


    # user signup route
    @app.route(F'/api/{API_VERSION}/signup', methods=['POST'])
    def signup_user():
        data = request.get_json()
        hashed_password = generate_password_hash(
            data['password'], method='sha256')

        user = User.query.filter_by(username=data['username']).first()
        if not user:
            new_user = User(public_id=str(uuid.uuid4()),
                            username=data['username'], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'registered successfully'}), 201
        else:
            return make_response(jsonify({"message": "User already exists!"}), 409)

    # user signin route
    @cross_origin
    @app.route(F'/api/{API_VERSION}/signin', methods=['POST'])
    def signin_user():
        auth = request.get_json()
        if not auth or not auth.get('username') or not auth.get('password'):
            return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic-realm= "Login required!"'})

        user = User.query.filter_by(username=auth['username']).first()
        if not user:
            return make_response('Could not verify user!', 401, {'WWW-Authenticate': 'Basic-realm= "No user found!"'})

        if check_password_hash(user.password, auth.get('password')):
            token = jwt.encode({'public_id': str(user.public_id)},
                               app.config['SECRET_KEY'], 'HS256')
            return make_response(jsonify({'token': token, 'user': user.format()}), 201)

        return make_response('Could not verify password!', 403, {'WWW-Authenticate': 'Basic-realm= "Wrong Password!"'})

    # get all categories
    @cross_origin
    @app.route(F'/api/{API_VERSION}/categories', methods=['GET'])
    @token_required
    def get_categories(current_user: User):
        try:
            categories: list[Category] = Category.query.filter(
                db.or_(Category.ownership == current_user.id, Category.ownership == 0)).all()
            return jsonify({
                "success": True,
                "categories": [category.format() for category in categories]
            })
        except:
            print(exc_info())
            abort(500)

    # insert category
    @cross_origin
    @app.route(F'/api/{API_VERSION}/categories', methods=['POST'])
    @token_required
    def insert_category(current_user: User):
        try:
            category_name: str = request.get_json()['category']

            category = Category(type=category_name, ownership=current_user.id)
            category.insert()

            return jsonify({
                "success": True,
                "category": category.format()
            })
        except:
            print(exc_info())
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # delete category
    @cross_origin
    @app.route(F'/api/{API_VERSION}/categories', methods=['DELETE'])
    @token_required
    def delete_category(current_user: User):
        try:
            category_id: str = request.get_json()['category_id']

            category: Category = Category.query.get(category_id)
            if category.ownership != current_user.id:
                abort(401)
            if category is None:
                abort(404)
            db.engine.execute(F"delete from categories where id={category_id}")
            return jsonify({
                "success": True,
                "category": category.format()
            })
        except:
            print(exc_info())
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

    # get all questions
    @cross_origin
    @app.route(F'/api/{API_VERSION}/questions', methods=['GET'])
    @token_required
    def get_questions(current_user: User):
        try:
            page = request.args.get('page', 1, type=int)
            questions = db.engine.execute(F'''
                select *
                from (
                    select q.id,
                    q.question,
                    q.answer,
                    q.difficulty,
                    q.category,
                    q.ownership,
                    r.rating
                    from questions q 
                    left join ratings r 
                    on q.id = r.question 
                    where (q.ownership = 0 or q.ownership = {current_user.id}) and (r."user" = {current_user.id} or r."user" is null)
                    ) as t1
                inner join (
                    select q.id, coalesce(AVG(r.rating), 0)::float as avg_rating
                    from questions q 
                    left join ratings r 
                    on q.id = r.question 
                    group by q.id
                    ) as t2
                on t1.id = t2.id
            ''').all()

            pages_count = ceil(len(questions)/QUESTIONS_PER_PAGE)

            if page > pages_count :
                return make_response(jsonify({
                    "success": False,
                    "message": "resource not found"
                }), 404)
            questions_paginated = paginate(questions, page, pages_count)

            return jsonify({
                "success": True,
                "questions": [{
                    "id": item[0],
                    "question": item[1],
                    "answer": item[2],
                    "difficulty": item[3],
                    "category": item[4],
                    "ownership": item[5],
                    "rating": item[6],
                    "avg_rating": item[-1]
                } for item in questions_paginated],
                "pages": pages_count
            })
        except:
            print(exc_info())
            abort(404)

    # delete question
    @cross_origin
    @app.route(F'/api/{API_VERSION}/questions', methods=['DELETE'])
    @token_required
    def delete_question(current_user: User):
        try:
            question_id: int = int(request.get_json()['question_id'])
            question: Question = Question.query.filter_by(
                id=question_id).first()
            if not question_id or not question or (question.id == 0 and current_user.id != 0):
                abort(404)
            db.engine.execute(
                F"delete from questions where id={question_id}")
                
            return jsonify({
                "success": True,
                "question": question.format()
            })
        except:
            print(exc_info())
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

    # insert question
    @cross_origin
    @app.route(F'/api/{API_VERSION}/questions', methods=['POST'])
    @token_required
    def insert_question(current_user: User):
        try:
            question_ = request.get_json()['question']
            answer = request.get_json()['answer']
            difficulty: int = int(request.get_json()['difficulty'])
            category_id: int = int(request.get_json()['category_id'])

            question = Question(question=question_, answer=answer,
                                difficulty=difficulty, category=category_id, ownership=current_user.id)
            question.insert()
            return jsonify({
                "success": True,
                "question": question.format()
            })
        except:
            print(exc_info())
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # search questions
    @cross_origin
    @app.route(F'/api/{API_VERSION}/questions/search', methods=['POST'])
    @token_required
    def search_question(current_user: User):
        try:
            search_term: str = request.get_json()['term']
            questions = db.engine.execute(F'''
                select *
                from (
                    select q.id,
                    q.question,
                    q.answer,
                    q.difficulty,
                    q.category,
                    q.ownership,
                    r.rating
                    from questions q 
                    left join ratings r 
                    on q.id = r.question 
                    where (q.ownership = 0 or q.ownership = {current_user.id}) 
                    and (r."user" = {current_user.id} or r."user" is null) 
                    and q.question like '%{search_term}%'
                    ) as t1
                inner join (
                    select q.id, coalesce(AVG(r.rating), 0)::float as avg_rating
                    from questions q 
                    left join ratings r 
                    on q.id = r.question 
                    group by q.id
                    ) as t2
                on t1.id = t2.id
            ''').all()

            return jsonify({
                "success": True,
                "questions": [{
                    "id": item[0],
                    "question": item[1],
                    "answer": item[2],
                    "difficulty": item[3],
                    "category": item[4],
                    "ownership": item[5],
                    "rating": item[6],
                    "avg_rating": item[-1]
                } for item in questions]
            })
        except:
            abort(404)

    # get questions of a given category and the medium rating of that question if it is public or private
    @cross_origin
    @app.route(F'/api/{API_VERSION}/category/<int:category_id>', methods=['GET'])
    @token_required
    def get_question_based_on_category(current_user: User, category_id: int):
        try:
            page = request.args.get('page', 1, int)
            questions = db.engine.execute(F'''
                select *
                from (
                    select q.id,
                    q.question,
                    q.answer,
                    q.difficulty,
                    q.category,
                    q.ownership,
                    r.rating
                    from questions q 
                    left join ratings r 
                    on q.id = r.question 
                    where (q.ownership = 0 or q.ownership = {current_user.id}) and (r."user" = {current_user.id} or r."user" is null) and category={category_id}
                    ) as t1
                inner join (
                    select q.id, coalesce(AVG(r.rating), 0)::float as avg_rating
                    from questions q 
                    left join ratings r 
                    on q.id = r.question 
                    group by q.id
                    ) as t2
                on t1.id = t2.id
            ''').all()

            pages_count = ceil(len(questions)/QUESTIONS_PER_PAGE)
            category: Category = Category.query.get(category_id)

            if page > pages_count or (category is None or not category):
                return make_response(jsonify({
                    "success": False,
                    "message": "resource not found"
                }), 404)
            questions_paginated = paginate(questions, page, pages_count)

            return jsonify({
                "success": True,
                "category": category.format(),
                "questions": [{
                    "id": item[0],
                    "question": item[1],
                    "answer": item[2],
                    "difficulty": item[3],
                    "category": item[4],
                    "ownership": item[5],
                    "rating": item[6],
                    "avg_rating": item[-1]
                } for item in questions_paginated],
                "pages": pages_count
            })
        except:
            print(exc_info())
            abort(404)

    # get random question for the quizz
    @cross_origin
    @app.route(F'/api/{API_VERSION}/questions/random', methods=['POST'])
    @token_required
    def get_random_questions(current_user: User):
        try:
            category_id: Optional[int] = request.json.get('category_id')
            previous_questions: Optional[list] = list(request.json.get('previous'))

            if not category_id or category_id is None:
                questions = db.session.query(Question).filter(Question.id.not_in(previous_questions)).filter(
                    db.or_(Question.ownership == 0, Question.ownership == current_user.id)).all()
                questions_set = [questions[i].format()
                                 for i in random.sample(range(0, len(questions)), 5)]
                return jsonify({
                    "success": True,
                    "questions": questions_set
                })
            elif category_id:
                category = Category.query.get(category_id)
                if not category:
                    return make_response(jsonify({
                        "success": False,
                        "message": "resource not found"
                    }), 404)
                questions = db.session.query(Question).filter(Question.id.not_in(previous_questions)).filter(
                    Question.category == category_id).filter(db.or_(Question.ownership == 0, Question.ownership == current_user.id)).all()
                questions_set = [questions[i].format()
                                 for i in random.sample(range(0, len(questions)), 5)]
                return jsonify({
                    "success": True,
                    "questions": questions_set,
                    "category": category_id
                })

        except:
            print(exc_info())
            abort(400)

    # check question's answer correctness
    @cross_origin
    @app.route(F'/api/{API_VERSION}/questions/verify', methods=['POST'])
    @token_required
    def check_answer(current_user: User):
        try:
            question_id: Optional[int] = request.json.get('question_id')
            answer: Optional[str] = request.json.get('answer')

            question: Question = Question.query.get(question_id)
            if not question or question is None:
                abort(404)
            if question.answer.lower().strip() == answer.lower().strip():
                return jsonify({
                    "correct": True,
                })
            else:
                return jsonify({
                    "correct": False,
                })
        except:
            print(exc_info())
            abort(404)

    # add or update rating
    @cross_origin
    @app.route(F'/api/{API_VERSION}/ratings', methods=['POST'])
    @token_required
    def update_or_add_rating(current_user: User):
        try:
            score = request.get_json()['rating']
            question_id = request.get_json()['question_id']
            rating: Rating = Rating.query.filter_by(
                user=current_user.id).filter_by(question=question_id).first()
            if not rating:
                new_rating: Rating = Rating(
                    question=question_id, rating=int(score), user=current_user.id)
                new_rating.insert()
                med = db.engine.execute(F"select coalesce((rating), 0) from ratings where question={question_id}").all()
                return jsonify({
                    "success": True,
                    "new_rating": score,
                    "medium": med[0][0]
                })
            rating.rating = score
            db.session.commit()
            med = db.engine.execute(F"select coalesce((rating), 0) from ratings where question={question_id}").all()
            print(med)
            return jsonify({
                "success": True,
                "new_rating": score,
                "medium": med[0][0]
            })
        except:
            print(exc_info())
            abort(404)
        finally:
            db.session.close()

    """
    error handlers for all expected errors
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify({"success": False, "error": 500,
                    "message": "internal error"}),
            500,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(422)
    def bad_request(error):
        return jsonify({"success": False, "error": 422, "message": "Unprocessable Entity"}), 422

    return app
