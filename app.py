
import pandas as pd
import cryptocode
from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from flask import Flask, redirect, url_for, render_template, send_file,request, session, jsonify
from flask_sqlalchemy import SQLAlchemy


from flask_admin import Admin as adm
from flask_admin.contrib.sqla import ModelView
import csv ,os ,json 

from dateTime_EGY import  get_week_number,WEEKDAY
from datetime import datetime ,date,timedelta
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
class User_admin(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    paswd = db.Column(db.String(100))
    def __init__(self,name,paswd):
        self.name = name
        self.paswd = paswd

class TAssistant(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    email =db.Column(db.String(100),unique =True ) 
    paswd = db.Column(db.String(100))
    user = db.Column(db.String(100))
    def __init__(self,name,email,paswd,user):
        self.name = name
        self.email = email
        self.paswd = paswd
        self.user = user

class SAffairs(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    paswd = db.Column(db.String(100))
    user = db.Column(db.String(100))
    def __init__(self,name,paswd,user):
        self.name = name
        self.paswd = paswd
        self.user = user
class QuizeCourse(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    TA = db.Column(db.String(100))
    course = db.Column(db.String(100))
    stu = db.Column(db.String(100))
    stuName = db.Column(db.String(100))
    week = db.Column(db.String(100))
    mark = db.Column(db.String(100))
    def __init__(self,TA,course,stu,week,mark,stuName):
        self.TA = TA
        self.course = course
        self.stu = stu
        self.week = week
        self.mark = mark
        self.stuName=stuName

class Course(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(100),unique =True)
    user = db.Column(db.String(100))
    def __init__(self,name,code,user):
        self.name = name
        self.code = code
        self.user = user

class TA_Course(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    TA = db.Column(db.String(100))
    course = db.Column(db.String(100))
    code = db.Column(db.String(100))
    stu_afferis = db.Column(db.String(100))
    def __init__(self,TA,course,code,stu_afferis):
        self.TA = TA
        self.course = course
        self.code = code
        self.stu_afferis = stu_afferis
class STU(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(100),unique =True)
    
    def __init__(self,name,code):
        self.name = name
        self.code = code
class STURegis(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(100)) 
    Course = db.Column(db.String(100))
    
    def __init__(self,name,code,Course):
        self.name = name
        self.code = code
        self.Course = Course
class TA_AttendanceC(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    Email = db.Column(db.String(100))
    Name = db.Column(db.String(100))
    Course = db.Column(db.String(100))
    Date = db.Column(db.String(100)) 
    week = db.Column(db.String(100)) 
    
    def __init__(self,Email,Name,Course,Date,week):
        self.Email = Email
        self.Name = Name
        self.Course = Course
        self.Date = Date
        self.week = week


class Attendace(db.Model):
    _id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    Date = db.Column(db.String(100))
    Time = db.Column(db.String(100))
    Week = db.Column(db.String(100))
    Course = db.Column(db.String(100))
    TA = db.Column(db.String(100))
    stuCode = db.Column(db.String(100))
    MAC = db.Column(db.String(100))   
    
    def __init__(self,Date,Time,Week,Course,TA,stuCode,MAC):
        self.Date = Date
        self.Time = Time
        self.Week = Week
        self.Course = Course
        self.TA = TA
        self.stuCode = stuCode
        self.MAC = MAC        

app.secret_key = "SecretSecret"
app.permanent_session_lifetime = timedelta(minutes=31)
adminp = adm(app)

class MyModelView(ModelView):
    def is_accessible(self):
        if "admin" in session:
            return True
        else:
            return False    
       

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('appx', next=request.url))


adminp.add_view(MyModelView(User_admin,db.session))
adminp.add_view(MyModelView(TAssistant,db.session))
adminp.add_view(MyModelView(SAffairs,db.session))
adminp.add_view(MyModelView(Course,db.session))
@app.route('/app')  
def appx():
    return render_template("Addmin.html")

@app.route('/appLogin',methods=["POST"])  
def appLogin():
    if request.method == 'POST': 
         ID = request.form["ID"]
         paswd = request.form["Password"]
         Admin = User_admin.query.filter_by(name=ID,paswd =paswd).first()
         if Admin :
             session.permanent =True
             session["admin"] = str(Admin.name)
             
             return redirect("/admin")
         else:
             return redirect("/app")
          
    else:
        return "Not allowed"
  

@app.route('/out')  
def out():
    session.pop("admin",None)

    return redirect(url_for('appx', next=request.url))
@app.route('/logout')  
def logout():
    session.pop("TA",None)
    session.pop("stu_affairs",None)
    
    return redirect('/')

@app.route('/stuAffiers/<x>/<y>/<a>/<b>')  
def stu_AFFIERS(x,y,a,b):
    if  str(x) == session["stu_affairs"]:
        if str(y) == 'view':
            data=TA_Course.query.all()
            x=len(data)
           
            
            return render_template("view_stuAff.html" ,x=x,msg='', usr =session["stu_affairs"] , data=data)
        elif str(y) == 'viewSTU':
            data=STU.query.all()
            x=len(data)
           
           
            return render_template("view_stu.html" ,x=x,msg='', usr =session["stu_affairs"] , data=data)
        elif str(y) == 'delete':
           
            
            d=TA_Course.query.filter_by(TA=a,course=b).first()
            db.session.delete(d)
            db.session.commit()
            data=TA_Course.query.all()
            x=len(data)
            return render_template("view_stuAff.html" ,x=x,msg='deleted', usr =session["stu_affairs"] , data=data)
        elif str(y) == 'deleteSTU':
           
            
            d=STU.query.filter_by(name=a,code=b).first()
            db.session.delete(d)
            db.session.commit()
            data=STU.query.all()
            x=len(data)
            return render_template("view_stu.html" ,x=x,msg='deleted', usr =session["stu_affairs"] , data=data)
        
        else:
            return "not alowed"
    else:
        return "not alowed"


@app.route('/')  
def index():
    return render_template("login.html")


@app.route('/Login',methods=["POST"])  
def Login():
    if request.method == 'POST': 
         ID = request.form["ID"]
         paswrd = request.form["Password"]
         type =  request.form["typex"]
         
         if type == 'stuA':
            stu_affairs = SAffairs.query.filter_by(name=ID,paswd=paswrd).first()
            if stu_affairs:
                session.permanent =True
                session['stu_affairs'] = str(stu_affairs.name)
                
                return redirect("/studentAffairs")

            else:
                return render_template("login.html",ms="user not found")
         elif type == 'TA':
            TA = TAssistant.query.filter_by(email=ID,paswd=paswrd).first()
            if TA:
                session.permanent =True
                session['TA'] = str(TA.name)
                session['TAEmail'] = str(TA.email)

                return redirect("/teacherAssistant")

            else:
                return render_template("login.html",ms="user not found")
         else:
             return "not allowed"

    return render_template("main.html")

@app.route('/studentAffairs', methods = ['POST','GET'])
def stu_affairs():
    if request.method == 'GET': 
        if "stu_affairs" in session:
            all_TA= TAssistant.query.all()
            all_Coursse=Course.query.all()
            TA_Len = len(all_TA)
            Coursse_Len = len(all_Coursse)
            return render_template("stu_affear.html" ,msg='', usr =session["stu_affairs"] , x=TA_Len,y=Coursse_Len,TA=all_TA ,course=all_Coursse )
        else:
        
            return redirect("/")
    elif  request.method == 'POST':
         if "stu_affairs" in session:
            if request.form["type1"] == '2':
                ta=request.form["TA"]
                cour=request.form["course"].split(',')
                all_TA= TAssistant.query.all()
                all_Coursse=Course.query.all()
                
                q=TA_Course.query.filter_by(TA=ta,code=cour[0]).first()
                
                if not q:
                    addQ = TA_Course(TA=ta,code=cour[0],course=cour[1],stu_afferis=session["stu_affairs"])
                    db.session.add(addQ)
                    db.session.commit()
                    msg = 'added !'
                else:
                    msg = 'already exist !'


                TA_Len = len(all_TA)
                Coursse_Len = len(all_Coursse)
                
                return render_template("stu_affear.html" ,msg=msg , usr =session["stu_affairs"] ,x=TA_Len,y=Coursse_Len,TA=all_TA ,course=all_Coursse )
            elif request.form["type1"] == '1':
                f=request.files["file"]
                f.save(f.filename) 
                os.rename(f.filename, 'studata.xlsx')
                
                try:  
                    data = pd.read_excel ('studata.xlsx')
                    counter = 0
                    for index, row in data.iterrows():
                        
                        stu= STU.query.filter_by(code=row['code']).first()
                        if not stu:
                            counter = counter +1
                            addQ = STU(name=row['name'],code=row['code'])
                            db.session.add(addQ)
                            db.session.commit()
                      
                    msg = "uploded " +str(counter)+" student" 
                    os.remove("studata.xlsx")
                      
                        
                               
                            
                except:
                    msg = " error "
                    
                    os.remove("studata.xlsx")
                all_TA= TAssistant.query.all()
                all_Coursse=Course.query.all()
                TA_Len = len(all_TA)
                Coursse_Len = len(all_Coursse)
                
                 
               

               
                return render_template("stu_affear.html" ,msg=msg , usr =session["stu_affairs"] ,x=TA_Len,y=Coursse_Len,TA=all_TA ,course=all_Coursse )
            elif request.form["type1"] == '3':
                f=request.files["file"]
                f.save(f.filename) 
                os.rename(f.filename, 'studata.xlsx')
                
                try:  
                    data = pd.read_excel ('studata.xlsx')
                    counter = 0
                    for index, row in data.iterrows():
                        
                        stu= STURegis.query.filter_by(code=row['code'],Course=row['course']).first()
                        if not stu:
                            counter = counter +1
                            addQ = STURegis(name=row['name'],code=row['code'],Course=row['course'])
                            db.session.add(addQ)
                            db.session.commit()
                      
                    msg = "uploded " +str(counter)+" student" 
                    os.remove("studata.xlsx")
                      
                        
                               
                            
                except Exception as e:
                    
                    msg = " error "
                    
                    os.remove("studata.xlsx")
                all_TA= TAssistant.query.all()
                all_Coursse=Course.query.all()
                TA_Len = len(all_TA)
                Coursse_Len = len(all_Coursse)
            return render_template("stu_affear.html" ,msg=msg , usr =session["stu_affairs"] ,x=TA_Len,y=Coursse_Len,TA=all_TA ,course=all_Coursse )
         
         else:
             return "NOT alowed"


@app.route('/teacherAssistant', methods = ['POST','GET'])
def TAV():
    if request.method == 'GET' and "TA" in session :
        all_TA= TA_Course.query.filter_by(TA=session['TAEmail']).all()
        
        x= len(all_TA)

        return render_template("TA_main.html",usr=session["TA"],x=x,corse=all_TA)
    
    else:
        return "not now"
@app.route('/teacherAssistant/view', methods = ['POST'])
def TA_View():
    if "TA" in session:
        cour=request.form["cours"]
        
        # all_TA= Attendace.query.filter_by(TA=session['TA'],Course=cour).all()
        x= db.session.execute("SELECT DISTINCT Week FROM attendace WHERE Course = '"+ cour + "'ORDER BY Week ASC ; ")
        y= db.session.execute("SELECT DISTINCT code , name FROM stu_regis WHERE Course = '"+ cour +"';")
        y2= db.session.execute("SELECT DISTINCT stuCode name  FROM attendace INNER JOIN STU on STU.code = attendace.stuCode  WHERE Course = '"+ cour +"' ; ")
        X,Y,Y2,YN=[],[],[],[]
         
        data =[]
        attendCount =[]
        
        for j in y2:
            Y2.append(j[0])
        for j in x:
            X.append(j[0])
            wee= db.session.execute("SELECT COUNT(DISTINCT stuCode) FROM attendace WHERE Course = '"+ cour + "' and week = '" +str(j[0]) +"' ;")
            for ii in wee:
                
                attendCount.append(ii[0])
        

        
        count = 0     
        for j in y:
            count =count +1
            Y.append(j[0])
            YN.append(str(count)+'*>'+j[1])
        
       
        for a in Y:
            for b in X:
                # add TA email to get only attened stu with him
                stuAtt= Attendace.query.filter_by(stuCode=str(a),Week=str(b),Course=cour).first()
                if stuAtt:
                    
                    data.append(stuAtt)
        
        lenX =len(X)
        lenY =len(Y)
        lenD =len(data)
        return render_template("view.html",weekC=attendCount,c=0,usr=session["TA"],X=X,LX=lenX,Y=Y,YN=YN, Y2=Y2,LY=lenY,LD=lenD,data=data)
    
    else:
        return "not now"   

@app.route("/Quiz", methods=["GET"] )
def quiz():
    if "TA" in session:
        all_TA= TA_Course.query.filter_by(TA=session['TAEmail']).all()
        
        x= len(all_TA)
        xq =[]
        xQ= db.session.execute("SELECT DISTINCT week FROM quize_course WHERE TA = '"+ session['TAEmail'] + "'ORDER BY Week ASC ; ")
       
        for i in xQ:
           
           xq.append(i[0]) 

        xLen = len(xq)
        return render_template("quize.html",usr=session["TA"],xLen=xLen,xQ=xq,x=x,corse=all_TA)
    else:
        return redirect("/")

@app.route("/Quizdata/view", methods=["POST"] )
def quizDView():
    if request.method == 'POST' and "TA" in session :
        data=request.form
        
        
        all_Mark= QuizeCourse.query.filter_by(course=data['courseV'],week=data['Week']).all()
        le =len(all_Mark)
        
        return render_template("ViewQuize.html",usr=session["TA"],X=all_Mark,le=le)


    else:
        return "not allowed"


@app.route("/Quizdata", methods=["POST"] )
def quizD():
    if request.method == 'POST' and "TA" in session :
        cour=request.data.decode("utf-8")
        
        data=json.loads(cour)
        
        
        msg = ""
        
        wek=get_week_number(WEEKDAY.FRI, datetime.now())[1]
        
        stu= STU.query.filter_by(code=data['STU_'],).first()
        if stu:
            stuR= STURegis.query.filter_by(code=data['STU_'],Course=data['cours']).first()
            if not stuR:
                msg = msg +"Not registered in that course"
            else:
                Mark= QuizeCourse.query.filter_by(stu=data['STU_'],course=data['cours'],week=wek).first()
                if Mark:
                    msg = msg +"already exist"
                else:
                    att = QuizeCourse(TA=session['TAEmail'],course=data['cours'],stu=data['STU_'],week=wek,mark=data['Mark'],stuName=str(stu.name))
                    db.session.add(att)
                    db.session.commit()

                    msg = msg +str(stu.name)+" has "+str(data['Mark'])            
        else:
            msg = msg + "wrong code"


        
        
        return ""+msg
    else:
        return "not allowed"


@app.route("/attend", methods=["POST"] )
def attend():
    if request.method == 'POST' and "TA" in session :
        cour=request.data.decode("utf-8")
        data=json.loads(cour)
        wek=get_week_number(WEEKDAY.FRI, datetime.now())[1]
        msg = ''
        stu= STU.query.filter_by(code=data['STU_'],).first()
        
        if stu:
            name=stu.name
            
            
            stuAtt= Attendace.query.filter_by(Week=wek,Course=data['cours'],stuCode=data['STU_']).first()
            
            if not stuAtt:
                today = date.today().strftime("%d/%m/%Y")
                now = datetime.now().strftime("%H:%M:%S")
                wek=get_week_number(WEEKDAY.FRI, datetime.now())[1]
                att = Attendace(Date=today,Time=now,Week=wek,Course=data['cours'],TA=session['TAEmail'],stuCode=data['STU_'],MAC="WEB_APP")
                db.session.add(att)
                db.session.commit()
                
                msg = str(name) +" added"
                
            else:
                
                msg = "already exist"
        else:
            msg='student not faund'               
            
        
        
        
        return msg
    else:
        return redirect("/")

@app.route("/attendApp", methods=["POST"] )
def attendApp():
    
        cour=request.form
        data=(cour)
        
        code =data['stu']
        mac =data['MAC']
        data = cryptocode.decrypt(data['Data'], "DEJAR")
        data = str(data).split('-')
        week=data[0]
        course=data[1]
        time=data[2]
        date=data[3]
        TAEmail=data[4]
        
        msg = ""
        stuR= STURegis.query.filter_by(code=code,Course=course).first()
        if not stuR:
            msg = msg +"Not registered in that course"
        else:
            stuAtt= Attendace.query.filter_by(Week=week,Course=course,stuCode=code).first()
            MACAtt= Attendace.query.filter_by(Week=week,Course=course,MAC=mac).first()
            if stuAtt or MACAtt :
                if MACAtt and not stuAtt :
                    msg = msg +"cheater "

                msg = msg +"already exist "
            else:
                now = datetime.now().strftime("%H:%M:%S")
                datetime_object = datetime.strptime(time,"%H:%M:%S")
                datetime_object = datetime_object.strftime("%H:%M:%S")
                datetime_object=datetime_object.split(':')
                now = now.split(':')
                

                t1 = timedelta(hours=int(now[0]), minutes=int(now[1]))
                t2 = timedelta(hours=int(datetime_object[0]), minutes=int(datetime_object[1]))
                
              
                
                if t1-t2 > timedelta(minutes=31) :
                    msg = msg +"session ended "
                else:
                    # attented ya m3alem
                    att = Attendace(Date=date,Time=time,Week=week,Course=course,TA=TAEmail,stuCode=code,MAC=mac)
                    db.session.add(att)
                    db.session.commit()
                    msg = msg + stuR.name + "attended"



                msg = msg +" done! "
        
        return msg




@app.route("/genrate", methods=["POST"] )
def genrateQR():
    if "TA" in session:
        today = date.today().strftime("%d/%m/%Y")
        now = datetime.now().strftime("%H:%M:%S")
        qr = request.form["QRdata"]
        Qr = request.form["QRdata"]
        wek=get_week_number(WEEKDAY.FRI, datetime.now())[1]
        qr =str(wek)+"-"+ qr +"-"+str(now)+"-"+today+"-"+session["TAEmail"]
        x = datetime.now()
        att = TA_AttendanceC(Email=session["TAEmail"],Name=session["TA"],Course=Qr,Date=x,week=wek)
        db.session.add(att)
        db.session.commit()
        data = cryptocode.encrypt(qr,"DEJAR")
        return render_template("genrate.html",qdata=str(data))
    else:
        return redirect("/") 

@app.route('/stuApp', methods = ['POST'])
def appp():
    datax=request.form
    
    if datax['func'] == "stu_login":
        
        stu= STU.query.filter_by(code=datax['stu'],).first()
        if stu:
            
            data = {
                'state':'found',
                'name':str(stu.name),
            }
        else:
            data = {
                'state':'no',
                'name':'not found',
            }
        return jsonify(data)
    elif datax['func'] == "stu_att":

        list_course =[]
        
        stu= db.session.execute("SELECT DISTINCT Course FROM attendace WHERE stuCode = '"+ datax['stu']  +"' ; ")
        
        for course in stu:
            att=Attendace.query.filter_by(stuCode=datax['stu'],Course=str(course[0])).count()
            cname=Course.query.filter_by(code=str(course[0])).first()
            list_course.append(str(cname.name)+':'+str(att))
            
            

        
        if stu:     
            data = {
                'stu_course':list_course ,
                'state':'good' 
            }
           
        else:
            data = {
                    'stu_course':'no',
                    'state':'no',
                }

       
        return jsonify(data)
    else:
        return "not allowed"




@app.route('/download', methods = ['POST','GET'])
def down():
    p = 'app.apk'
    return send_file(p,as_attachment=True)

if __name__ == '__main__':
     db.create_all()
     Admin=User_admin.query.all()
     if not Admin:
        user = User_admin(name="armada",paswd="123")
        db.session.add(user)
        db.session.commit()
    #  app.run( port=5001 , debug= True)
     app.run()

