import os
import re
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import (
  MySQLDatabase,
  SqliteDatabase,
  Model,
  CharField,
  TextField,
  DateTimeField,
)
from playhouse.shortcuts import model_to_dict
import datetime

load_dotenv()
app = Flask(__name__)

# database creation
if os.getenv("TESTING") == "true":
  print("Running in test mode")
  mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
  mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
  )


# define models
class TimelinePost(Model):
  name = CharField()
  email = CharField()
  content = TextField()
  created_at = DateTimeField(default=datetime.datetime.now)

  class Meta:
    database = mydb

# connect and attach models
mydb.connect()
mydb.create_tables([TimelinePost])



# app variables

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


# page routes

@app.route('/')
def index():
  return render_template('index.html', title=title, experiences=experiences, url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
  return render_template('hobbies.html', title=title, url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
  timeline_posts = get_timeline_posts()['timeline_posts']
  return render_template('timeline.html', title=title, timeline_posts=timeline_posts, url=os.getenv("URL"))


# api routes

@app.route('/api/timeline_post', methods=['POST'])
def post_timeline_post():
  # Get form data
  name = request.form.get('name', '').strip()
  email = request.form.get('email', '').strip()
  content = request.form.get('content', '').strip()

  # Validate name
  if not name:
    return 'Invalid name', 400

  # Validate content
  if not content:
    return 'Invalid content', 400

  # Validate email format
  email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
  if not email or not re.match(email_pattern, email):
    return 'Invalid email', 400

  # Create timeline post if all validations pass
  timeline_post = TimelinePost.create(name=name, email=email, content=content)

  return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_posts():
  return {
    'timeline_posts': [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
  }

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_timeline_post():
  post_id = request.form['id']
  post = TimelinePost.get(TimelinePost.id == post_id)
  post.delete_instance()
  return {'status': 'success', 'message': 'Post deleted successfully'}
