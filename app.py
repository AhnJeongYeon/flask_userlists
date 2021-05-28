from flask import Flask , render_template
from data import Articles

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET', 'POST']) # 경로(그 쪽 경로에 입장하면 실행)/로그인,관리자OX
def hello_world():
    return render_template('home.html', name="안정연") # 섞는 게 가능
   
    #'<h1>Hello World!</h1>' # h1과tag가 만나면 tag의 기능만 캡쳐함

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    articles = Articles()
    return render_template( "articles.html", articles = articles )

@app.route('/article/<id>', methods=['GET', 'POST'])
def article(id):
    articles = Articles()
    print(len(articles))
    article = articles[int(id)-1]
    if len(articles)<=int(id):
        
        return render_template("article.html", article = article)
    else:
        return render_template("article.html", article = "NO DATA")

@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    return render_template( "add_article.html" )

if __name__ == '__main__':
    app.run(port=5000)

# 서버 띄우기 GET 방식으로 Enter만 치는것.




