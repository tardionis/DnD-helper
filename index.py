from flask import Flask, g, render_template, request, redirect
import sqlite3
import os
from moduleFlask import *

#Link zu meiner Database

app = Flask(__name__)
#wenn ich mit dieser Datei öffne heißt die app "_main_"
app.config['DEBUG'] = True
#Debug mode True
app.config['SECRET_KEY'] = 'super-secret'
#Key = super-secret

DATABASE = "./database/DnD.db"
#Link zu meiner Database

if not os.path.exists(DATABASE):
    global conn
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("""create table party (
                pid INTEGER PRIMARY KEY,
                Name text,
                MaxLeben INTEGER,
                Leben INTEGER,
                'Armor Class' INTEGER
                );
                """)
    conn.commit()
    conn.close()

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/kampfsystem/auto", methods= ["GET", "POST"])
def autoKampfsystem():
    return pers("charakterWahl.html", "party")

@app.route("/kampfsystem",methods = ["POST","GET"])
def Kampfsystem():
    Schaden = None;
    if request.method == "POST":
        if 'user' in request.form:
            user = request.form["user"]
            return attacken(user)
        elif 'opfer' in request.form:
            opfer = request.form["opfer"]
            schad = request.form["schaden"]
            link = 'kampfsystem'
            return schaden(opfer, schad, link)
        else:
            return render_template("<script> alert('scheiße');</script>")
    return pers("kampfsystem.html", "party")

@app.route("/table/<table>",methods = ["POST","GET"])
def table(table):
    if request.method == "POST":
        if 'bin' in request.form:
            garbage = request.form["bin"]
            bin(garbage, table)
        if 'pencil' in request.form:
            pencil = request.form["pencil"]
            return redirect("/anmelden/{}/{}".format(table, pencil))
            print('hallo')
        print(1)
    print(2)
    return pers("table.html", table)

@app.route("/anmelden/<table>/<user>",methods = ["POST","GET"])
def editieren(table, user):
    return edit("edit.html", "anmelden/{}/{}".format(table, user), table, user)

@app.route("/anmelden/<table>",methods = ["POST","GET"])
def partymelden(table):
    return anmelden("anmelden.html", "anmelden/"+table, table)

@app.route("/")
def start():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port="8080")
