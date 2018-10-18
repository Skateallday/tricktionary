from flask import Flask, flash, render_template, request, url_for
import json



data=[]
	
with open('static/skaters.json') as f:
	data = json.load(f)
	f.close()


app = Flask(__name__)

@app.route('/')
def root():
	
	url1 = url_for('static', filename='eric.png')
	url2 = url_for('static', filename='leticia.png')
	url = url_for('static', filename='chris.png')

	return render_template("Assignment.html",url1=url1, url=url, url2=url2 )

@app.route('/Search/', methods=['POST','GET'])
def my_form_post():
	
	if request.method == 'POST':
		print request.form
		search = request.form['search']
			
		for  skater in data:
		
			print("Value: " + str(skater))
			if search in skater:
				skater=skater[search]
				print ("this worked")	
				  
			else:
				return("There are no results for your search, try again.")
				print ("DOES NOT WORK")
	
		return render_template("Search.html", search=search, skater=skater)


@app.route('/about/')
def about():
	return render_template("about.html")

@app.route('/home/')
def home():
	
	url1 = url_for('static', filename='eric.png')
	url2 = url_for('static', filename='leticia.png')
	url = url_for('static', filename='chris.png')

	return render_template("Assignment.html",url1=url1, url=url, url2=url2)

@app.route('/contact/')
def contact():
	return render_template("contact.html")

@app.route('/results/<string:stat>')
def results(stat):
	txt_url=open('static/' + stat + '.txt') 
	content = txt_url.read()
	txt_url.close()
	img_url = url_for('static', filename= stat+'.jpg')
	for skaters in data:
		print(skaters)
		if stat in skaters:
			skaters=skaters[stat]
			print(skaters)
		return render_template("results.html", skaters=skaters, img_url=img_url, txt_url=content,  stat=stat)

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
