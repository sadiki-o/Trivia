# Backend - Quizzio API

## Setting up the Backend

### Install Dependencies

1. **Python 3.x** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies .

### Project Setup

To get started navigate to the `/backend` directory and run:

```bash
cd backend
```

```bash
python -m venv env
```

```bash
source env/bin/activate
```

```bash
pip install -r requirements.txt
```



#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgresql running, create a `trivia` database:

```bash
createbd trivia
```

*Note* : in the backend directory you will find a .env file containing database credentials and website url and PORT, change them according to your database and server configuration before proceeding.

### Project Structure

```
backend
│   .env
|	app.py
│	db.py
|	models.py
|	requirements.txt
|	settings.py
|	test_flaskr.py
└───migrations
    │___versions
        |
		|___7ec16e3a97a1_.py
		|___d18ea280b54d_.py
```

*Note :* the migrations folder holds two migrations, one for the models and one revision for configuring and populating data in the DB, you don't have to run `flask db migrate`   and `flask db upgrade`



### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server make sure you are inside the virtual environment and execute:

```bash
export FLASK_APP=app.py
```

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Endpoints Docs

Here is a list of endpoints and their expected results:

*send and verify token and return a user object :*

```
POST '/api/v1.0/verify'
```

*signup a new user by providing a <u>username</u> & <u>password</u>, return success if doesn't exist and already exist if the user already exist*

```
POST '/api/v1.0/singup'
```

*signin a user by providing a <u>username</u> and <u>password</u> , return a JWT token if successful*

```
POST '/api/v1.0/signin'
```

**the endpoints down bellow all require you to include an 'x-access-token' in order to access the ressource**

*get all categories of the current_user or the admin*

```
GET '/api/v1.0/categories'
```

*insert a new category owned by the current_user*

```
POST '/api/v1.0/categories'
```

*delete category owned by the current_user by providing a <u>category_id</u>*

```
DELETE '/api/v1.0/categories'
```

*get all questions owned by the user or the admin in a paginated way, avg_rating per question, user rating of the questions as well as the number of 8 questions set defined in <u>QUESTIONS_PER_PAGE</u> variable, you can include page as a search query (optional) otherwise page will be set to 1*

```
GET '/api/v1.0/questions?page=2'
```

*insert new question owned by the user*

```
POST '/api/v1.0/questions
```

*delete question owned by the user by providing a <u>question_id</u>*

```
DELETE '/api/v1.0/questions
```

*search questions by providing a search term and return a set of questions that match the search*

```
POST '/api/v1.0/questions/search
```

*get questions of a given category and the medium rating of each question and the number of 8 questions set defined in <u>QUESTIONS_PER_PAGE</u> variable, you can include page as a search query (optional) otherwise page will be set to 1*

```
POST '/api/v1.0/questions/random
```

*check question's answer correctness, by providing a <u>question_id</u> and <u>answer</u> to the question and return true or false*

```
POST '/api/v1.0/questions/verify
```

*add or update a questions's rating, by providing a <u>rating</u> and <u>question_id</u>*

```
POST '/api/v1.0/ratings
```

*get 5 random questions for the quizz, by providing a category_id(optional) and an array of previous_questions(optional) to make sure the client receive a new set of questions different than the previous one*

```
POST '/api/v1.0/category/<int:category_id>?page=2
```

## Testing

To run the tests, execute the following after setting up the <u>Database</u> and the <u>Server</u>

```bash
python test_flaskr.py
```