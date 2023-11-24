from flask import Flask, render_template, request, redirect, url_for;
import sqlite3
import datetime

app = Flask(__name__)


#create database for user inputs
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
#create table of weekdays
    c.execute("SELECT COUNT(*) FROM weekdays")
    if c.fetchone()[0] == 0:
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
              (id INTEGER PRIMARY KEY AUTOINCREMENT,task_id INTEGER,day TEXT,
               FOREIGN KEY(task_id) REFERENCES daily_tasks(id)
              )"""
              )
    
#commit changes to db
    conn.commit()
    conn.close()

init_sqlite_db()
conn = sqlite3.connect('database.db')
c = conn.cursor()

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

#handle forms from add_task page
@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.form["task"]
    days = request.form.getlist("days")
    time_allotment = request.form["time_allotment"]
    c.execute("INSERT INTO daily_tasks (task, time_allotment) VALUES (?,?)", (task, time_allotment))
    task_id = c.lastrowid
    for day in days:
        c.execute('INSERT INTO task_days (task_id, "day") VALUES (?,?)', (task_id, day))
    conn.commit()
    return redirect(url_for("index"))

#BEGIN CODE FOR TASK VIEW PAGE
from flask import g

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/today_tasks")
def today_tasks():
    conn = get_db()
    c = conn.cursor()

    #get current day
    current_day = datetime.datetime.now().strftime('%A')

    #retrieve tasks from database
    c.execute("""
              SELECT daily_tasks.task, daily_tasks.time_allotment
              FROM daily_tasks 
              JOIN task_days ON daily_tasks.id = task_days.task_id
              WHERE task_days.day = ?
              """, (current_day,))
    tasks = c.fetchall()

    conn.commit()
    conn.close()

    return render_template('today.html', tasks=tasks)