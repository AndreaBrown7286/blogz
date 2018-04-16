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

    #def __repr__(self):
        #return '<title %r>' % self.title

    
@app.route('/blog', methods=['GET','POST'])
def blog_list():    
    
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)
    

@app.route('/newblog', methods=['GET', 'POST'])
def newblog():
    
    if request.method == 'POST':   
        blog_title = request.form['blog_title']
        blog_area = request.form['blog_area']
        newblog = Blog(blog_title, blog_area)
        db.session.add(newblog)
        db.session.commit()
        blog_title_error=""
        blog_area_error=""   
    return render_template('newblog.html')
    
    if blog_title == "": 
        blog_title_error="Please fill in both fields"
        blog_title=blog_title
    if blog_area == "":    
        blog_area_error="Please fill in both fields"
        blog_area=blog_area

    if not blog_area_error and not blog_title_error:
        return redirect('/blog')
    else:
        return render_template('newblog.html', blog_area_error=blog_area_error,
            blog_title_error=blog_title_error)

@app.route('/', methods=['GET'])
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()