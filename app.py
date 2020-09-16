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
UPLOAD_FOLDER = '/home/skateallday/tricktionary/static/images/uploads'
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
		search = request.form['search']
			
		for  skater in data:
		
			if search in skater:
				skater=skater[search]
				  
			else:
				return("There are no results for your search, try again.")
	
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
				conn = sqlite3.connect('tempLibrary.db')                
				with conn:
						c = conn.cursor()
						try:	
								c.executemany(record, [formData])
						except Exception as e: print(e)
						flash("Post unsuccessful, try again or please contact admin.")
						redirect("index.html")

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
	results="Skater"
	txt_url=open( os.path.join(app.root_path, 'static/text/' + category + '.txt') )
	content = txt_url.read()
	txt_url.close()
	if request.method == 'GET':
		conn = sqlite3.connect( os.path.join(app.root_path,'library.db'))
		with conn:
			c = conn.cursor()
			try:
				findCategory = ("SELECT * FROM " + category +" ")
				c.execute(findCategory)
				results =c.fetchall()
				if g.username:
					return render_template("resultsTemplates/"+str(category)+"Results.html", i=0, category=category, content=content, results=results, loggedIn= "yes", username=g.username)
				else:
					return render_template("resultsTemplates/"+str(category)+"Results.html", i=0, results=results, content=content, category=category)
			except Exception as e: print(e)
	else:
		return render_template("resultsTemplates/"+str(category)+"Results.html", i=0, results=results, content=content, category=category)



#####################################################################
#																	#
# 	 					LOG IN SECTION					 			#
#																	#
#####################################################################

@app.route('/Login/', methods=['GET', 'POST'])
def LogIn():
		if g.username:
			return redirect('home')

		else:
			form = loginForm(request.form)       
			if request.method == 'POST':  
					conn = sqlite3.connect( os.path.join(app.root_path, 'library.db') )               
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

			conn =sqlite3.connect( os.path.join(app.root_path,'library.db'))
			with conn:
					c =conn.cursor()
					try:
						signupSQL = '''INSERT INTO users (username, password, email, admin) VALUES(?,?,?,?)'''
						c.executemany(signupSQL, newEntry)
						flash((registerForm.username.data) + " Successfully Registered!")
						session['logged_in'] = True
						session['username'] = (registerForm.username.data)
						return redirect('home')     
					except:
						flash("This is already an account, please log in with those details or change details.")
						c.commit()
						return render_template("signup.html", form=registerForm)				
		return render_template("signup.html", form=registerForm)
	return render_template('signup.html', form=registerForm)

#####################################################################
#																	#
#  						END OF SECTION								#
#																	#
#####################################################################

       
@app.route("/profile", methods=['GET', 'POST'])
def profile():      
        if g.username:
                conn =sqlite3.connect( os.path.join(app.root_path,'library.db'))
                c = conn.cursor()

                c.execute('SELECT * FROM users WHERE username LIKE (?)', (g.username, ))
                results = c.fetchall()
                    
                return render_template("profile.html", loggedIn="yes", username=g.username)                
                
        else:
                flash('Please Login to continue')
                return redirect('Login')

#####################################################################
#																	#
#  						ADMIN PANEL									#
#																	#
#####################################################################
		 
@app.route("/adminPanel", methods=['GET', 'POST'])
def admin():
	if g.username:
		conn =sqlite3.connect( os.path.join(app.root_path,'library.db'))
		c = conn.cursor()
		c.execute('SELECT * FROM users WHERE username LIKE (?)', (g.username, ))
		admin = c.fetchall()
		for results in admin:
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
	
	return render_template("adminRecords.html", loggedIn= "yes", username=g.username)



@app.route('/choosenApprove/<chooseApprove>', methods=['POST', 'GET'])
def choosenApprove(chooseApprove):
	if chooseApprove == 'approveSkaters':
		table = "skaters"

	elif chooseApprove =='approveSkateboards':
		table = "skateboards"

	elif chooseApprove =='approveWheels':
		table = "wheels"

	elif chooseApprove =='approveTricks':
		table = "tricks"
	
	elif chooseApprove =='approveTrucks':
		table = "trucks"

	else:
		table = "shoes"

	if request.method == 'GET':
				conn = sqlite3.connect( os.path.join(app.root_path,'tempLibrary.db') )
				with conn:
						c = conn.cursor()
						try:	
								findApprove = ("SELECT * FROM " + table +" ")
								c.execute(findApprove)
								results =c.fetchall()   
								for result in results:
									return render_template("approvalList/"+str(chooseApprove)+".html",i=0, results=results, loggedIn= "yes", username=g.username)
				
						except Exception as e: print(e)
						flash("Not successful, try again please!")
						redirect("adminRecords.html")

	if g.username:		
		return render_template("approvalList/"+str(chooseApprove)+".html", loggedIn= "yes", username=g.username)
	else:
		flash('Please Login to continue')
		return render_template('index.html')		

@app.route("/userRecords", methods=['POST', 'GET'])
def userRecords():
	conn = sqlite3.connect( os.path.join(app.root_path,'tempLibrary.db'))
	c = conn.cursor()
	c.execute('SELECT * from wheels')
	results = c.fetchall()
	for data in results:
		return render_template("userRecords.html", loggedIn="yes", username=g.username, results=results)
		
	return render_template("userRecords.html", loggedIn="yes", username=g.username)

@app.route("/approve/<table>/<approveId>", methods=['POST', 'GET'])
def approve(table, approveId):
	if table == 'skaters':
		record = '''INSERT INTO ''' + table + ''' (name, DOB, nationality, gender, skateboard, wheels, shoes, trucks, img_url) VALUES (?,?,?,?,?,?,?,?,?);'''
	elif table =='skateboards':
		record = '''INSERT INTO ''' + table + ''' (name, est, nationality, img_url) VALUES (?,?,?,?);'''
	elif table =='wheels':
		record = '''INSERT INTO ''' + table + ''' (name, est, nationality, img_url) VALUES (?,?,?,?);'''
	elif table =='tricks':
		record = '''INSERT INTO ''' + table + ''' (name, creator, difficulty, youtube_url) VALUES (?,?,?,?);'''
	elif table =='trucks':
		record = '''INSERT INTO ''' + table + ''' (name, est, nationality, img_url) VALUES (?,?,?,?);'''
	else:
		record = '''INSERT INTO ''' + table + ''' (name, est, nationality, img_url) VALUES (?,?,?,?);'''

	connTemp = sqlite3.connect( os.path.join(app.root_path, 'tempLibrary.db'))
	cTemp = connTemp.cursor()
	try:
		cTemp.execute('SELECT * FROM '+ table +' WHERE name LIKE (?)', (approveId,))
		tempResults = cTemp.fetchall()
		for data in tempResults:
			conn = sqlite3.connect( os.path.join(app.root_path, 'library.db') )
			with conn:
				try:
					c = conn.cursor()
					c.executemany(record, [data])
					c.close()
					cTemp.execute('DELETE FROM '+ table +' WHERE name LIKE (?)', (approveId, ))	
					connTemp.commit()
					cTemp.close()
					flash("You have moved " + approveId + "  into " + table + " and removed it from the temporary database. This will now appear live on the site.")
					return redirect(url_for('adminRecords', loggedIn='yes', username=g.username))
				except Exception as e: print(e)
				flash("Did not approve record, try again!", "error" )		
				return redirect(url_for('adminRecords', loggedIn='yes', username=g.username))
	except Exception as e: print(e)
	flash("Did not approve record, try again!", "error" )		
	return redirect(url_for('adminRecords', loggedIn='yes', username=g.username))
	

@app.route("/delete/<table> <approveId>", methods=['POST', 'GET'])
def delete(table, approveId):
	connTemp = sqlite3.connect( os.path.join(app.root_path,'tempLibrary.db'))
	cTemp = connTemp.cursor()
	try:
		cTemp.execute('DELETE FROM '+ table +' WHERE name LIKE (?)', (approveId, ))	
		connTemp.commit()
		cTemp.close()
		flash("You have deleted " + approveId + " from " + table)
	except Exception as e: print(e)
	flash("Not successful, try again please!")
	return redirect(url_for('adminRecords', loggedIn='yes', username=g.username))

#####################################################################
#																	#
#  						END OF SECTION								#
#																	#
#####################################################################


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
