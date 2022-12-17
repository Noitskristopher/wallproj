from flask_app.config.mysqlConnection import connectToMySQL
from flask import flash, session
from flask_app.models import user, comment
mydb = 'coding_wall'


class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        self.comments = []

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['content']) < 1:
            flash("Post Content Must Not Be Blank", 'postError')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = '''
        INSERT INTO posts (content, user_id, created_at, updated_at )
        VALUES (%(content)s, %(user_id)s, NOW(), NOW());'''
        results = connectToMySQL(mydb).query_db(query, data)
        print(f"results: {results}")
        return results

    @classmethod
    def get_all(cls):
        query = '''
        SELECT *
        FROM posts;'''
        results = connectToMySQL(mydb).query_db(query)
        # print(results)
        output = []
        for row in results:
            output.append(cls(row))
            # print(output)
        return output

    @classmethod
    def get_all_posts_with_user(cls):
        query = '''
        SELECT posts.*, users.first_name
        FROM posts
        JOIN users
        ON posts.user_id = users.id;'''
        results = connectToMySQL(mydb).query_db(query)
        all_posts = []
        for row in results:
            this_post = cls(row)
            this_post.creator = row['first_name']
            print(row)
            print(row['id'])
            post_dict = {
                'post_id': row['id']
            }
            query2 = '''
            SELECT *
            FROM comments
            WHERE post_id = %(post_id)s;'''
            results2 = connectToMySQL(mydb).query_db(query2, post_dict)
            for comm in results2:
                this_post.comments.append(comment.Comment(comm))
                print(f"post comment objects: {this_post.comments}")
            all_posts.append(this_post)
        return all_posts

    @classmethod
    def delete(cls, data):
        query = '''
        DELETE FROM posts WHERE id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        print(results)
