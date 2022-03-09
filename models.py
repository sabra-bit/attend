from __main__ import app
from flask_sqlalchemy import SQLAlchemy

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