from flask import Flask,render_template,redirect,request,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ok'
app.config['MYSQL_DB'] = 'flask_app'

mysql = MySQL(app)

@app.context_processor
def inject_built_in_function():
    return dict(enumerate=enumerate,len=len)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("select * from students")
    students = cur.fetchall()
    return render_template('students/index.html',students=students)

@app.route('/insert',methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name,email,phone) VALUES (%s, %s,%s)",(name,email,phone))

        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/delete/<string:id>',methods=['GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("delete from students where id=%s",(id,))
    mysql.connection.commit()
    return redirect(url_for('index'))


@app.route('/update/<string:id>',methods=['POST'])
def update(id):
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("update students set name = %s,email = %s,phone = %s where id=%s",(name,email,phone,id))
        mysql.connection.commit()
        return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)