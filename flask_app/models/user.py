from flask_app.config.mysqlConnection import connectToMySQL
from flask_app.models import post
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z`]')
mydb = 'coding_wall'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['first_name']) < 1:
            flash("Please Enter A First Name", 'regError')
            is_valid = False
        elif not NAME_REGEX.match(request['first_name']):
            flash("Invalid First Name", 'regError')
            is_valid = False
        elif len(request['first_name']) <= 3:
            flash("First Name Must Be Longer Than Two Characters", 'regError')
            is_valid = False
        if len(request['last_name']) < 1:
            flash("Please Enter A Last Name", 'regError')
            is_valid = False
        elif not NAME_REGEX.match(request['last_name']):
            flash("Invalid Last Name", 'regError')
            is_valid = False
        elif len(request['last_name']) <= 3:
            flash("Last Name Must Be Longer Than Two Characters", 'regError')
            is_valid = False
        if len(request['email']) < 1:
            flash("Please Enter A Email Address", 'regError')
            is_valid = False
        elif not EMAIL_REGEX.match(request['email']):
            flash("Invalid email address!", 'regError')
            is_valid = False
        if len(request['password']) < 1:
            flash("Please Enter A Password", 'regError')
            is_valid = False
        elif len(request['password']) < 9:
            flash("Password Must Be Longer Than Eight Characters", 'regError')
            is_valid = False
        if len(request['passConf']) < 1:
            flash("Please Confirm Your Password", 'regError')
            is_valid = False
        elif request['password'] != request['passConf']:
            flash("Passwords Do Not Match", 'regError')
            is_valid = False
        if User.getByEmail(request):
            flash('Choose A Different Email', 'regError')
            is_valid = False
        print(f"is_valid: {is_valid}")
        return is_valid

    @classmethod
    def save(cls, data):
        query = '''
        INSERT INTO users (first_name, last_name, email, password, created_at, updated_at )
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());'''
        results = connectToMySQL(mydb).query_db(query, data)
        print(f"results: {results}")
        return results

    @classmethod
    def get_all(cls):
        query = '''
        SELECT *
        FROM users;'''
        results = connectToMySQL(mydb).query_db(query)
        # print(results)
        output = []
        for row in results:
            output.append(cls(row))
            # print(output)
        return output

    @classmethod
    def deleteById(cls, data):
        # print(data)
        query = '''
        DELETE FROM users
        WHERE id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        print(f'results:{results}')

    @classmethod
    def getById(cls, data):
        # print(data)
        query = '''
        SELECT * FROM users
        WHERE id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        print(f'results:{results}')
        return cls(results[0])

    @classmethod
    def getByEmail(cls, data):
        query = '''
        SELECT * FROM users
        WHERE email = %(email)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        print(f'results:{results}')
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getByIdJoinPosts(cls, data):
        query = '''
        SELECT * FROM users
        LEFT JOIN posts
        ON users.id = posts.user_id
        WHERE users.id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        print(f'results: {results}')
        output = cls(results[0])
        if not results[0]['posts.id'] == None:
            for row in results:
                post_info = {
                    'id': row['posts.id'],
                    'content': row['content'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at'],
                    'user_id': row['user_id']
                }
                output.posts.append(post.Post(post_info))
        return output
