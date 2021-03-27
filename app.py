from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    desc=db.Column(db.String(250),nullable=False)
    date=db.Column(db.String(25),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        date=request.form['date']
        todo=Todo(title=title,desc=desc,date=date)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)
    #return 'Hello, World!'

#we can add multiple endpoints like this
@app.route('/show')
def  show():
    allTodo=Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/delete/<int:sno>')
def  delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET','POST'])
def  update(sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        date=request.form['date']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        todo.date=date
        db.session.add(todo)
        db.session.commit() 
        return redirect("/")

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
if __name__ =="__main__":
    app.run(debug=True,port=8000)#we can cange the prt name like this if you dont want to change the port name you no need to writ port=800
