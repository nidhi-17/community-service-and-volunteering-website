from flask import Flask
from flask import render_template, jsonify, request, redirect, url_for, send_file, session, make_response,flash
from flask_session import Session
import mysql.connector
import json
from werkzeug.security import check_password_hash, generate_password_hash
from addPost import add_text, details


#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["MP_db"]
# mycol = mydb["Volunteer"]


pointer = int(102)
track = int(601)
k = int(7)
c = int(2)

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Nidhi@179",
  database="mydb"
)



import os
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#app.debug = True
Session(app)



@app.route('/test',methods=["GET","POST"])
def tt():
    myresult = None
    pk = ''
    if request.method == 'POST':
        pk = request.get_data().decode('utf-8')
        mycursor = db.cursor()

        mycursor.execute("SELECT Img FROM details")

        myresult = mycursor.fetchall()
        print(myresult)
        ls = []
        for i in myresult:
            ls.append(str(i[0].decode('utf-8')))

        print(ls)
        return jsonify(ls)
        #return  send_file('C:/Users/sanja/OneDrive/Desktop/lala.jpg', mimetype='image/jpg')

    else :
        print("heloooooooo elsee")
        return make_response('failure')

@app.route('/', methods=["GET", "POST"])
def a():
    return render_template("main.html")

@app.route('/Login',methods=["GET", "POST"])
def b():
    return render_template("login.html",data={'status':True})

@app.route('/logout',methods=["GET", "POST"])
def log():
    print(session['name'])
    session['name'] = None
    return render_template("login.html")

@app.route('/Admin', methods=["GET", "POST"])
def admin():
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM mydb.complaint")
    e = mycursor.fetchall()
    mycursor.execute("SELECT ngo_name, ngo_loc, ngo_email, ngo_phone, ngo_certi FROM mydb.ngo")
    n = mycursor.fetchall()
    mycursor.execute("SELECT Fname, Lname, Email, Phone, Address FROM mydb.volunteer")
    n1 = mycursor.fetchall()
    return render_template("Admin.html", data = e, ngo = n, vol=n1)

@app.route('/ret',methods=["GET", "POST"])
def ret():
    dat = {}
    if request.method == 'POST':
        pk = request.get_data().decode('utf-8')
        pk = str(pk)
        pk = pk.replace("&", " ")
        pk = pk.replace("%40", "@")
        pk = pk.replace("=", " ")
        pk = list(pk.split(" "))
        it = iter(pk)
        pk = dict(zip(it, it))
        print("pk",pk)
        if pk.get('e') == "Admin" :
            #return render_template('Admin.html', data="Admin")
            return jsonify(int(1))
        elif pk.get('e').startswith('@') :
            mycursor = db.cursor()
            name = pk.get('e')
            name = name.replace("@","")
            print(name)
            mycursor.execute("SELECT ngo_pass FROM mydb.ngo WHERE ngo_name = %s", (name,))
            da = mycursor.fetchone()
            test = generate_password_hash(pk.get('p'))
            print(test)
            print(check_password_hash(da[0], pk.get('p')))
            if  test and check_password_hash(da[0], pk.get('p')):
                session["name"] = name
                print(session['name'])
                #return render_template('test.html')
                return jsonify(int(2))
            else :
                return jsonify(int(8))
        else :
            mycursor = db.cursor()
            mycursor.execute("SELECT v_pass FROM mydb.volunteer WHERE Email = %s", (pk.get('e'),))
            da = mycursor.fetchone()
            test = generate_password_hash(pk.get('p'))
            print(test)
            print(check_password_hash(da[0], pk.get('p')))
            if  test and check_password_hash(da[0], pk.get('p')):
                session["name"] = pk.get('e')
                print(session['name'])
                print("apple")
                #return render_template('user.html', data=session["name"])
                return jsonify(int(3))
            else :
                return jsonify(int(8))


@app.route('/Insert',methods=["GET", "POST"])
def d():
    global pointer
    global track
    dat = {}
    if request.method == 'POST':
        pk = request.get_data().decode('utf-8')
        pk = str(pk)
        pk = pk.replace("&", " ")
        pk = pk.replace("%40", "@")
        pk = pk.replace("=", " ")
        pk = list(pk.split(" "))
        it = iter(pk)
        pk = dict(zip(it, it))
        print(pk)


    if pk.get('id') == 'u' :
        global pointer
        mycursor = db.cursor()
        print(pk)
        add = pk.get('address')
        add = add.replace("+", " ")
        add = add.replace("%2C",",")
        sql = "INSERT INTO mydb.volunteer (idVolunteer, Fname, Lname, Email, Phone, Address, Gender, DOB, Age, Admin_ID, v_pass) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s,%s)"
        val = (pointer,pk.get('Fname'), pk.get('Lname'), pk.get('email'),pk.get('pno'),add,pk.get('gender'),pk.get('date'), pk.get('age'),1001,generate_password_hash(pk.get('pass')) )
        mycursor.execute(sql, val)
        db.commit()
        pointer = pointer + 1

        print(mycursor.rowcount, "record inserted.")

        return redirect(url_for('b'))
    else :
        global track
        mycursor = db.cursor()
        print(pk)
        add = pk.get('Nloc')
        add = add.replace("+", " ")
        add = add.replace("%2C",",")
        des = pk.get('Nd')
        des = des.replace("+", " ")
        des = des.replace("%2C",",")
        cert = pk.get('Ncert')
        cert = cert.replace("%2F", "/")
        print(cert)
        sql = "INSERT INTO mydb.ngo (idNGO, ngo_name, ngo_loc, ngo_email, ngo_phone, ngo_descrip, ngo_certi, ngo_pass, AdminID) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)"
        val = (track, pk.get('Nname'), add, pk.get('Ne'),pk.get('Nphone'),des,cert, generate_password_hash(pk.get('Npass')),1001)
        mycursor.execute(sql, val)
        db.commit()
        track = track + 1
        print(mycursor.rowcount, "record inserted.")
        return redirect(url_for('b'))



@app.route('/Register',methods=["GET", "POST"])
def c():
    return render_template("register.html")


@app.route('/rem',methods=["GET", "POST"])
def remove():
    data = request.get_data().decode('utf-8')
    data = data.replace("="," ")
    data = data.replace("+", " ")
    data = list(data.split(" "))
    print(data[0])
    mycursor = db.cursor()
    mycursor.execute("DELETE FROM mydb.ngo WHERE ngo_name = %s",(data[1],))
    db.commit()
    return redirect(url_for('admin'))


@app.route('/ruser',methods=["GET", "POST"])
def ruse():
    if request.method == "POST" :
        data = request.get_data().decode('utf-8')
        data = data.replace("="," ")
        data = data.replace("+", " ")
        data = list(data.split(" "))
        print(data[1])
        mycursor = db.cursor()
        mycursor.execute("DELETE FROM mydb.volunteer WHERE Fname = %s",(data[1],))
        db.commit()
        return redirect(url_for('admin'))




@app.route('/User',methods=["GET", "POST"])
def user1():
    mycursor = db.cursor()
    email = session["name"]
    mycursor.execute("SELECT idVolunteer from mydb.volunteer WHERE Email = %s",(email,))
    here = mycursor.fetchone()

    mycursor.execute("SELECT Fname, Lname, Email, Phone, Address FROM mydb.volunteer  WHERE idVolunteer =%s",(here[0],))
    info1 = mycursor.fetchall()
    
    mycursor.execute("SELECT e_name,e_loc,e_date,e_time FROM event WHERE volID = %s",(here[0],))
    e = mycursor.fetchall()

    mycursor.execute("SELECT e_name,e_loc,e_date,e_time, e_descrip, e_img FROM event")
    upevents = mycursor.fetchall()
    return render_template("user.html", data=session["name"], info=list(info1), events = e, upevents = upevents)

@app.route('/ngo',methods=["GET", "POST"])
def ngo1():
    mycursor = db.cursor()
    name = session["name"]
    name = name.replace("@", "")
    mycursor.execute("SELECT * FROM event")
    data = mycursor.fetchall()
    return render_template('ngo.html', data=data, obj = name)

@app.route("/add_post", methods=["POST", "GET"])
def AddText():
    global k
    mycursor = db.cursor()
    ngo = session["name"]
    ngo = ngo.replace("@","")
    mycursor.execute("SELECT idNGO from mydb.ngo WHERE ngo_name = %s",(ngo,))
    id = mycursor.fetchone()
    Ename = request.form["e_name"]
    Edesp = request.form["e_descrip"]
    Edate = request.form["e_date"]
    Etime = request.form["e_time"]
    Eloc = request.form["e_loc"]
    Eimg = request.form["e_image"]
    mycursor.execute("INSERT INTO event(idEvent,e_name,e_loc,e_date,e_time,e_descrip,e_img,NgoId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (k,Ename,Eloc,Edate,Etime,Edesp,Eimg,id[0]))
    k = k + 1
    db.commit()
    return redirect(url_for('ngo1'))

@app.route("/delete_post",methods=['GET','POST'])
def DelText():
    mycursor = db.cursor()
    my_id  = request.form.getlist('options')
    delstamt='delete from event WHERE idEvent = %s'
    mycursor.execute(delstamt,my_id)
    db.commit()

    return redirect(url_for('ngo1'))


@app.route('/about',methods=["GET", "POST"])
def aboutus():
    return render_template("about.html")


@app.route("/com", methods=["POST", "GET"])
def com1():
    if request.method == "POST":
        desp = request.form["c_descrip"]
        date = request.form["c_date"]
        email = session["name"]
        mycursor = db.cursor()
        mycursor.execute("SELECT idVolunteer from mydb.volunteer WHERE Email = %s",(email,))
        here = mycursor.fetchone()
        print(here[0])
        print(desp)
        print(date)
        details(desp,date,here[0])
        return redirect(url_for('user1'))


@app.route("/signup",methods=['GET','POST'])
def su():
    mycursor = db.cursor()
    pk = request.get_data().decode('utf-8')
    pk = str(pk)
    pk = pk.replace("%3A",":")
    pk = pk.replace("&", " ")
    pk = pk.replace("%40", "@")
    pk = pk.replace("=", " ")
    pk = list(pk.split(" "))
    print(pk)
    it = iter(pk)
    pk = dict(zip(it, it))
    print(pk)
    name = pk.get('n').replace("+"," ")
    time = pk.get('t').replace("+"," ")
    em = session["name"]
    mycursor.execute("SELECT idVolunteer FROM mydb.volunteer WHERE Email = %s",(em,))
    id = mycursor.fetchone()
    mycursor.execute("SELECT idEvent FROM mydb.event ORDER BY  idEvent DESC LIMIT 1")
    var = mycursor.fetchone()
    var = var[0]
    var = var + 1
    mycursor.execute("INSERT INTO event(idEvent,e_name,e_loc,e_date,e_time,e_descrip,e_img,volID,NgoId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (var,name,pk.get('l'),pk.get('d'),time,pk.get('dd'),pk.get('i'),101,501))
    db.commit()
    mycursor.execute("SELECT Fname, Lname, Email, Phone, Address FROM mydb.volunteer")
    info1 = mycursor.fetchall()
    email = session["name"]
    mycursor.execute("SELECT idVolunteer from mydb.volunteer WHERE Email = %s",(email,))
    here = mycursor.fetchone()
    mycursor.execute("SELECT e_name,e_loc,e_date,e_time FROM event WHERE volID = %s",(here[0],))
    e = mycursor.fetchall()
    mycursor.execute("SELECT e_name,e_loc,e_date,e_time, e_descrip, e_img FROM event WHERE volID IS NULL")
    upevents = mycursor.fetchall()
    data = {"info" : info1, "events" : e, "upevents" : upevents}
    data = json.dumps(data)
    data = json.loads(data)
    return jsonify(data=data)

@app.route("/explore",methods=['GET','POST'])
def e():
    mycursor = db.cursor()
    mycursor.execute("SELECT e_name,e_loc,e_date,e_time, e_descrip, e_img FROM event")
    upevents = mycursor.fetchall()
    return render_template("explore.html", upevents=upevents)


if __name__ == "__main__" :
    app.run(debug=True)
