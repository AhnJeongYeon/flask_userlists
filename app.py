from flask import Flask , render_template, redirect, request
from data import Articles
import pymysql
from passlib.hash import sha256_crypt

db = pymysql.connect(
            host='localhost', 
            user='root', 
            password='1234', 
            db='gangnam',
            charset='utf8mb4')

cur = db.cursor()


app = Flask(__name__)
app.debug = True

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

            return "SUCCESS"
        else : 
            return redirect('/register')
    else :
        return render_template('register.html')
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        return "SUCCESS"
    else :
        return render_template('login.html')

@app.route('/', methods=['GET', 'POST']) # 경로(그 쪽 경로에 입장하면 실행)/로그인,관리자OX
def hello_world():
    return render_template('home.html', name="안정연") # 섞는 게 가능
   
    #'<h1>Hello World!</h1>' # h1과tag가 만나면 tag의 기능만 캡쳐함

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    # articles = Articles()

    query = 'SELECT * FROM topic;'

    cur.execute(query)

    db.commit()

    articles = cur.fetchall()

    print(articles)
    return render_template( "articles.html", articles = articles )


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
        return render_template('article.html', article = article )


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
        return render_template("add_article.html")

@app.route("/article/<id>/edit", methods = ['GET','POST'])

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

        return render_template('edit_article.html', article = article)
        

        

if __name__ == '__main__':
    app.run(port=5000)

# 서버 띄우기 GET 방식으로 Enter만 치는 것.





