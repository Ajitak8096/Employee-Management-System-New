from flask import Flask , render_template , request , flash , redirect , url_for , session , jsonify
from db import EMS 
import os
import datetime, time
import bcrypt 

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_APP_SECRET_KEY')
db_usr = EMS()

@app.route('/')
def home():
    if 'loggedIn' in session:
        return render_template('home.html', sessionData=session)
    else:
         flash('Login to Proceed')
         return redirect(url_for('login'))

@app.route('/login', methods=["GET","POST"])
def login():
        if 'loggedIn' not in session:
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                id=db_usr.login(username,password)
                print(id)
                if id[1]:
                    if id[0] != []:
                        session['loggedIn'] = True 
                        session['username'] = username
                        session['id'] = id[0][0][0]
                        flash('Logged In!')
                        return redirect(url_for('home'))
                    else:
                        flash('Not Found!')
                else:
                    flash(id[0])
                        
            return render_template('login.html')
        else:
            flash('Already Logged In!')
            return redirect(url_for('home'))

@app.route('/view' , methods=['GET','POST'])
def view():
    if 'loggedIn' in session:
        if request.method == 'POST':
            empid = request.form['empid']
            data = db_usr.view(empid)
            if data[1]:
                if data[0] != []:
                    return render_template('view.html', data=data[0] )
                else:
                    flash('Not Found!')
            else:
                flash(data[0])

        return render_template('view.html')
    else:
        flash('Login to Proceed')
        return redirect(url_for('login'))
    

@app.route('/add' , methods=['GET','POST'])
def add():
    if 'loggedIn' in session:
        if request.method == 'POST':
            empid = request.form['empid']
            name = request.form['name']
            salary = float(request.form['salary'])
            state = request.form['state']
            education = request.form['education']
            pid = int(request.form['pid'])
            uniqueid = request.form['uniqueid']
            data = db_usr.add(empid,name,salary,state,education,pid,uniqueid)
            if data[1]:
                if data[0] == True:
                    flash(f'Succesfully Added {name}')
                else:
                    flash('Failed to Add')
            else:
                flash(data[0])

        return render_template('add.html')
    else:
        flash('Login to Proceed')
        return redirect(url_for('login'))
    
@app.route('/delete', methods=['GET','POST'])
def delete():
    if 'loggedIn' in session:
        if request.method == 'POST':
            empid = request.form['empid']
            data = db_usr.delete(empid)
            if data[1]:
                if data[0] == True:
                    flash(f'Succesfully Deleted {empid}')
                else:
                    flash('Failed to Delete')
            else:
                flash(data[0])

        return render_template('delete.html')
    else:
        flash('Login to Proceed')
        return redirect(url_for('login'))

@app.route('/top', methods=['GET'])
def top():
    if 'loggedIn' in session:
        data=db_usr.top()
        return render_template('top.html',data=data[0])
    else:
        flash('Login to Proceed')
        return redirect(url_for('login'))
    
@app.route('/all', methods=['GET'])
def all():
    if 'loggedIn' in session:
        data=db_usr.all()
        return render_template('all.html',data=data[0])
    else:
        flash('Login to Proceed')
        return redirect(url_for('login'))
    
@app.route('/dis', methods=['GET'])
def dis():
    if 'loggedIn' in session:
        data=db_usr.dis()
        return render_template('dis.html',data=data[0])
    else:
        flash('Login to Proceed')
        return redirect(url_for('login'))

@app.route('/update' , methods=['GET','POST'])
def update():
    if 'loggedIn' in session:
        if request.method == 'POST':
            if 'load' in request.form:
                #LOAD DATA
                empid = request.form['empid']
                data = db_usr.view(empid)
                if data[1]:
                    if data[0] != []:
                        return render_template('update.html', update=list(data[0][0]) )
                    else:
                        flash('Not Found!')
                else:
                    flash(data[0])


            elif 'update' in request.form:
                #UPDATE 
                empid = request.form['empid']
                name = request.form['name']
                salary = request.form['salary']
                state = request.form['state']
                education = request.form['education']
                pid = request.form['pid']
                data = db_usr.update(empid, ['name','salary','state','education','pid'] , [name,salary,state,education,pid])
                
                if data[1]:
                    if data[0] == True:
                        flash('Updated Succesfully')
                    else:
                        flash('Something Went Wrong')
                else:
                    flash(data[0])

        return render_template('update.html')
    else:
        flash('Login to Proceed')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    flash('Logged Out!')
    session.clear()
    return redirect(url_for('login'))

app.run(host='0.0.0.0',port=80,debug=True)