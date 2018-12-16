import database as db
import json
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    """Index Homepage"""
    db.init_db()
    return "Home Page"


@app.route("/todolist", methods=['GET', 'POST'])
def todolist():
    """To do list based on given HTML method"""
    if request.method == 'GET':
        return todolist_get()
    else:
        return todolist_post()


def todolist_get():
    """To do list with HTML GET method"""
    done_ctr = 0
    notdone_ctr = 0
    header = "<pre>"
    post = ""
    for task in db.query_fetchall_db("SELECT * FROM tasks"):
        if task[1] == 1:
            post += "[X] "
            done_ctr += 1
        else:
            post += "[ ] "
            notdone_ctr += 1
        post += str(done_ctr+notdone_ctr) + " " + task[0] + "\n"
    header += "To-do list (" + str(done_ctr+notdone_ctr) + " tasks, "
    header += str(done_ctr) + " done, " + str(notdone_ctr) + " to do)\n"
    post += "</pre>"
    return header+post


def todolist_post():
    content = request.get_json(force=True)
    cur = db.query_edit_db(
        """INSERT INTO Tasks(title, done, author_ip, created_date)
         VALUES (?, ?, ?, ?)""",
        args=(
            content["title"],
            False if "done" not in content else bool(content["done"]),
            request.remote_addr,
            datetime.now().replace(microsecond=0).isoformat(' ')
        )
    )
    return jsonify(task_id=cur.lastrowid)


@app.route("/todolist/<int:task_id>", methods=['GET', 'PATCH'])
def todolist_task(task_id):
    if request.method == 'GET':
        return todolist_task_get(task_id)
    else:
        return todolist_task_patch(task_id)


def todolist_task_get(task_id):
    if(check_if_exists(task_id)):
        return task_not_found()
    else:
        task = db.query_fetchall_db(
            "SELECT * FROM tasks WHERE rowid = ?",
            [task_id]
        )[0]
        return jsonify(
            title=str(task[0]),
            done=bool(task[1]),
            author_ip=str(task[2]),
            created_date=str(task[3])
        )


def todolist_task_patch(task_id):
    if(check_if_exists(task_id)):
        return task_not_found()
    else:
        content = request.get_json(force=True)
        task = db.query_fetchall_db(
            "SELECT * FROM tasks WHERE rowid = ?",
            [task_id]
        )[0]
        db.query_fetchall_db(
            "UPDATE tasks SET title = ?, done = ? WHERE rowid = ?",
            [
                str(task[0]) if "title" not in content else content["title"],
                bool(task[1]) if "done" not in content else bool(content["done"]),
                task_id
            ]
        )
        return jsonify(status=204, text="Updated successfully")


def check_if_exists(task_id):
    count = db.query_fetchall_db("SELECT Count(*) FROM tasks")
    if(task_id > count[0][0] or task_id < 1):
        return True
    else:
        return False


def task_not_found():
    return jsonify(error=404, text="Task not found")
