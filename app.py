from flask import Flask, render_template, request, redirect, url_for;
import sqlite3

app = Flask(__name__)

#create database for user inputs
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
#create table of weekdays
    c.execute("CREATE TABLE IF NOT EXISTS weekdays (day TEXT PRIMARY KEY);")
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    c.executemany("INSERT INTO weekdays VALUES (?)", [(day,) for day in weekdays])

#create table for daily tasks
    c.execute(
              """
              CREATE TABLE IF NOT EXISTS daily_tasks (id INTEGER PRIMARY KEY AUTOINCREMENT,
              time_allotment INTEGER NOT NULL,
              weekday TEXT, task TEXT, FOREIGN KEY(weekday) REFERENCES weekdays(day)
              )
              """
    )
#create table for task_days
    c.execute("""
              CREATE TABLE IF NOT EXISTS task_days
              (id INTEGER PRIMARY KEY AUTOINCREMENT,task_id INTEGER,
               FOREIGN KEY(task_id) REFERENCES daily_tasks(id),day TEXT
              )"""
              )
    
#commit changes to db
    conn.commit()
    conn.close()

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.form["task"]
    days = request.form.getlist("days")
    time_allotment = request.form["time_allotment"]
    conn =sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO daily_tasks (task, time_allotment) VALUES (?,?)", (task, time_allotment))
    task_id = c.lastrowid
    for day in days:
        c.execute("INSERT INTO task_days (task_id, day) VALUES (?,?)" (task_id, day))


    conn.commit()
    conn.close()

    return redirect(url_for("index"))

