from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import os, jinja2
from main import db,Task

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
ACK_MODIFICATIONS = True
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    new_blog = db.Column(db.String(750))
    completed = db.Column(db.Boolean)
    
    def __init__(self, title, new_blog):
        self.title = title
        self.new_blog = new_blog
        self.completed = False

@app.route('/')
def index():
    blogs = Blog.query.all()
    return render_template('blog-list.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'GET':
        return render_template('blog-add.html')

    title_err = ""
    new_blog_err = ""

    if request.method == 'POST':
        title = request.form['title']
        new_blog = request.form['new_blog']

    if not title:
        title_err = "Please enter a valid title"

    if not new_blog:
        new_blog_err = "Please enter a valid blog entry"

    if not title_err and not new_blog_err:
        blog = Blog(title, new_blog)
        db.session.add(blog)
        db.session.commit()
        return redirect('/blog?id=' + str(blog.id))

    return render_template('blog-add.html', title_err=title_err, new_blog_err=new_blog_err)

@app.route('/blog', methods=['GET'])
def blog_listings():

    if request.args:
        id = request.args.get("id")
        blog = Blog.query.get(id)
        return render_template('post-blog.html', title="Build a blog", blog=blog)
    else:
        blogs = Blog.query.all()
        
        return render_template('blog-list.html', blogs=blogs)

if __name__ == '__main__':
    app.run()