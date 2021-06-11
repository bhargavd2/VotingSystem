from flask import Flask, render_template, redirect, request, url_for, session
from firebase import Firebase

config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": ""
}
firebase = Firebase(config)

auth = firebase.auth()

db = firebase.database()

app = Flask(__name__)
app.secret_key = ""

# index route
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/<message>", methods=["GET"])
def indexi(message):
    return render_template("index.html", messages=message)


@app.route("/main", methods=["GET"])
def main():
    if session.get("admin") == False:
        try:
            c = db.child("candidates").get()
            data = []
            for i in c.each():
                a = i.val()
                b = i.key()
                if a == None:
                    continue
                a.pop("votes")
                data.append(a)
            return render_template("main.html", list=data)
        except:
            redirect(url_for('.indexi', message="error loading election"))
    else:
        return redirect(url_for('.indexi', message="invalid access pls login"))


@app.route("/main/<messages>", methods=["GET"])
def maini(messages):
    if session.get("admin") == False:
        try:
            c = db.child("candidates").get()
            data = []
            for i in c.each():
                a = i.val()
                b = i.key()
                if a == None:
                    continue
                a.pop("votes")
                data.append(a)
            return render_template("main.html", list=data, message=messages)
        except:
            redirect(url_for('.indexi', message="error loading election"))
    else:
        return redirect(url_for('.indexi', message="invalid access pls login"))


# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get the request data
        email = request.form["email"]
        password = request.form["password"]

        if email == "admin@test.com" and password == "123456":
            session["admin"] = True
            return redirect("/control")
        else:
            try:
                e = db.child("election").get()
                if e.val() == True:
                # login the user
                    user = auth.sign_in_with_email_and_password(email, password)
                    v = db.child("voters").get()
                    flag = "false"
                    for i in v.each():
                        a = i.val()
                        b = i.key()
                        if a == None:
                            continue
                        if a["email"] == email:
                            flag = a["status"]
                            break
                    if flag.lower() == "true":
                        return redirect(url_for('.indexi', message="election over"))
                else:
                    return redirect(url_for('.indexi', message="election not started"))
                # set the session
                user_email = email
                session["email"] = user_email
                session["admin"] = False
                return redirect("/main")
            except:
                return redirect(url_for('.indexi', message="Wrong Credentials"))

    return render_template("index.html")


# logout route
@app.route("/logout")
def logout():
    # remove the token setting the user to None
    auth.current_user = None
    # also remove the session
    # session['usr'] = ""
    # session["email"] = ""
    session.clear()
    return redirect("/")


@app.route("/addV", methods=["GET", "POST"])
def addV():
    if session.get("admin") == True:
        if request.method == "POST":
            try:
                id = request.form["id"]
                email = request.form["email"]
                password = request.form["pass"]
                auth.create_user_with_email_and_password(email, password)
                a = {}
                a["email"] = email
                a["id"] = id
                a["status"] = "false"
                user = auth.sign_in_with_email_and_password(email, password)
                a["uid"] = user["localId"]
                auth.current_user = None
                db.child("voters").child(id).update(a)
                return redirect(url_for('.controli', messages="added voter"))
            except:
                return redirect(url_for('.controli', messages="error adding voter"))
        else:
            return render_template("addvoter.html")
    else:
        return redirect(url_for('.indexi', message="invalid access pls login as admin"))


@app.route("/addC", methods=["GET", "POST"])
def addC():
    if session.get("admin") == True:
        if request.method == "POST":
            try:
                id = request.form["id"]
                email = request.form["name"]
                party = request.form["party"]
                a = {}
                a["id"] = id
                a["name"] = email
                a["party"] = party
                a["votes"] = 0
                auth.current_user = None
                db.child("candidates").child(id).update(a)
                return redirect(url_for('.controli', messages="added candidate"))
            except:
                return redirect(url_for('.controli', messages="error adding candidate"))
        else:
            return render_template("adcand.html")
    else:
        return redirect(url_for('.indexi', message="invalid access pls login as admin"))


@app.route("/deleteV", methods=["GET", "POST"])
def deleteV():
    if session.get("admin") == True:
        if request.method == "POST":
            try:
                id = request.form["id"]
                db.child("voters").child(id).remove()
                return redirect(url_for('.controli', messages="deleted voter"))
            except:
                return redirect(url_for('.controli', messages="error deleting voter"))
        else:
            return render_template("removevoter.html")
    else:
        return redirect(url_for('.indexi', message="invalid access pls login as admin"))


@app.route("/deleteC", methods=["GET", "POST"])
def deleteC():
    if session.get("admin") == True:
        if request.method == "POST":
            try:
                id = request.form["id"]
                db.child("candidates").child(id).remove()
                return redirect(url_for('.controli', messages="deleted candidate"))
            except:
                return redirect(url_for('.controli', messages="error deleting candidate"))
        else:
            return render_template("remcand.html")
    else:
        return redirect(url_for('.indexi', message="invalid access pls login as admin"))


@app.route("/viewV", methods=["GET"])
def viewV():
    if session.get("admin") == True:
        try:
            v = db.child("voters").get()
            data = []
            for i in v.each():
                a = i.val()
                b = i.key()
                if a == None:
                    continue
                a.pop("uid")
                a.pop("status")
                data.append(a)
            return render_template("voterlist.html", list=data)
        except:
            return redirect(url_for('.controli', messages="error loading viewv"))
    else:
        return redirect(url_for('.indexi', message="invalid access pls login as admin"))


@app.route("/viewC", methods=["GET"])
def viewC():
    if session.get("admin") == True:
        try:
            c = db.child("candidates").get()
            data = []
            for i in c.each():
                a = i.val()
                b = i.key()
                if a == None:
                    continue
                a.pop("votes")
                data.append(a)

            return render_template("candlist.html", list=data)
        except:
            return redirect(url_for('.controli', messages="error loading viewc"))
    else:
        return redirect(url_for('.indexi', message="invalid access pls login as admin"))


@app.route("/control", methods=["GET", "POST"])
def control():
    if session.get("admin") == True:
        if request.method == "POST":
            try:
                print(request.form["id"])
                id = request.form["id"]
                mes = ""
                if id == "End the Election":
                    db.child("election").set(False)
                    mes = "election stoped"
                elif id == "Start the Election":
                    v = db.child("voters").get()
                    for user in v.each():
                        a = user.val()
                        b = user.key()
                        if a == None:
                            continue
                        a["status"] = "false"
                        db.child("voters").child(b).update(a)

                    c = db.child("candidates").get()
                    for user in c.each():
                        a = user.val()
                        b = user.key()
                        if a == None:
                            continue
                        a["votes"] = 0
                        db.child("candidates").child(b).update(a)

                    db.child("election").set(True)
                    mes = "election started"
                return redirect(url_for('.controli', messages=mes))
            except:
                return redirect(url_for('.controli', messages="error try again"))
        else:
            return render_template("adminhome.html")
    else:
        return redirect(url_for('.indexi', message="invalid access pls login as admin"))


@app.route("/control/<messages>", methods=["GET"])
def controli(messages):
    if session.get("admin") == True:
        return render_template("adminhome.html", list=messages)
    else:
        return redirect(url_for('.indexi', message="invalid access pls login as admin"))


@app.route("/results", methods=["GET"])
def results():
    if session.get("admin") == True:
        try:
            c = db.child("candidates").get()
            data = []
            for i in c.each():
                a = i.val()
                b = i.key()
                if a == None:
                    continue
                data.append(a)
            return render_template("result.html", list=data)
        except:
            return redirect(url_for('.controli', messages="error try again"))
    else:
        return redirect(url_for('.indexi', message="invalid access pls login as admin"))


@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        try:
            id = request.form["id"]
            c = db.child("candidates").get()
            for i in c.each():
                a = i.val()
                b = i.key()
                if a == None:
                    continue
                if id == str(b):
                    a["votes"] = a["votes"] + 1
                    db.child("candidates").child(b).update(a)
                    break

            v = db.child("voters").get()
            for i in v.each():
                a = i.val()
                b = i.key()
                if a == None:
                    continue
                if session["email"] == a["email"]:
                    a["status"] = "true"
                    db.child("voters").child(b).update(a)
                    break

            return redirect("/logout")
        except:
            return redirect(url_for('.maini', messages="error try again"))
    else:
        return redirect(url_for('.indexi', message="invalid access"))


# run the main script
if __name__ == "__main__":
    app.run(debug=True)
