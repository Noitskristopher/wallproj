from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, post, comment


@app.route('/comment/create', methods=["POST"])
def create_comment():
    if 'user_id' in session:
        if comment.Comment.validate_create(request.form):
            print(request.form)
            data = {
                'content': request.form['content'],
                'user_id': session['user_id'],
                'post_id': request.form['post_id']
            }
            print(data)
            comment.Comment.save(data)
            return redirect('/wall')
        return redirect('/wall')
    return redirect('/')
