from flask import Flask , render_template, redirect, request, session
from data import Articles
import pymysql
from passlib.hash import sha256_crypt
from functools import wraps

db = pymysql.connect(
            host='localhost', 
            user='root', 
            password='1234', 
            db='gangnam',
            charset='utf8mb4')

cur = db.cursor()


app = Flask(__name__)
app.debug = True

def is_loged_in(f):
    @wraps(f)
    def _wraps(*args, **kwargs) :
        if 'is_loged' in session :
            query = f"select username from users where email = '{session['email']}'"
            cur.execute(query)
            db.commit()
            user = cur.fetchone()
            # print(user)
            user_name = user[0]
            return f(*args, **kwargs)
        else :
            return redirect('/login')
    return _wraps

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        

        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password = sha256_crypt.encrypt(password)
        # print(sha256_crypt.verify("1234", password_1))
        # print(name, email, password)
        sql = f"SELECT email FROM users WHERE email = '{email}'"
        cur.execute(sql)
        db.commit()
        user_email = cur.fetchone()
        print(user_email)
        if user_email == None:

            query = f"INSERT INTO users (name, email, username, password) VALUES ('{name}', '{email}', '{username}', '{password}')"

            cur.execute(query)
            db.commit()

            return redirect('/login')
        else : 
            return redirect('/register')
    else :
        return render_template('register.html')
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email, password)

        query = f"SELECT * FROM users WHERE email = '{email}';"
        cur.execute(query)
        db.commit()
        user = cur.fetchone()
        print(user)

        if user == None:
            return redirect('/login')
        else :
            if sha256_crypt.verify(password, user[4]):
                session['is_loged'] = True
                session['email'] = user[2]
                session['username'] = user[3]
                print(session)
                return redirect('/')
            else :
                return redirect('/login')

        
    else :
        return render_template('/login.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/', methods=['GET', 'POST']) # 경로(그 쪽 경로에 입장하면 실행)/로그인,관리자OX
@is_loged_in
def hello_world():
    return render_template('home.html', user_name = session['username']) # 섞는 게 가능
   
    #'<h1>Hello World!</h1>' # h1과tag가 만나면 tag의 기능만 캡쳐함

@app.route('/about', methods=['GET', 'POST'])
@is_loged_in
def about():
    return render_template("about.html", user_name = session['username'])

@app.route('/articles', methods=['GET', 'POST'])
@is_loged_in
def articles():
    # articles = Articles()

    query = 'SELECT * FROM topic;'

    cur.execute(query)

    db.commit()

    articles = cur.fetchall()

    print(articles)
    return render_template( "articles.html", articles = articles , user_name = session['username'])


@app.route('/article/<id>', methods=['GET', 'POST'])
def article(id):
    # articles = Articles()
    # print(len(articles))
    # article = articles[int(id)-1]
    # if len(articles)<=int(id):
        
    #     return render_template("article.html", article = article)
    # else:
    #     return render_template("article.html", article = "NO DATA")

    query = f"SELECT * FROM topic WHERE id = {id} "

    cur.execute(query)
    db.commit()

    article = cur.fetchall()
    print(article)
    if article **None:
        return redirect('/articles')
    else:
        return render_template('article.html', article = article, user_name = session['username'] )


@app.route('/article/<id>/delete')
def delete_article(id):
    query = f'DELETE FROM `topic` WHERE id = {id};'
    cur.execute(query)

    db.commit()

    # db.close()

    return redirect('/articles')

@app.route('/add_article',  methods = ['GET','POST'])
def add_articles():

    if request.method == "POST" :

        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        
        print(title, description, author)
        # return "SUCCESS"

        query = "INSERT INTO `topic` (`title`,`description`,`author`) VALUES (%s, %s, %s);"
        input_data = [title, description ,author]
        # print(request, description, author)

        cur.execute(query,input_data)
        db.commit()
        print(cur.rowcount)
        # db.close()

        return redirect("/articles")
        
    else :
        return render_template("add_article.html", user_name = session['username'])

@app.route("/article/<id>/edit", methods = ['GET','POST'])
@is_loged_in

def edit_article(id):
    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']

        author = request.form['author']
        # print(title, description, author)

        # return "SUCCESS"
        
        query = f"UPDATE `gangnam`.`topic` SET  title='{title}',description= '{description}' ,author='{author}' WHERE id = {id};"
        print(query)
    
        cur.execute(query)

        db.commit()

        return redirect('/articles')
        

    else:
        query = f"SELECT * FROM topic WHERE id = {id};"


        cur.execute(query)
        db.commit()

        article = cur.fetchone()

        return render_template('edit_article.html', article = article, user_name = session['username'])

       

if __name__ == '__main__':
    app.secret_key = "gangnamStyle"
    app.run(port=5000)
    

# 서버 띄우기 GET 방식으로 Enter만 치는 것






