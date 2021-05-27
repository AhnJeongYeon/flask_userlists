from os import name
from flask import Flask , render_template

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
    return render_template("articles.html")

if __name__ == '__main__':
    app.run(port=5000)

# 서버 띄우기 GET 방식으로 Enter만 치는것.




