import json
from flask import Flask, send_from_directory, request, render_template, make_response, redirect, session
from flask_session import Session
import base64
import sqlite3
import hashlib
import uuid
import os

app = Flask(__name__, static_url_path='',
            static_folder='../client/public',
            template_folder="../client/public")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
uploads_dir = '../client/public/photos'


def Connect(sqlCommand: str):
    myConnection = sqlite3.connect('users.sqlite')
    cursor = myConnection.cursor()
    cursor.execute(sqlCommand)
    output = cursor.fetchall()
    myConnection.commit()
    myConnection.close()
    return output

def ConnectArgs(sqlCommand : str, argument):
    myConnection = sqlite3.connect('users.sqlite')
    cursor = myConnection.cursor()
    cursor.execute(sqlCommand, argument)
    output = cursor.fetchall()
    myConnection.commit()
    myConnection.close()
    return output


def convertToBinaryData(file):
    blobData = file.read()
    return blobData



# utwórz bazę danych jeśli nie istnieje
Connect("CREATE TABLE IF NOT EXISTS users ( nickname TEXT UNIQUE NOT NULL, password TEXT NOT NULL, admin INT1 DEFAULT 0)")
try:
    Connect("INSERT INTO users (nickname, password, admin) VALUES ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 1)")
except:
    print("admin juz byl")
Connect("CREATE TABLE IF NOT EXISTS slider (title TEXT UNIQUE NOT NULL, description TEXT NOT NULL, photo BLOB, href TEXT DEFAULT '/')")
Connect("CREATE TABLE IF NOT EXISTS articles (title TEXT UNIQUE NOT NULL, content TEXT NOT NULL, comments TEXT, category TEXT)")
Connect("CREATE TABLE IF NOT EXISTS news (id INTEGER NOT NULL PRIMARY KEY, title TEXT NOT NULL DEFAULT '', text TEXT NOT NULL DEFAULT '')")
Connect("CREATE TABLE IF NOT EXISTS block (id INTEGER NOT NULL PRIMARY KEY, title TEXT NOT NULL DEFAULT '', text TEXT NOT NULL DEFAULT '', img BLOB DEFAULT NULL)")
Connect("CREATE TABLE IF NOT EXISTS styles (id INTEGER NOT NULL PRIMARY KEY, colors TEXT NOT NULL, font TEXT NOT NULL, ord INT NOT NULL, sel INT NOT NULL)")


if len(Connect("SELECT * FROM block WHERE id = 0")) == 0:
    Connect("INSERT INTO block (id, title, text) VALUES (0, 'null', 'null')")


@app.route("/")
def base():
    return send_from_directory('../client/public', 'index.html')


@app.route("/register", methods=["POST"])
def register():
    req = request.get_json()
    nickname = req.get("nickname")
    password = req.get("password")
    password = password.encode()
    password = hashlib.sha256(password)
    password = password.hexdigest()
    session["nickname"] = nickname

    data = {}
    try:
        Connect(f"INSERT INTO users VALUES ('{nickname}', '{password}', 0)")
        data["success"] = True
    except sqlite3.IntegrityError:
        data["success"] = False
        data["message"] = "This nickname already exists"
    except:
        data["success"] = False
        data["message"] = "Unexpected error"
    finally:
        return app.response_class(response=json.dumps(data), status=200, mimetype="application/json")


@app.route("/delUser", methods=["POST"])
def delUser():
    req = request.get_json()
    nickname = req.get("nickname")
    Connect(f"DELETE FROM users WHERE nickname = '{nickname}'")
    if(session["admin"]):
        leftUsers = Connect("SELECT * FROM users")
        return app.response_class(response=json.dumps(leftUsers), status=200, mimetype="application/json")
    else:
        return app.response_class(response=json.dumps([]), status=200, mimetype="application/json")


@app.route("/logIn", methods=["POST"])
def logIn():
    req = request.get_json()
    nickname = req.get("nickname")
    password = req.get('password')
    password = password.encode()
    password = hashlib.sha256(password)
    password = password.hexdigest()

    users = Connect("SELECT * FROM users ORDER BY oid")
    data = json.dumps({"logged": False, "admin": False})
    for x in users:
        if x[0] == nickname and x[1] == password:
            if x[2] == 0:
                data = json.dumps({"logged": True, "admin": False})
                session["logged"] = True
                session["admin"] = False
                session["nickname"] = nickname
                break
            else:
                data = json.dumps({"logged": True, "admin": True})
                session["logged"] = True
                session["admin"] = True
                session["nickname"] = nickname
                break
    res = app.response_class(response=data, status=200,
                             mimetype='application/json')
    return res


@app.route("/checkLogin", methods=["POST", ])
def checkLogin():
    data = {"logged": session.get("logged", False), "admin": session.get("admin", False), "nickname": session.get("nickname")}
    return app.response_class(response=json.dumps(data), status=200, mimetype="application/json")


@app.route("/logOut", methods=["POST", "GET"])
def logOut():
    session["logged"] = None
    session["admin"] = None
    session["nickname"] = None
    return redirect("/", code=301)


@app.route("/loadUsers", methods=["POST"])
def loadUsers():
    if(session["admin"]):
        users = Connect("SELECT * FROM users")
        return app.response_class(response=json.dumps(users), status=200, mimetype="application/json")
    else:
        users = Connect(f"SELECT * FROM users WHERE nickname ='{session['nickname']}'")
        return app.response_class(response=json.dumps(users), status=200, mimetype="application/json")

@app.route("/changeUser", methods=["POST"])
def changeUser():
    req = request.get_json(force= True)
    password = req["password"]
    if password == '':
        password = Connect(f"SELECT password FROM users WHERE nickname = '{req['oldNickname']}'")[0][0]
    else:
        password = password.encode()
        password = hashlib.sha256(password)
        password = password.hexdigest()
    Connect(f"UPDATE users SET nickname= '{req['nickname']}', password = '{password}', admin = '{req['access']}' WHERE nickname = '{req['oldNickname']}' ")
    if(session["admin"]):
        if(req["oldNickname"] == session["nickname"]):
            session["nickname"] == req["nickname"]
        users = Connect("SELECT * FROM users")
        return app.response_class(response=json.dumps(users), status=200, mimetype="application/json")
    else:
        session['nickname'] = req["nickname"]
        users = Connect(f"SELECT * FROM users WHERE nickname ='{session['nickname']}'")
        return app.response_class(response=json.dumps(users), status=200, mimetype="application/json")

@app.route("/pushSlide", methods=["POST"])
def pushSlide():
    title = request.form["title"]
    description =  request.form["description"]
    href = request.form["href"]
    img = request.files["img"]
    ConnectArgs("INSERT INTO slider VALUES (?, ?, ?, ?)", (title, description, img.read(), href))
    #Connect("INSERT INTO slider VALUES ('" + title +"', '" + description + "', " +  str(img.read()) + ", '" + href + "')")
    return app.response_class(response=json.dumps({"success": True}), status=200, mimetype="application/json")

@app.route("/loadSlider", methods=["POST"])
def loadSlider():
    data = Connect("SELECT * FROM slider")
    res = []
    for x in data:
        res.append({"title":x[0], "description":x[1], "image": base64.b64encode(x[2]).decode(), "href": x[3]})
    return app.response_class(response=json.dumps(res), status=200, mimetype="application/json")

@app.route("/delSlider", methods=["POST"])
def delSlider():
    req = request.get_json()
    Connect(f"DELETE FROM slider WHERE title = '{req['title']}'")
    return app.response_class(response=json.dumps({"success": True}), status=200, mimetype="application/json")

@app.route("/addArticle", methods=["POST"])
def addArticle():
    req = request.get_json()
    try:
        Connect(f"INSERT INTO articles VALUES('{req['title']}', '{req['content']}', '[]', '{req['category']}')")
        return app.response_class(response=json.dumps({"success": True}), status=200, mimetype="application/json")
    except sqlite3.IntegrityError:
        return app.response_class(response = json.dumps({"success": False, "err": "Article with this title already exists"}), status=400, mimetype="application/json")
    except:
        return app.response_class(response=json.dumps({"success": False, "err": "Unexpected error"}), status=500, mimetype="application/json")

@app.route("/getArticles", methods=["POST"])
def getArticles():
    articles = Connect("SELECT * FROM articles")
    return app.response_class(response=json.dumps(articles), status=200, mimetype="application/json")

@app.route("/delArticle", methods=["POST"])
def delArticle():
    req = request.get_json(force=True)
    Connect(f"DELETE FROM articles WHERE title = '{req['title']}'")
    return app.response_class(response=json.dumps({"success": True}), status=200, mimetype="application/json")

@app.route("/showArticle", methods=["POST"])
def showArticle():
    req = request.get_json()
    data = Connect(f"SELECT * FROM articles WHERE title = '{req['title']}'")
    res = {"title": data[0][0], "content": data[0][1], "comments": data[0][2], "category": data[0][3]}
    return app.response_class(response=json.dumps(res), status=200, mimetype="application/json")

@app.route("/editArticle", methods=["POST"])
def editArticle():
    req = request.get_json()
    Connect(f"UPDATE articles SET title = '{req['title']}', content = '{req['content']}', category = '{req['category']}' WHERE title = '{req['oldTitle']}' ")
    return app.response_class(response=json.dumps({"success": True}), status=200, mimetype="application/json")

@app.route("/pushComment", methods=["POST"])
def pushComment():
    req = request.get_json()
    strComments = Connect(f"SELECT comments FROM articles WHERE title = '{req['title']}'")
    Comments = json.loads(strComments[0][0])
    Comments.append({"nickname": req["nickname"], "comment": req["comment"]})
    strComments = json.dumps(Comments)
    Connect(f"UPDATE articles SET comments = '{strComments}' WHERE title = '{req['title']}'")
    return app.response_class(response=strComments, status=200, mimetype="application/json")

@app.route("/delComment", methods=["POST"])
def delComment():
    req = request.get_json()
    strComments = Connect(f"SELECT comments FROM articles WHERE title = '{req['title']}'")[0][0]
    comments: list = json.loads(strComments)
    comments.remove(req['comment'])
    strComments = json.dumps(comments)
    Connect(f"UPDATE articles SET comments = '{strComments}' WHERE title = '{req['title']}'")
    return app.response_class(response=strComments, status=200, mimetype="application/json")

@app.route("/applyFilters", methods=["POST"])
def applyFilters():
    req = request.get_json()
    articles = Connect(f"SELECT * FROM articles WHERE title LIKE '%{req['search']}%' OR category LIKE '%{req['search']}%' ORDER BY {req['sort']}")
    return app.response_class(response=json.dumps(articles), status=200, mimetype="application/json")

@app.route("/public/<path:path>", methods=["GET", "POST"])
def catch_all(path):
    return send_from_directory("../client/public", path)


@app.route("/getContent", methods=["GET", "POST"])
def getcontent():
    data = {"content": {}}
    try:
        res = Connect("SELECT title, text, id FROM news")
        rr = []
        for r in res:
            rr.append({"title": r[0], "text": r[1], "id": r[2]})
        data["content"]["news"] = rr
        res = Connect("SELECT title, text FROM block")
        rrr = {}
        if len(res) == 0:
            rrr = {"title": "null", "text": "null"}
        else:
            rrr["title"] = res[0][0]
            rrr["text"] = res[0][1]
        data["content"]["block"] = rrr
        data["success"] = True
    except:
        print("zle")
        data["success"] = False
        data["message"] = "Unexpected error"
    finally:
        return app.response_class(response=json.dumps(data), status=200, mimetype="application/json")


@app.route("/saveContent", methods=["POST"])
def savecontent():
    req = request.get_json()
    block = req["block"]
    ConnectArgs("UPDATE block SET title = ?, text = ? WHERE id = 0",
                (block["title"], block["text"]))
    news = req["news"]
    for ne in news:
        if "id" in ne:
            ConnectArgs(
                "UPDATE news SET title = ?, text = ? WHERE id = ?", (ne["title"], ne["text"], ne["id"]))
    res = Connect("SELECT id FROM news")
    tt = []
    for u in res:
        tt.append(u[0])
    for u in news:
        if "id" in u:
            tt.remove(u["id"])
    idlist = ', '.join(str(v) for v in tt)
    Connect(f"DELETE FROM news WHERE id IN ({idlist})")
    for ne in news:
        if "id" not in ne:
            ConnectArgs(
                "INSERT INTO news (title, text) VALUES (?, ?)", (ne["title"], ne["text"]))
    return app.response_class(response=json.dumps({"ok": "true"}), status=200, mimetype="application/json")


@app.route("/saveBImg", methods=["POST"])
def savebimg():
    file = request.files["img"]
    if file:
        ConnectArgs("UPDATE block SET img = ? WHERE id = 0", (file.read(),))
    return app.response_class(response=json.dumps({"ok": "true"}), status=200, mimetype="application/json")


@app.route("/getBImg", methods=["POST", "GET"])
def getbimg():
    res = Connect("SELECT img FROM block WHERE id = 0")
    img = res[0][0]
    return app.response_class(response=img, status=200, mimetype="application/octet-stream")


@app.route("/saveStyles", methods=["POST"])
def savestyles():
    req = request.get_json()
    Connect("DELETE FROM styles")
    for r in req:
        ConnectArgs("INSERT INTO styles (colors, font, ord, sel) VALUES (?, ?, ?, ?)",
                    (r["col"], r["font"], r["ord"], r["sel"]))
    return app.response_class(response=json.dumps({"ok": "true"}), status=200, mimetype="application/json")


@app.route("/getStyles", methods=["GET", "POST"])
def getstyles():
    con = Connect("SELECT colors,font,ord,sel FROM styles")
    rr = []
    for r in con:
        rr.append({"col": r[0], "font": r[1], "ord": r[2], "sel": bool(r[3])})
    return app.response_class(response=json.dumps(rr), status=200, mimetype="application/json")

@app.route("/addPhoto", methods = ["POST"])
def addPhoto():
    img = request.files["img"]
    print(img)
    uniqueFileName = str(uuid.uuid4())
    img.filename = uniqueFileName 
    img.save(os.path.join(uploads_dir, img.filename))
    return app.response_class(response=json.dumps({"success": True}), status=200, mimetype="application/json")

@app.route("/photos/<name>", methods = ["POST", "GET"])
def photos(name):
    return send_from_directory("../client/public/photos", name)

@app.route("/getPhotosNames", methods = ["POST"])
def getPhotosNames():
    files = os.listdir("../client/public/photos")
    return app.response_class(response=json.dumps({"files": files}), status=200, mimetype="application/json")

@app.route("/deletePhoto", methods= ["POST"])
def deletePhoto():
    req = request.get_json()
    os.remove("../client/public/photos/" + req['name'])
    return app.response_class(response=json.dumps({"success": True}), status=200, mimetype="application/json")

@app.errorhandler(404)
def not_found(lol):
    print("404")
    return make_response(
        render_template("index.html"),
        200
    )


if __name__ == "__main__":
    app.run(debug=True)
