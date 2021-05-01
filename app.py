from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc  = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} {self.title}"

@app.route('/todo_delete/<int:id>')
def todo_delete(id):
    todo = Todo.query.filter_by(sno=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todos')

@app.route('/todo_edit/<int:id>',methods=['GET','POST'])
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
        return render_template('edit_todos.html',todo=todo)


@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/todos',methods=['GET','POST'])
def todos():
    if request.method=='POST':
        todo = Todo(title=request.form['title'],desc=request.form['desc'])
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('todos.html',allTodo=allTodo)



@app.route('/contact')
def contact():
    return 'contact page'

@app.route('/about')
def about():
    return 'about page'

if __name__ == "__main__":
    app.run(debug=False,port=8000)