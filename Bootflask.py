from flask import Flask, flash, render_template, request, url_for
import json

data=[]	
with open('static/skaters.json') as f:
	data = json.load(f)
	f.close()


app = Flask(__name__)

@app.route('/')
def root():
	start ='<img src="'
	url = url_for('static', filename='antwuan.png')
	end = '">'
	return start+url+end, 200
	#return render_template("Assignment.html",  skater=data)

@app.route('/Search/', methods=['POST','GET'])
def my_form_post():
	
		if request.method == 'POST':
			print request.form
			search = request.form['search_option']
			for key, value in data.items():
				if search in key:
					print("TEST")
				else:
					print("This is not in our files")
	
		return render_template("Search.html", search=search, skater=data)


@app.route('/about/')
def about():
	return render_template("about.html")

@app.route('/home/')
def home():
	
	return render_template("Assignment.html", skater=data) 

@app.route('/contact/')
def contact():
	return render_template("contact.html")

@app.route('/results/<string:stat>')
def results(stat):
	for skater in data['skaters']:
		for v in data:
			if stat in v:
				return skater 
	return render_template("results.html", skater=skater,  stat=stat)

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
