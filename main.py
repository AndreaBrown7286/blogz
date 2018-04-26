from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:mypassword@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B123'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

    def __repr__(self):
        return '<Blog %r>' % self.name

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog_list', 'index', 'signup']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')


@app.route("/login", methods=['GET','POST'])
def login():
    
    login_error = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = user.username
            return redirect('/newblog')
        else:
            login_error = "User password incorrect, or user does not exist."
            
    return render_template('login.html', login_error=login_error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    username_error = ""
    password_error = ""
    verify_password_error = ""
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_password = request.form['verify_password']
        if not username or len(username) <3 or len(username) >20 or str.isalpha(username)==False:
            username_error="The username must be between 3-20 characters with no spaces."
            username = username
        username_db_count = User.query.filter_by(username=username).count()
        if username_db_count > 0:
            username_error="This username already exists, please login."
            username = username
        if not password or len(password) <3 or len(password) >20 or str.isalpha(password)==False:
            password_error="The password must be between 3-20 characters with no spaces."
            password = ''
        if password != verify_password:
            verify_password_error="Your passwords do not match."
            verify_password = ''
        if not username_error and not password_error and not verify_password_error:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            session['user'] = user.username
            return redirect('/newblog')
    return render_template('signup.html', username_error=username_error,
            password_error=password_error, verify_password_error=verify_password_error)    
    

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
            blog_title = blog_title
        if not blog_body:    
            blog_body_error="Please fill in both fields"
            blog_body = blog_body 
        
        if blog_body_error or blog_title_error:
            return render_template('newblog.html', blog_body_error=blog_body_error,
                blog_title_error=blog_title_error)
        
        newblog = Blog(blog_title, blog_body, logged_in_user())
        db.session.add(newblog)
        db.session.commit()
        newblog_id = str(newblog.id)
        return redirect('/blog?id='+ newblog_id)

    return render_template('newblog.html')    


@app.route('/logout')
def logout():
    del session['user']
    return redirect('/blog')
    #needs to redirect to /blog, but instead redirects to /login


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

def logged_in_user():
    owner = User.query.filter_by(username=session['user']).first()
    return owner


if __name__ == '__main__':
    app.run()