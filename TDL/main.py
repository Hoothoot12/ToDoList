from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///lists-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    date = db.Column(db.String(120), unique=False, nullable=False)
    time = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        # this is where you define what will show when you call function
        return '%r' % self.title

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html',lists=db.session.query(List).all(),number=len(db.session.query(List).all()))

@app.route("/add", methods=['GET','POST'])
def add():
    if request.method=='POST':
      list=List(title=request.form['name'],date=request.form['date'],time=request.form['time'])
      db.session.add(list)
      db.session.commit()
      return redirect(url_for('home'))
    return render_template('add.html')

@app.route("/edit", methods=['GET','POST'])
def edit():
    list_id = request.args.get('id')
    list_to_update = List.query.get(list_id)
    if request.method=='POST':
        list_to_update.date = request.form['date']
        list_to_update.time =request.form['time']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',list=list_to_update)

@app.route("/delete")
def delete():
      list_id=request.args.get('id')
      list_to_delete = List.query.get(list_id)
      db.session.delete(list_to_delete)
      db.session.commit()
      return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
