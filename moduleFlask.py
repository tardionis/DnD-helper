from flask import Flask, g, render_template, request, redirect
import sqlite3
import os

DATABASE = "./database/DnD.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
#extahiere Database für Flask

def hilfRes(table):
    cur = get_db().cursor()
    return cur.execute("select * from '" + table + "';")

def hilfRes2(table):
    res=hilfRes(table)
    return list(map(lambda x: x[0], res.description))

def curToString(liste):
    liste = list(map(lambda x:list(map(lambda y: y, x)) , liste))
    liste = list(map(lambda x: list(map(str, x)), liste))
    return liste

def curToStringTitle(liste):
    liste = list(map(lambda x: x[0:], liste))
    liste = list(map(str, liste[0:]))
    return liste

def invenGegenstand(user):
    cur = get_db().cursor()
    return cur.execute("select gegenstand.name, gegenstand.effecte, gegenstand.beschreibung from gegenstand, inventar using('gid') where pid= " + user + ";")

def invenAttacke(user):
    cur = get_db().cursor()
    return cur.execute("select attacke.Name, attacke.Attacke, attacke.Schaden, attacke.Würfel from attacke, invenAttacke using('aid') where pid= " + user + ";")

def invenZauber(user):
    cur = get_db().cursor()
    return cur.execute("""select zauber.Name, zauber.Englisch, zauber.Stufe,
    zauber.Klasse, zauber.schule, zauber.Ritual, zauber.Zeit, zauber.Komp,
    zauber.Konz, zauber.Quelle from zauber,
    invenZauber using('zid') where pid= """ + user + ";")

def pers(second, table):
    res= hilfRes(table)
    res2= hilfRes2(table)
    return render_template(second, zeilen=res, len=len(res2), headline=res2)


def persPlus(second, table, weiter):
    cur = get_db().cursor()
    res = cur.execute("select * from " + table + ";")
    res2 = list(map(lambda x: x[0], res.description))
    return render_template(second, zeilen=res, len=len(res2), headline=res2, user=weiter)

def anmelden(second, link, table):
    db = get_db()
    cur = db.cursor()
    res = cur.execute("select * from " + table + ";")
    res2 = list(map(lambda x: x[0], res.description))
    res3 = map(str, res2[1:])
    if request.method == "POST":
        werte = []
        for wert in res3:
            werte = werte + [request.form[wert]]
        wert2 = "','".join(werte)
        res2str = "','".join(map(str, res2[1:]))
        cur.execute("insert into "+ table +"('"+res2str+"') values ('"+ wert2 +"');")
        db.commit()
    else:
        return render_template(second, headline=res2, link=link, table=table)
    return redirect("/" + link)

def attacken(user):
    party = hilfRes("party")
    title = hilfRes2("party")
    gegenstand = invenGegenstand(user)
    titleG = hilfRes2("gegenstand")
    db = get_db()
    cur = db.cursor()
    userName = cur.execute("select Name from party where pid ="+ user + ";").fetchone()
    attacke = invenAttacke(user)
    titleA = hilfRes2("attacke")
    zauber = invenZauber(user)
    titleZ = hilfRes2("zauber")
    party = curToString(party)
    title = curToStringTitle(title)
    return render_template("kampfsystem.html", zeilen=party,
    dieOpfer=party, opferHeadline=title,
    headline=title, user=user, len=len(title), gegenstand=gegenstand,
    headlineGegenstand=titleG, userName=userName[0], attacke=attacke,
    headlineAttacke=titleA, zauber=zauber, headlineZauber=titleZ)


def schaden(user, abzug, link):
    db = get_db()
    cur = db.cursor()
    res = cur.execute("select leben from party where pid ="+ user + ";")
    db = get_db()
    cur = db.cursor()
    MaxLeben = cur.execute("select MaxLeben from party where pid ="+ user + ";")
    res = list(map(lambda x: x[0], res))
    res = list(map(str, res[0:]))
    res = int(res[0])
    abzug = int(abzug)
    res -= abzug
    MaxLeben = list(map(lambda x: x[0], MaxLeben))
    MaxLeben = list(map(str, MaxLeben[0:]))
    MaxLeben = int(MaxLeben[0])
    if (res <= 0):
        res=0
    elif(res > MaxLeben):
        res=MaxLeben
    cur.execute("update party set leben="+ str(res) +" where pid = "+ user +";")
    db.commit()
    party = hilfRes("party")
    res2 = hilfRes2("party")
    res
    return redirect("/"+link)