from flask import Flask, render_template;
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
    
    
#commit changes to db
    conn.commit()
    conn.close()

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")
