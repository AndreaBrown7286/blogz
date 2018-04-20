from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:mypassword@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    
@app.route('/blog', methods=['GET','POST'])
def blog_list():    
    
    if not request.args.get('id'):
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)

    if request.args.get('id'):
        blog_id = request.args.get('id')
        single_blog = Blog.query.get(blog_id)

        blog_title=single_blog.title
        blog_body=single_blog.body

        return render_template('blog-display.html', blog_title=single_blog.title,blog_body=single_blog.body )


@app.route('/newblog', methods=['GET', 'POST'])
def newblog():
    
    blog_title_error=""
    blog_body_error=""  


    if request.method == 'POST':   
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        
        if not blog_title: 
            blog_title_error="Please fill in both fields"
            blog_title=blog_title
        if not blog_body:    
            blog_body_error="Please fill in both fields"
            blog_body=blog_body 
        
        if blog_body_error or blog_title_error:
            return render_template('newblog.html', blog_body_error=blog_body_error,
                blog_title_error=blog_title_error)
        
        newblog = Blog(blog_title, blog_body, author)
        db.session.add(newblog)
        db.session.commit()
        newblog_id = str(newblog.id)
        return redirect('/blog?id='+ newblog_id)

    return render_template('newblog.html')    

    

    

@app.route('/', methods=['GET'])
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()