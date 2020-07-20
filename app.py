from flask import Flask, redirect, flash, render_template, request, url_for, session, g
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from models import whoIs, sessionCheck
from forms.forms import search, loginForm, contactForm, registration, recordSelection
from forms.addRecords import newSkater, newSkateboards, newShoes, newTricks, newTrucks, newWheels
from werkzeug.utils import secure_filename

from flask_wtf.csrf import CSRFProtect, CSRFError
import os
import json
import random
import sqlite3


data=[]

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
SECRET_KEY = os.urandom(32)
UPLOAD_FOLDER = 'static/images/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['jpg'])
app.config['SECRET_KEY'] = SECRET_KEY

@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html") 

@app.before_request
def before_request():
        g.username = None
        if 'username' in session:
                g.username = session['username']

@app.route('/')
@app.route('/home')
def home():
	if g.username:
		return render_template("index.html", loggedIn= "yes", username=g.username)

	else:
		return render_template("index.html")


@app.route('/Search/', methods=['POST', 'GET'])
def my_form_post():
	if request.method == 'POST':
		print ("request form")
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



@app.route('/addRecord', methods=['POST', 'GET'])
def addRecord():
	if g.username:		
				return render_template("addRecord.html", loggedIn= "yes", username=g.username)
	else:
		return render_template("addRecord.html")


#####################################################################
#																	#
#  MOVE CODE BELOW INTO A NEW FILE TO MAKE PROJECT MORE MODULAR 	#
#																	#
#####################################################################


@app.route('/formTemplate/<selectForm>', methods=['POST', 'GET'])
def formTemplate(selectForm):
	if selectForm == 'newSkater':
		form = newSkater(request.form)
		table = "skaters"
		if request.method == 'POST':
			f = request.files.get('img_url')
			img_url = (form.img_url.data)
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			formData = [form.name.data, form.DOB.data, form.nationality.data, form.gender.data, form.skateboard.data, form.wheels.data, form.shoes.data, form.trucks.data, filename]
			record = '''INSERT INTO ''' + table + ''' (name, DOB, nationality, gender, skateboard, wheels, shoes, trucks, img_url) VALUES (?,?,?,?,?,?,?,?,?);'''

	elif selectForm =='newSkateboard':
		form =newSkateboards(request.form)
		table = "skateboards"
		if request.method == 'POST':
			f = request.files.get('img_url')
			img_url = (form.img_url.data)
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			formData = [form.name.data, form.est.data, form.nationality.data, filename]
			record = '''INSERT INTO ''' + table + ''' (name, est, nationality, img_url) VALUES (?,?,?,?);'''

	elif selectForm =='newWheels':
		form =newWheels(request.form)	
		table = "wheels"
		if request.method == 'POST':
			f = request.files.get('img_url')
			img_url = (form.img_url.data)
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			formData = [form.name.data, form.est.data, form.nationality.data, filename]
			record = '''INSERT INTO ''' + table + ''' (name, est, nationality, img_url) VALUES (?,?,?,?);'''


	elif selectForm =='newTricks':
		form =newTricks(request.form)
		table = "tricks"
		formData = [form.name.data, form.creator.data, form.difficulty.data,  form.youtube_url.data]
		record = '''INSERT INTO ''' + table + ''' (name, creator, difficulty, youtube_url) VALUES (?,?,?,?);'''
	
	elif selectForm =='newTrucks':
		form =newTrucks(request.form)	
		table = "trucks"
		if request.method == 'POST':
			f = request.files.get('img_url')
			img_url = (form.img_url.data)
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			formData = [form.name.data, form.est.data, form.nationality.data, filename]
			record = '''INSERT INTO ''' + table + ''' (name, est, nationality, img_url) VALUES (?,?,?,?);'''

	else:
		form =newShoes(request.form)
		table = "shoes"
		if request.method == 'POST':
			f = request.files.get('img_url')
			img_url = (form.img_url.data)
			filename = secure_filename(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			formData = [form.name.data, form.est.data, form.nationality.data, filename]
			record = '''INSERT INTO ''' + table + ''' (name, est, nationality, img_url) VALUES (?,?,?,?);'''

	if request.method == 'POST':
				conn = sqlite3.connect('library.db')                
				with conn:
						c = conn.cursor()
						try:	
								c.executemany(record, [formData])
								print("Successful!")						
						except Exception as e: print(e)
						flash(" Successfully Posted!!")

	if g.username:		
		return render_template("formTemplates/"+str(selectForm)+".html", loggedIn= "yes", username=g.username, form=form)
	else:
		return render_template("formTemplates/"+str(selectForm)+".html", form=form)				
								
								
#####################################################################
#																	#
#  						END OF SECTION								#
#																	#
#####################################################################


@app.route('/contact/', methods=['POST', 'GET'])
def contact():
	contactform = contactForm(request.form)
	if g.username:
		return render_template("contact.html", loggedIn= "yes", username=g.username, contactForm=contactform)

	else:
		return render_template("contact.html",  contactForm=contactform)

@app.route('/list/<string:category>', methods=['POST', 'GET'])
def lists(category):
	txt_url=open('static/text/' + category + '.txt') 
	content = txt_url.read()
	txt_url.close()
	if request.method == 'GET':
				conn = sqlite3.connect('library.db')                
				with conn:
						c = conn.cursor()
						try:	

								findCategory = ("SELECT * FROM " + category +" ")
								c.execute(findCategory)
								results =c.fetchall()   
								for result in results:
									print(results)
									print(result)						
						except Exception as e: print(e)

	if g.username:
		return render_template("resultsTemplates/"+str(category)+"Results.html", category=category, content=content, results=results, loggedIn= "yes", username=g.username)

	else:
		return render_template("resultsTemplates/"+str(category)+"Results.html", results=results, content=content, category=category)

@app.route('/upload/', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		print ("request.form")
		upload = request.form['upload']
		with open('static/newSkaters.json', 'w') as G:
			json.dump(request.form, G)
		return render_template("upload.html", upload=upload)

@app.route('/Login/', methods=['GET', 'POST'])
def LogIn():
		if g.username:
			return redirect('home')

		else:
			form = loginForm(request.form)       
			if request.method == 'POST':  
					conn = sqlite3.connect('library.db')                
					with conn:
							c = conn.cursor()
							try:
									find_user = ("SELECT * FROM users WHERE username = ?")
									c.execute(find_user, [(form.username.data)])
									results =c.fetchall()                        
									userResults = results[0]
									if bcrypt.check_password_hash(userResults[1],(form.password.data)):
											session['username'] = (form.username.data)
											return redirect(url_for('home'))
									else:
											flash('Either username or password was not recognised')
											return render_template('login.html', form=form)   
							except Exception as e:print(e)

							flash('Either username or password was not recognised')
							return render_template('login.html', form=form)                                 
			return render_template("login.html", form=form) 

@app.route("/logout")
def logout():        
        session['logged_in'] = True
        session.clear()
        flash("You have successfully logged out.")
        return redirect('home')


@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def SignUp():
        if g.username:
                return redirect('home')
        else:
                registerForm = registration(request.form) 
                if request.method == 'POST':
                        pw_hash =bcrypt.generate_password_hash(registerForm.password.data)
                        newEntry = [((registerForm.username.data), pw_hash, (registerForm.emailAddress.data), 'No')]

                        conn =sqlite3.connect('library.db')
                        print ("Opened database successfully")
                        with conn:
                                c =conn.cursor()
                                try:
                                        signupSQL = '''INSERT INTO users (username, password, email, admin) VALUES(?,?,?,?)'''
                                        c.executemany(signupSQL, newEntry)
                                        print ("Insert correctly")
                                except:
                                        flash("This is already an account, please log in with those details or change details.")
                                        c.commit()
                                        return render_template("signup.html", form=registerForm)
                                flash((registerForm.username.data) + " Successfully Registered!")
                                session['logged_in'] = True
                                session['username'] = (registerForm.username.data)
                                return redirect('account')                                
                        return render_template("signup.html", form=registerForm)
                return render_template('signup.html', form=registerForm)

       
@app.route("/profile", methods=['GET', 'POST'])
def profile():      
        if g.username:
                conn =sqlite3.connect('library.db')
                print ("Opened database successfully")
                c = conn.cursor()

                c.execute('SELECT * FROM users WHERE username LIKE (?)', (g.username, ))
                results = c.fetchall()
                print(results) 
                    
                return render_template("profile.html", loggedIn="yes", username=g.username)                
                
        else:
                flash('Please Login to continue')
                return redirect('Login')
		 
@app.route("/adminPanel", methods=['GET', 'POST'])
def admin():
	if g.username:
		conn =sqlite3.connect('library.db')
		c = conn.cursor()
		c.execute('SELECT * FROM users WHERE username LIKE (?)', (g.username, ))
		admin = c.fetchall()
		for results in admin:
			print(results[3]) 
			if str(results[3]) == "Yes":
				return render_template("adminPanel.html", loggedIn= "yes", username=g.username)
			else:
				flash("You do not have admin rights to access this page")
				return redirect("home")
		flash("You do not have admin rights to access this page")
		return redirect("home")
	else:
		flash('Please log in to continue')
		return redirect('Login')

@app.route("/adminRecords", methods=['POST', 'GET'])
def adminRecords():
	form = newSkater(request.form)       
	conn = sqlite3.connect('library.db')
	print ("Library data opened")
	c = conn.cursor()
	c.execute('SELECT * from skaters')
	results = c.fetchall()
	print(results)
	for data in results:
		return render_template("adminRecords.html", loggedIn= "yes", username=g.username, form=form, data=data)
	if request.method == 'POST':
		
		enterSkater = [((form.name.data), (form.DOB.data), (form.nationality.data), (form.gender.data), (form.skateboard.data), (form.wheels.data ), (form.shoes.data), (form.trucks.data))]
		with conn:
			try:
				insertPost = '''INSERT INTO skaters (name, DOB, nationality, gender, skateboard, wheels, shoes, trucks) VALUES(?,?,?,?,?,?,?,?)'''
				c.executemany(insertPost, enterSkater)
				print ("Insert correctly")
			except Exception as e: print(e)                                                        
		flash(" Successfully Posted!!")
	
	return render_template("adminRecords.html", loggedIn= "yes", username=g.username, form=form)

@app.route("/userRecords", methods=['POST', 'GET'])
def userRecords():
	conn = sqlite3.connect('tempLibrary.db')
	c = conn.cursor()
	c.execute('SELECT * from wheels')
	results = c.fetchall()
	print(results)
	for data in results:
		return render_template("userRecords.html", loggedIn= "yes", username=g.username, results=results)
		
	return render_template("userRecords.html", loggedIn= "yes", username=g.username)

@app.route("/approve/<approveId>", methods=['POST', 'GET'])
def approve(approveId):
	connTemp = sqlite3.connect('tempLibrary.db')
	cTemp = connTemp.curor()
	conn =sqlite3.connect('library.db')
	c = conn.cursor()
	c.execute('SELECT * from wheels')
	results = c.fetchall()
	print(results)
	for data in results:
		return render_template("userRecords.html", loggedIn= "yes", username=g.username, results=results)
		
	return render_template("userRecords.html", loggedIn= "yes", username=g.username)


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
