from flask_app.config.mysqlConnection import connectToMySQL
from flask import flash, session
from flask_app.models import user
mydb = 'coding_wall'


class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['content']) < 1:
            flash("Comment Content Must Not Be Blank", 'postError')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = '''
        INSERT INTO comments (content, user_id, post_id, created_at, updated_at )
        VALUES (%(content)s, %(user_id)s, %(post_id)s, NOW(), NOW());'''
        results = connectToMySQL(mydb).query_db(query, data)
        print(f"results: {results}")
        return results
