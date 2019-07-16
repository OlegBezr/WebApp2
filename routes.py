from flask import Flask, render_template, request, redirect, url_for
from flask_heroku import Heroku
from forms import UsersForm
from models import db, User

app = Flask(__name__)
heroku = Heroku(app)

db.init_app(app)

app.secret_key = "​e14a-key​"

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
	form = UsersForm()
	if request.method == 'GET':
		return render_template('add_user.html', form=form)
	else:
		if form.validate_on_submit():
			first_name = request.form['first_name']
			age = request.form['age']
			new_user = User(first_name=first_name, age=age)
			db.session.add(new_user)
			db.session.commit()
			return redirect(url_for('add_user'))

@app.route('/view-users')
def view_users():
	form = UsersForm()
	users = User.query.all()
	if request.method == 'GET':
		return render_template('view_users.html', users=users, form = form)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
	db.session.delete(User.query.get(user_id))
	db.session.commit()
	return redirect(url_for('view_users'))

@app.route('/update-user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
	form2 = UsersForm()
	user = User.query.get(user_id)
	if request.method == 'GET':
		return render_template('edit_user.html', form=form2, user=user)
	else:
		if form.validate_on_submit():
			first_name = request.form['first_name']
			age = request.form['age']
			db.session.delete(User.query.get(user_id))
			db.session.commit()
			return redirect(url_for('view_users'))

if __name__ == "__main__":
	app.run(debug=True)