import mysql.connector
#database connection
mydb1 = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Nidhi17",
  database="mpdb"
)
#inserting data to db
see = int(4)
c = int(1)

def add_text(Ename,Edesp,Edate,Etime,Eloc,Eimg):
    global see
    cursor = mydb1.cursor()
    cursor.execute("INSERT INTO event(idEvent,e_name,e_loc,e_date,e_time,e_descrip,e_img,volID,NgoId) VALUES (%s,%s,%s,%s,%s,%s,%s,100,500)", (increment(see),Ename,Eloc,Edate,Etime,Edesp,Eimg))
    mydb1.commit()

def increment(see):
    see += 1
    return see

def  details(d,date,id):
    global c
    cursor = mydb1.cursor()
    cursor.execute("INSERT INTO mpdb.complaints (cid, C_Descp, CDate, vid) VALUES (%s,%s,%s,%s)",(c,d,date,id))
    c = c + 1
    mydb1.commit()
