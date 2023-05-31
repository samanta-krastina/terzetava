from flask import Flask, render_template, redirect, request
from datetime import datetime
import json
import sqlite3
import create_table_user_logins

# Izveido Flask aplikaciju
app = Flask('app')
app.config['JSON_AS_ASCII'] = False

# Izveidot DB chatroom_datas.db un 2 tabulas
create_table_user_logins.create_logins_table()
create_table_user_logins.create_chat_table()


# Pirmais logs pievienojoties - piedava login/register pogu opcijas
@app.route('/')
def landing():
  return render_template('landing.html')


# Chata galvenais logs
@app.route('/chats')
def sakums():
  return render_template("chatroom.html")


# Ielade jaunakaas zinas no messages.json
@app.route('/read_msg')
def read_msg():
  with open('data/messages.json', 'r', encoding="utf-8") as f:
    messages = f.read()
  return messages


@app.route('/sutit/<vards>/<zina>')
def sutit(vards, zina):
  tagad = datetime.now()
  laiks = tagad.strftime("%d.%m.%Y. %H:%M:%S")

  rinda = {
    "vards": vards,
    "zina": zina,
    "laiks": laiks
  }
  # Seit bus DB chat table
  print(rinda)
  # Jaunierakstito chata zinu ievieto chat tabula
  conn = sqlite3.connect('chatroom_data.db')
  c = conn.cursor()
  c.execute("INSERT INTO chat (username, message, time) VALUES (?, ?, ?)", (vards, zina, laiks))
  conn.commit()
  conn.close()

  with open("data/messages.json", "r", encoding="utf-8") as r:
    vecie = r.read()
    rindas = json.loads(vecie)

  rindas.append(rinda)

  with open("data/messages.json", "w", encoding="utf-8") as w:
    w.write(json.dumps(rindas, indent=2, ensure_ascii=False))
  return "OK"


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('chatroom_data.db')
    c = conn.cursor()
    # Find user with provided username and password
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()

    if user:
      # Ja izdodas ielogoties, redirect uz chats
      return redirect('/chats')
    else:
      # Ja neizdodas ielogoties, pieprasa atkartoti
      return render_template('login.html', error='Nepareizs lietotajvards vai parole!')
  else:
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('chatroom_data.db')
    c = conn.cursor()

    # Parbauda, vai DB jau eksiste dotais username
    c.execute("SELECT * FROM users WHERE username=?", (username, ))
    user = c.fetchone()

    if user:
      # Lietotajs jau eksisete, atver register.html apr jaunu
      return render_template('register.html', error='Lietotajvards jau ir registrets!')
    else:
      # Pievienot jaunu lietotaaju tabulaa, atver login.html lapu
      c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
      conn.commit()
      conn.close()
      return redirect('/login')
  else:
    return render_template('register.html')

# Palaist Flask aplikaciju - gan uz localhost, gan datora IPv4 adreses lokalaja tiklaa
app.run(host='0.0.0.0', port=8080, debug=True)