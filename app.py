import datetime
import os

from flask import Flask, render_template, redirect, url_for, flash
from forms import ItemForm
from models import Items
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

#get and post: default is only get, post is when browser submits data to form
@app.route("/", methods=('GET', 'POST'))
def add_item():
	form = ItemForm()
	if form.validate_on_submit():
		item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())
		db_session.add(item)
		db_session.commit()
		return redirect(url_for('success'))
	return render_template('index.html', form=form)

@app.route("/success")
def success():
	results = []

	qry = db_session.query(Items)
	results = qry.all()

#	print("------ Start ------")
#	for i in results:
#		print (i.name)
#	print("------ End ------")
#	
	current_itr = len(results)-1
	name_added = results[current_itr].name
	quant_added = str(results[current_itr].quantity)

	success_string = "Success! You have added "+quant_added+" of "+name_added

	return success_string


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5001)
