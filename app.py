from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__():
        return '<Task %r>' %self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue adding your task.'

    else:
        tasks = Todo.query.filter_by(completed=False).all()
        return render_template('index.html', tasks=tasks)

@app.route('/del/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'There was a problem deleting your task.'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
            task.content = request.form['content']

            try:
                db.session.commit()
                return redirect('/')

            except:
                return "There was an issue upadating your task."
    else:
        return render_template('update.html', task=task)

@app.route('/mark/<int:id>')
def mark(id):
    try:
        task_to_mark = Todo.query.get_or_404(id)
        task_to_mark.completed = True
        db.session.commit()
        return redirect('/')

    except:
        return 'There was an issue marking your task as done.'

@app.route('/completed')
def completed():
    completed_tasks = Todo.query.filter_by(completed=True).all()
    return render_template('done.html', completed_tasks=completed_tasks)

@app.route('/completed/del/<int:id>')
def del_completed(id):
    del_completed = Todo.query.get_or_404(id)

    try:
        db.session.delete(del_completed)
        db.session.commit()
        return redirect('/completed')
    except:
        return 'There was an issue deleting your completed task.'

if __name__ == '__main__':
    app.run(debug=True)
