from flask import Flask, flash, render_template, request
import json

with open('static/skaters.json') as f:
	data = json.load(f)
	print(json.dumps(data, indent=2))

	
app = Flask(__name__)

@app.route('/')
def root():
	for skater in data['skaters']:
		print(skater) 
	return render_template("Assignment.html",  skater=skater)

@app.route('/Search/', methods=['POST','GET'])
def my_form_post():
	if request.method == 'POST':
		print request.form
		search = request.form['search']
	for skater in data['skaters']:
		if search in skater:
			return skater
		return None	
	print my_form_post(skaters, search)	
		
	return render_template("Search.html", search=search, skater=skater)


@app.route('/about/')
def about():
	return render_template("about.html")

@app.route('/home/')
def home():
	for skater in data['skaters']:
		print(skater)
	
	return render_template("Assignment.html", skater=skater)

@app.route('/contact/')
def contact():
	return render_template("contact.html")

@app.route('/results/<string:stat>')
def results(stat):
	#for skater in data['skaters']:
		#print(skater)
	return render_template("results.html",  stat=stat)

@app.route('/upload/', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		print request.form
		upload = request.form['upload']
		with open('static/newSkaters.json', 'w') as G:
			json.dump(request.form, G)
		return render_template("upload.html", upload=upload)
if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
