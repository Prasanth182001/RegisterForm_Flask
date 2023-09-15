from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL

app=Flask(__name__)
app.secret_key="ac12"

# mysql connection

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="Prasanth@182001"
app.config["MYSQL_DB"]="flask02"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/addpage",methods=["GET","POST"])
def add():
    if request.method == 'POST' and request.form["name_"] and request.form["email_"] and request.form["pass_"]:
        try:
           n = request.form["name_"]
           e = request.form["email_"]
           p = request.form["pass_"]

           con=mysql.connection.cursor()
           con.execute("insert into ff01 (NAME,EMAIL,PASSWORD) value (%s,%s,%s)",(n,e,p))
           mysql.connection.commit()
           con.close()
           flash("Record added successfully")
        except:
           flash("Error in insert operation")
        finally:
           return redirect(url_for("index"))
    return render_template('sign-up.html')


@app.route("/loginpage",methods=["GET","POST"])
def login():
    if request.method == "POST" and request.form["_name"] and request.form["_pass"]:
          un=request.form["_name"]
          pa=request.form["_pass"]
          con=mysql.connection.cursor()
          con.execute("select * from ff01 where NAME=%s and PASSWORD=%s",(un,pa))
          result=con.fetchone()
          if result:
              session['id'] = result['NAME']
              session['pd'] = result['PASSWORD']
              return redirect(url_for("home"))
          else:
              flash('Incorrect username / password !')

    return render_template("index.html")

@app.route("/homepage")
def home():
    msg = 'Logged in successfully !'
    return render_template("home.html",msg=msg)

@app.route("/logout")
def logout():
    session.pop('id')
    session.pop('pd')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)