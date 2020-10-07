from flask import Flask, g, render_template, request, redirect
import sqlite3
import os

DATABASE = "./database/DnD.db"

def get_db(): # getting databases connection Object
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
#extahiere Database für Flask

def hilfRes(table): # get all rows in a specific table
    cur = get_db().cursor()
    return cur.execute("select * from '" + table + "';")

def hilfRes2(table): # get the column names in a specific table
    res=hilfRes(table)
    return list(map(lambda x: x[0], res.description))

def curToString(liste): # making a cursor with multiple rows to a String list list
    liste = list(map(lambda x:list(map(lambda y: y, x)) , liste))
    liste = list(map(lambda x: list(map(str, x)), liste))
    return liste

def curToStringTitle(liste): # making a cursor Object with one row to a String list
    liste = list(map(lambda x: x[0:], liste))
    liste = list(map(str, liste[0:]))
    return liste

def invenGegenstand(user): # select specific Objects of a specific player from inventar
    cur = get_db().cursor()
    return cur.execute("select gegenstand.name, gegenstand.effecte, gegenstand.beschreibung from gegenstand join inventar on id=gid where pid='{}';".format(user))

def invenAttacke(user): # select specific Objects of a specific player from invenAttacke
    cur = get_db().cursor()
    return cur.execute("select attacke.Name, attacke.Attacke, attacke.Schaden, attacke.Würfel from attacke join invenAttacke on id = aid where pid='{}';".format(user))

def invenZauber(user):# select specific Objects of a specific player from invenZauber
    cur = get_db().cursor()
    return cur.execute("""select zauber.Name, zauber.Englisch, zauber.Stufe,
    zauber.Klasse, zauber.schule, zauber.Ritual, zauber.Zeit, zauber.Komp,
    zauber.Konz, zauber.Quelle from zauber join invenZauber on id=zid where pid='{}';""".format(user))

def pers(second, table): # makes an unspecific Html template
    res= hilfRes(table)
    res2= hilfRes2(table)
    return render_template(second, zeilen=res, len=len(res2), headline=res2, table=table)


def persPlus(second, table, weiter): # makes an unspecific Html template that gives you a user object
    cur = get_db().cursor()
    res = cur.execute("select * from '{}';".format(table))
    res2 = list(map(lambda x: x[0], res.description))
    return render_template(second, zeilen=res, len=len(res2), headline=res2, user=weiter, table=table)

def bin(bin, table): # Deletes something out of a list
    db = get_db()
    cur = db.cursor()
    res = cur.execute("delete from '{}' where id = '{}';".format(table, bin))
    if table == 'attacke':
        res = cur.execute("delete from invenAttacke where aid='{}';".format(bin))
    if table == 'zauber':
        res = cur.execute("delete from invenZauber where zid='{}';".format(bin))
    if table == 'gegenstand':
        res = cur.execute("delete from inventar where gid='{}';".format(bin))
    db.commit()

def anmelden(second, link, table): # makes every add tamplate
    db = get_db()
    cur = db.cursor()
    res = cur.execute("select * from '{}';".format(table))
    res2 = list(map(lambda x: x[0], res.description))
    res3 = map(str, res2[1:])
    if request.method == "POST":
        werte = []
        for wert in res3:
            werte = werte + [request.form[wert]]
        wert2 = "','".join(werte)
        res2str = "','".join(map(str, res2[1:]))
        cur.execute("insert into '{}'('{}') values ('{}');".format(table, res2str, wert2))
        db.commit()
    else:
        return render_template(second, headline=res2, link=link, table=table)
    return redirect("/" + link)

def edit(second, link, table, ident): # makes every edit template
    db = get_db()
    cur = db.cursor()
    res = cur.execute("select * from '{}';".format(table))
    res2 = list(map(lambda x: x[0], res.description))
    res3 = list(map(str, res2[1:]))
    res = cur.execute("select * from '{}' where id='{}';".format(table, ident)).fetchone()
    if request.method == "POST":
        werte = []
        for i in range(0, len(res3)):
            werte.append("{}='{}'".format(res3[i], request.form[res3[i]]))
            neueWert = ','.join(werte)
        sql = "update '{}' set {} where id='{}';".format(table, neueWert, ident)
        cur.execute(sql)
        db.commit()
    else:
        return render_template(second, headline=res2, placeholder=res, link=link, table=table)
    return redirect("/" + link)

def attacken(user): # first kampsystem
    party = hilfRes("party")
    title = hilfRes2("party")
    gegenstand = invenGegenstand(user)
    titleG = hilfRes2("gegenstand")
    db = get_db()
    cur = db.cursor()
    userName = cur.execute("select Name from party where id='{}';".format(user)).fetchone()
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


def schaden(user, abzug, link): # handels damage an partymembers
    db = get_db()
    cur = db.cursor()
    res = cur.execute("select leben from party where id='{}';".format(user))
    db = get_db()
    cur = db.cursor()
    MaxLeben = cur.execute("select MaxLeben from party where id='{}';".format(user))
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
    cur.execute("update party set leben='{}' where id='{}';".format(str(res),user))
    db.commit()
    party = hilfRes("party")
    res2 = hilfRes2("party")
    return redirect("/"+link)

# def erstelle_liste() # adding new lists
