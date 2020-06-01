from flask import Flask, render_template, url_for, flash, redirect, request


import os
import cx_Oracle


# Configure db
db_user = os.environ.get('DBAAS_USER_NAME', 'system')
db_password = os.environ.get('DBAAS_USER_PASSWORD', 'oracle')
db_connect = os.environ.get('DBAAS_DEFAULT_CONNECT_DESCRIPTOR', "localhost:1521/orcl")

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        'database': 'DB:orcl',
        'table': 'TableName:MyUsers',
        'content': 'Employess Details',
        'date_created': 'may 29, 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == "POST":
        details = request.form
        ID = details['id']
        firstName = details['fname']
        lastName = details['lname']
        connection = cx_Oracle.connect(db_user, db_password, db_connect)
        cur = connection.cursor()
        cur.execute('INSERT INTO MyUsers (ID,firstName,lastName) VALUES (\'' + str(ID) + '\',\'' + str(firstName) + '\',\'' + str(lastName)+'\')')
        connection.commit()
        cur.close()
        return redirect("/table")
    return render_template('index.html')


@app.route("/table")
def table():
    connection = cx_Oracle.connect(db_user, db_password, db_connect)
    cur = connection.cursor()
    cur.execute("SELECT * FROM MyUsers")
    details = cur.fetchall()
    return render_template('users.html', details=details,title='table')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == "POST":
        details = request.form
        ID1 = details['id']
        connection = cx_Oracle.connect(db_user, db_password, db_connect)
        cur = connection.cursor()
        sql = 'DELETE FROM MyUsers where ID= '+ID1
        cur.execute(sql)
        connection.commit()
        cur.close()
        return redirect("/table")
    return render_template('index1.html')




@app.route('/alter', methods=['GET', 'POST'])
def alter():
    if request.method == "POST":
        details = request.form
        ID1 = details['id']
        firstName = details['fname']
        lastName = details['lname']
        connection = cx_Oracle.connect(db_user, db_password, db_connect)
        cur = connection.cursor()
        sql = "UPDATE MyUsers SET firstname = '" + str(firstName) + "' , lastName= '" + str(lastName)  +"' WHERE ID = " +ID1
        cur.execute(sql)
        connection.commit()
        cur.close()
        return redirect("/table")
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)