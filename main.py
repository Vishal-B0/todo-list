from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///list1.db"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Todolist(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    work: Mapped[str] = mapped_column(String(100))
    time: Mapped[datetime] = mapped_column(DateTime)


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def todo():
    if request.method == "POST":
        task_text = request.form["todowork"]
        raw_task_time = request.form["task-time"]  # string

        if task_text.strip() != "" and raw_task_time.strip() != "":
            task_time = datetime.fromisoformat(raw_task_time)

            new_work = Todolist(
                work=task_text,
                time=task_time
            )

            db.session.add(new_work)
            db.session.commit()

        return redirect(url_for("todo"))

    all_tasks = Todolist.query.all()
    return render_template("todolist2.html", tasks=all_tasks)


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Todolist.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for("todo"))


if __name__ == "__main__":
    app.run(debug=True)