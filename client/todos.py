from flask import Blueprint,render_template,request,redirect
from flask_login import login_required,current_user

from . import db
from .models import Todo

todos = Blueprint('todos',__name__)

@todos.route('/todos',methods=['GET','POST'])
@login_required
def todo():
    if request.method=='POST':
        todo = Todo(title=request.form['title'],desc=request.form['desc'],user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('todos.html',allTodo=allTodo,user=current_user)

@todos.route('/todo_delete/<int:id>')
@login_required
def todo_delete(id):
    todo = Todo.query.filter_by(sno=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todos')

@todos.route('/todo_edit/<int:id>',methods=['GET','POST'])
@login_required
def todo_edit(id):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo.query.filter_by(sno=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/todos')
    else:
        todo = Todo.query.filter_by(sno=id).first()
        return render_template('edit_todos.html',todo=todo,user=current_user)
