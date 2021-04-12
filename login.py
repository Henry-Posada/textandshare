# Import statements
from flask import Flask,render_template,request,redirect,url_for
from flaskext.mysql import MySQL
import MYSQLdb

# mysql = MySQL()
# Container for app
app = Flask(_name_)

# Possible other way to connect
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root_password'
# app.config['MYSQL_DATABASE_DB'] = 'textAndShareDB'
# app.config['MYSQL_DATABASE_HOST'] = '69.121.70.211:3306'
 
# Connection to MySQL database
conn = MySQLdb.connect(host="69.121.70.211:3306",user="root",password="root_password",db="textAndShareDB") 

# First page
@app.route("/")
def index():
	return render_template("signup.html", title="signUp")

# Sign up method
@app.route("/signUp",methods=["POST"])
def signUp():
	username = str(request.form["user"])
	password = str(request.form["password"])
	email = str(request.form["email"])
	
	# cursor = mysql.connect().cursor()
	cursor = conn.cursor()
	
	cursor.execute("INSERT INTO users (name,password,email)VALUES(%s,%s,%s)",(username,password,email))

	conn.commit()

	return redirect(url_for("login"))

# Log in method	
@app.route("/login")
def login():
	return render_template("login.html",title="data")

# Checks if inputted user credentials are valid
@app.route("/checkUser",methods=["POST"])
def check():
	username = str(request.form["user"])
	password = str(request.form["password"])
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM users WHERE username=' "+ username + "' AND password =' " + password + " ' ")

	user = cursor.fetchone()
	
	if user is None:
		return "Username or password is incorrect"
	else:
		return redirect(url_for("index"))

# Takes you to main page
@app.route("/index")
def index():
	return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True)