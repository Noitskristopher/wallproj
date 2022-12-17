from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, post
from datetime import datetime
dateFormat = "%m/%d"


@app.route('/post/create', methods=["POST"])
def create_post():
    if 'user_id' in session:
        if post.Post.validate_create(request.form):
            data = {
                'content': request.form['content'],
                'user_id': session['user_id']
            }
            post.Post.save(data)
            return redirect('/wall')
        return redirect('/wall')
    return redirect('/')


@app.route('/posts/delete/<int:post_id>')
def delete_post(post_id):
    if 'user_id' in session:
        post.Post.delete({'id': post_id})
        return redirect('/wall')
    return ('/')
