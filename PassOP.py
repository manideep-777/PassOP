# from flask import Flask,render_template

# app=Flask(__name__)

# @app.route("/")
# def hello():
#     return render_template("main.html")

# app.run(debug=True)

from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask application
app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'PassOP.db')  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route("/")
def hello():
    # return render_template("main.html")
    all_users = User.query.all()  
    return render_template("main.html", users=all_users)

@app.route("/add_user", methods=['POST'])
def add_user():
    url = request.form.get('url')
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username and password and url:
        new_user = User(url=url, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    
    return "Failed to add user."

if __name__ == "__main__":
    app.run(debug=True)
