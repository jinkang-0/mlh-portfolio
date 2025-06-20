import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

experiences = [
  {
    "title": "Software Engineer Intern",
    "company": "Moody's Analytics",
    "date": "June 2024 - Aug. 2024",
    "location": "Remote"
  },
  {
    "title": "Full Stack Developer",
    "company": "University of California, Berkeley, School of Education",
    "date": "Oct. 2023 - May 2024",
    "location": "Berkeley, CA"
  },
  {
    "title": "Full Stack Developer",
    "company": "Immigration Justice Project",
    "date": "Sep. 2023 - June 2024",
    "location": "Berkeley, CA"
  }
]

title = "Jinkang Fang"

@app.route('/')
def index():
  return render_template('index.html', title=title, experiences=experiences, url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
  return render_template('hobbies.html', title=title, url=os.getenv("URL"))
