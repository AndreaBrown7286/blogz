from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:mypassword@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<title %r>' % self.title


@app.route('/', methods=['POST', 'GET'])
def index():

    return redirect('/blog')
    
@app.route('/blog', methods=['POST', 'GET'])
def blog_list():    
    
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)


@app.route('/newblog', methods=['POST'])
def new_blog():
    
    blog_title=request.form['blog_title']
    blog_area=request.form['blog_area']
    new_blog=Blog(blog_title, blog_area)
    db.session.add(new_blog)
    db.session.commit()
    blog_title_error=""
    blog_area_error=""
    
    if blog_title == "": 
        blog_title_error="Please fill in both fields"
        blog_title=blog_title
    if blog_area == "":    
        blog_area_error="Please fill in both fields"
        blog_area=blog_area

    if not blog_error:
        return redirect('/blog')
    else:
        return render_template('newblog.html', blog_title=blog_title, blog_area=blog_area,
        blog_error=blog_error)



if __name__ == '__main__':
    app.run()