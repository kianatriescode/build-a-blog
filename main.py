from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))

    def __init__(self,name,body):
        self.title = title 
        self.body = body

@app.route('/blog', methods=['POST', 'GET'] ) 
def blog():    
    blog_post = Blog.query.all()
    blog_id = request.args.get('id')
    
    if blog_id == None:
        return render_template('index.html',title="Build a blog",blog_post=blog_post) 
    
    else:
        blogpage = Blog.query.get(blog_id)
        
        
       
        return render_template('post.html',blogpage=blogpage)
         
@app.route('/add', methods = ['POST','GET'])
def newpost():
    newpost_error = ''
    body_error = ''
    if request.method == "GET":
        return render_template('newpost.html',title='New blog entry',newpost_error=newpost_error, body_error=body_error)    
    if request.method == 'POST':
        blog_name = request.form['newpost']
        blog_body = request.form['body']
        new_post = Blog(blog_name,blog_body)
        db.session.add(new_post)
        db.session.commit()
        blog_id = new_post.id

        if blog_name == '':
            newpost_error = 'Your new blog needs a title'
    
        elif blog_body=='':
            body_error = 'You need to add some content to your blog post'    
    if not newpost_error and not body_error:   
         return redirect('/blog?id={}'.format(blog_id))
    else:
        return render_template('newpost.html',title='New blog entry',newpost_error=newpost_error, body_error=body_error)

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()