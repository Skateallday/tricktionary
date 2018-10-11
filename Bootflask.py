from flask import Flask, flash, render_template, request
import json
with open('static/skaters.json') as f:
	data = json.load(f)
	
app = Flask(__name__)

@app.route('/')
def root():
	for skater in data['skaters']:
		skater=skater
	return render_template("Assignment.html",  skater=skater)

@app.route('/', methods=['POST','GET'])
def my_form_post():
	if request.method == 'POST':
		print request.form
		search = request.form['search']
		
	return render_template("Search.html", search=search)

@app.route('/about/')
def about():
	return render_template("about.html")

@app.route('/home/')
def home():
	for skater in data['skaters']:
		skater=skater
	
	return render_template("Assignment.html", skater=skater)

@app.route('/contact/')
def contact():
	return render_template("contact.html")


@app.route('/Search/',  methods=['GET', 'POST'])
def search():

	return render_template("Search.html", search=search)
	
if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
