import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request
from datetime import datetime,timezone, timedelta

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>楊子青Python網頁2023-11-14</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=楊子青>傳送使用者暱稱</a><br>"
    homepage += "<a href=/about>子青簡介網頁</a><br>"
    homepage += "<a href=/account>網頁表單輸入帳密傳值</a><br><br>"
    homepage += "<a href=/read>人選之人演員</a><br>"
    homepage += "<a href=/search>根據角色查詢演員</a><br><br>"
    homepage += "<a href=/books>精選圖書列表</a><br>"
    return homepage


@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    tz = timezone(timedelta(hours=+8))
    now = datetime.now(tz)
    return render_template("today.html",datetime = str(now))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")


@app.route("/read")
def read():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("人選之人─造浪者")    
    docs = collection_ref.get()    
    for doc in docs:         
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form["keyword"]
        Result = "您輸入的角色關鍵字是：" + keyword + "，查詢結果如下：<br><br>"
        db = firestore.client()
        collection_ref = db.collection("人選之人─造浪者")    
        docs = collection_ref.order_by("birth").get()    
        for doc in docs:
            x = doc.to_dict()
            if keyword in x["role"]:    
                Result += x["name"] + "在劇中扮演" + x["role"] + "，出生於西元" + str(x["birth"]) + "<br>" 
        return Result
    else:
        return render_template("cond.html")

@app.route("/books")
def books():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("圖書精選")    
    docs = collection_ref.order_by("anniversary").get()    
    for doc in docs:
        bk = doc.to_dict()
        Result += "書名：<a href=" + bk["url"] + ">" + bk["title"] + "</a><br>"
        Result += "作者：" + bk["author"] + "<br>"
        Result += str(bk["anniversary"]) + "週年<br>"
        Result += "<img src=" + bk["cover"] + "></img><br><br>" 
    return Result

if __name__ == "__main__":
    app.run(debug=True)