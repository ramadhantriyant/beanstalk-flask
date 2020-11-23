import os
from flask import Flask, render_template, redirect, url_for, request
from models.todos import Todos

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/", methods=['GET', 'POST'])
def home():
    todos = Todos.find_all()

    if request.method == "post":
        task = request.form['task']
        todo = Todos(task, False)
        todo.save_to_db()

    return render_template("home.html", todos=todos)


@app.route("/new", methods=['POST'])
def new_task():
    task = request.form['task']
    todo = Todos(task, False)
    todo.save_to_db()
    
    return redirect(url_for("home"))


@app.route("/edit/<int:id>")
def edit_task(id):
    task = Todos.find_by_id(id)
    task.done = True
    task.save_to_db()

    return redirect(url_for("home"))


@app.route("/delete/<int:id>")
def delete_task(id):
    task = Todos.find_by_id(id)
    task.delete_from_db()

    return redirect(url_for("home"))

if __name__ == "__main__":
    from db import db

    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(debug=True)
