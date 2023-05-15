
from flask import Flask, render_template, url_for, flash, redirect,request,session,Response,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_login import login_user, current_user, logout_user, login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_restful import Resource, Api, reqparse
from flask_mail import Message
from datetime import date
import smtplib
import os
import secrets
import json
from flask_cors import CORS
from pusher import pusher
import simplejson
import time
from hashlib import sha1
import hmac
import base64
import string
import random



app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='admin2', password='1234', server='161.97.79.224', database='oes')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, async_mode='eventlet')
app.config['CORS_HEADERS'] = 'Content-Type'
pusher = pusher.Pusher(app_id = "1134388", key = "a60f02f7bde182f427ce", secret = "f42daac6390680efc75f", cluster = "ap2", ssl=True)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
parser = reqparse.RequestParser()
# N = 12
# res = ''.join(random.choices(string.ascii_lowercase +  string.digits, k = N)) 
# exam=str(res)


class UserInformation( db.Model,UserMixin):                  #student table
    __tablename__ = 'App_students'
    
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String())
    student_email = db.Column(db.Text())
    student_phone = db.Column(db.Integer)
    session = db.Column(db.Integer)
    student_address = db.Column(db.Text())
    country = db.Column(db.Text())
    state = db.Column(db.Text())
    city = db.Column(db.Text())
    section = db.Column(db.Text())
    student_password = db.Column(db.Text())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    branch_id_id = db.Column(db.Integer)
    college_id_id = db.Column(db.Integer)
    semester_id_id = db.Column(db.Integer)
   

class Session(db.Model):
    __tablename__ = 'App_session'
    student_id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(40), index=True,default=1) 
class CollegeInfo( db.Model,UserMixin):               #college table
    __tablename__ = 'App_college'
    user_id_id = db.Column(db.Integer, primary_key=True)
    college_name = db.Column(db.String())
    college_code = db.Column(db.Text())
    college_address = db.Column(db.Text())
    college_university = db.Column(db.String())
    college_contact = db.Column(db.Text())
    type=db.Column(db.Text())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    college_id = db.Column(db.Integer)

class ProctorInfo( db.Model,UserMixin):
    __tablename__ = 'App_proctor'

    proctor_id = db.Column(db.Integer, primary_key=True)
    proctor_title = db.Column(db.String())	
    proctor_name = db.Column(db.String())
    proctor_email = db.Column(db.Text())
    proctor_phone = db.Column(db.Integer)
    proctor_password = db.Column(db.Text())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    college_id_id = db.Column(db.Integer)
    assign_section=db.Column(db.Text())

class CollegeExam( db.Model,UserMixin):                #exam table
    __tablename__ = 'App_exam'

    exam_id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String())
    instructions = db.Column(db.Text())
    duration = db.Column(db.Text())
    date = db.Column(db.Text())
    starting_time = db.Column(db.Text())
    ending_time = db.Column(db.Text())
    is_calc = db.Column(db.Text())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    college_id_id = db.Column(db.Integer)
    subject_id_id = db.Column(db.Integer)
    semester_id_id = db.Column(db.Integer)
    branch_id_id = db.Column(db.Integer)


class BranchInfo( db.Model,UserMixin):               #branch table
    __tablename__ = 'App_branch'
    branch_id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    college_id_id = db.Column(db.Integer)


class SemesterInfo( db.Model,UserMixin):               #branch table
    __tablename__ = 'App_semester'
    semester_id = db.Column(db.Integer, primary_key=True)
    semester_name = db.Column(db.String())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    college_id_id = db.Column(db.Integer)

class SubjectInfo( db.Model,UserMixin):              #subject table
    __tablename__ = 'App_subject'
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String())
    subject_code = db.Column(db.String())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    total_marks = db.Column(db.Integer)
    college_id_id = db.Column(db.Integer)
    branch_id_id = db.Column(db.Integer)




class QuestionInfo( db.Model,UserMixin):                       #question table
    __tablename__ = 'App_questions'

    question_id = db.Column(db.Integer, primary_key=True)
    questions = db.Column(db.String())
    option_a = db.Column(db.Text())
    option_b = db.Column(db.Text())
    option_c = db.Column(db.Text())
    option_d = db.Column(db.Text())
    answer = db.Column(db.Text())
    question_type = db.Column(db.Text())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    marks = db.Column(db.Integer)
    branch_id_id = db.Column(db.Integer)
    college_id_id = db.Column(db.Integer)
    exam_id_id = db.Column(db.Integer)
    subject_id_id = db.Column(db.Integer)


class AnswerInfo( db.Model,UserMixin):                  #answer table
    __tablename__ = 'App_answer'

    answer_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text())
    
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    question_id_id = db.Column(db.Integer)
    student_id_id = db.Column(db.Integer)
    exam_id_id = db.Column(db.Integer)

class PasswordInfo( db.Model,UserMixin):                  #answer table
    __tablename__ = 'App_password'
    answer_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text())
    student_email = db.Column(db.Text())

		
class ExamProctor(db.Model,UserMixin):	
    __tablename__ = 'App_exam_proctor_id'	
    id = db.Column(db.Integer, primary_key=True)	
    exam_id = db.Column(db.Integer)	
    proctor_id = db.Column(db.Integer)

def load_user(user_pk):
   return g.session.query(UserInformation).get(user_pk)

@app.route('/',methods=["GET","POST"])                   #signing in to application
def signin():
    if request.method == 'POST':
        session['email'] = request.form['email']
        print(session['email'])
        session['password'] = request.form['password']
        registeredUser = UserInformation.query.filter_by(student_email=session['email'],student_password=session['password']).first()    #fetching student detail
        ProctorUser = ProctorInfo.query.filter_by(proctor_email=session['email'],proctor_password=session['password']).first() 
                   #fetching proctor detail
        try:
      #student a particular proctor is assigned
            college_details = CollegeInfo.query.filter_by(college_id=ProctorUser.college_id_id).first()
            check_proctor = CollegeExam.query.filter_by(college_id=ProctorUser.college_id_id).first()
        except:
            print("student signed in...")
            

        try:
            
            #getting all the details of student
            # signin.name=registeredUser.student_name
            session['name']=registeredUser.student_name
            print(session['name'])
            # print("namre",session['name'])
            session['email']=registeredUser.student_email
            # print("namre",session['email'])
            session['student_id']=registeredUser.student_id
            # print("namre",session['student_id'])
            session['college_id_id']=registeredUser.college_id_id
            # print("namre",session['college_id'])
            session['semester_id']=registeredUser.semester_id_id
            session['branch_id']=registeredUser.branch_id_id
            # print("JHH",session['branch_id'])
            from datetime import date
            today = date.today()  
            exam_details = CollegeExam.query.filter_by(college_id_id=session['college_id_id'],semester_id_id=session['semester_id'],branch_id_id=session['branch_id'],date=today).all()
            print(exam_details)
            if len(exam_details)==0:
                msg="No Exam Scheduled!!!"
                return render_template("base.html",msg=msg)
            from datetime import datetime
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            FMT = '%H:%M'
            for e in exam_details:
                tdelta = datetime.strptime(e.starting_time, FMT) - datetime.strptime(current_time, FMT)
                tdelta1 = datetime.strptime(e.ending_time, FMT) - datetime.strptime(current_time, FMT)
                if e.starting_time>=current_time or e.ending_time>=current_time:
                    session['exam_id']=e.exam_id
                    AnswerUser = AnswerInfo.query.filter_by(student_id_id=session['student_id'],exam_id_id=session['exam_id']).first()
                    
                AnswerUser=None  
        except:
            print("something went wrong")
       

        if registeredUser is not None and AnswerUser is None :      #checking condition for student login
            from datetime import date
            today = date.today()   
            print('Logged in..')
            session['logged_in']=True
            today = date.today()  
            college_details = CollegeInfo.query.filter_by(college_id=session['college_id_id']).first()
            print("School hai ya college",college_details.type)
            session['type']=college_details.type
            exam_details = CollegeExam.query.filter_by(college_id_id=session['college_id_id'],semester_id_id=session['semester_id'],branch_id_id=session['branch_id'],date=today).all()
            from datetime import datetime
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            FMT = '%H:%M'
            for e in exam_details:
                tdelta = datetime.strptime(e.starting_time, FMT) - datetime.strptime(current_time, FMT)
                tdelta1 = datetime.strptime(e.ending_time, FMT) - datetime.strptime(current_time, FMT)
                dur=int(e.duration)
                tdelta=int((tdelta.total_seconds())/60)
                tdelta1=int((tdelta1.total_seconds())/60)
                print(tdelta,tdelta1)
                session['tdelta1']=tdelta1
                print(tdelta1)
                if (tdelta<=5 and tdelta1>=0):
                    # print("apna is time frame ka exam",e.exam_name)
                    session['duration']=e.duration
                    session['exam_name']=e.exam_name
                    session['instructions']=e.instructions
                    session['calculator']=e.is_calc
                    session['exam_id']=e.exam_id
                    exam_proctor = ExamProctor.query.filter_by(exam_id=session['exam_id']).all()	
                    for i in exam_proctor:	
                        print("ye hai proctor",i.proctor_id)
                    from datetime import datetime
                    now = datetime.now()
                    now=now.strftime("%H:%M")
                    start = e.starting_time
                    end1 = e.ending_time
                    new=datetime.strptime(start,"%H:%M")
                    new=new.strftime("%H:%M")
                    old=datetime.strptime(end1,"%H:%M")
                    old=old.strftime("%H:%M") 
                    branch_info=BranchInfo.query.filter_by(college_id_id=session['college_id_id']).first()
                    semester_info=SemesterInfo.query.filter_by(college_id_id=session['college_id_id']).first()
                    subject_info=SubjectInfo.query.filter_by(college_id_id=session['college_id_id']).first()
                    #print("Branch Name "+branch_info.branch_name)
            try:
                session['college_name']=college_details.college_university  #getting college and exam details

            except:
                msg="Today no exam available for you!!"                     #if exam date has passed
                return render_template('log.html',msg=msg)
            try:
                print(registeredUser.country)
                if registeredUser.country=='India':
                    return render_template('changepassword1.html')
                else:
                    print(PasswordInfo.answer)
                    return render_template('newfile.html',registeredUser=registeredUser,duration_exam=session['duration'],college_details=college_details,new=new,old=old,now=now,exam_name=session['exam_name'],start=start,end1=end1,ins=session['instructions'],type=session['type'],branch_name=branch_info.branch_name,semester_name=semester_info.semester_name,subject_name=subject_info.subject_name)
            except:
                msg="you can login only 5 minutes before examination"                  #if exam date has passed
                return render_template('log.html',msg=msg)
        elif session['email']=='demo@gmail.com' and session['password']=='demo': 
            import time
            import datetime
            t = time.localtime()
            current_time = time.strftime("%H:%M", t)
            nextTime = datetime.datetime.now() + datetime.timedelta(minutes = 15)
            end_time=nextTime.strftime("%H:%M")
            return render_template('demoinfo.html',current_time=current_time,end_time=end_time)  
        elif ProctorUser is not None:  	
            from datetime import date	
            today = date.today()   	
            from datetime import datetime	
            now = datetime.now()	
            current_time = now.strftime("%H:%M")	
            FMT = '%H:%M'	
            try:	
                sections = []	
                exam_details = CollegeExam.query.filter_by(college_id_id=ProctorUser.college_id_id,date=today).all()	
                for e in exam_details:	
                    if e.starting_time>=current_time or e.ending_time>=current_time:	
                            exam_proctor=ExamProctor.query.filter_by(exam_id=e.exam_id,proctor_id=ProctorUser.proctor_id)	
                            for ep in exam_proctor:	
                                print("ye hai proctor id",ep.proctor_id)	
                                assigned_proctor=ProctorUser.assign_section	
                                proctor_sections=assigned_proctor.split(",")	
                                for ps in proctor_sections:	
                                    section1 = UserInformation.query.filter_by(section=ps,branch_id_id=e.branch_id_id,semester_id_id=e.semester_id_id,college_id_id=e.college_id_id).all()	
                                    print("ye hai section",section1)	
                                    for i in section1:	
                                        q_info = i.student_email	
                                        sections.append(q_info)	
                                print(sections)	

                    #sections=None	
            except:	
                msg="You are not assigned to exam"	
                render_template('base.html',msg=msg)	
            full_proctor=ProctorUser.proctor_title+" "+ProctorUser.proctor_name 
            print(full_proctor) 	
                                         #login proctor	
            print("ye hai apne sections",sections)                            	
            return render_template('proctor.html',proctorname=full_proctor,college_name=college_details.college_university,sections=sections)
        try:
            if AnswerUser is not None:                              #checking answer table for particular student
                msg='You already attempted the test'
                return render_template('log.html',msg=msg)
            else:
                msg='No exam has been assigned to u...'             #checking exam detail
                return render_template('log.html',msg=msg)
        except:
            msg='Invalid Credentials!!!'                         #checking email id and password for login.
            return render_template('log.html',msg=msg)       
        
    else:
        return render_template('log.html')
 
@app.route('/passwordchanged',methods=["GET","POST"])
def new_pass():
    pass1=request.form['pass1']
    pass2=request.form['pass2']
    if pass1==pass2:
        current_user= UserInformation.query.filter_by(student_email=session['email'],student_password=session['password']).first() 
        # print(current_user.student_password)
        current_user.student_password=pass1
        current_user.country=current_user.country.upper()
        db.session.commit()
        # print(current_user.student_password)
        msg="password changed successfully!!"
        return render_template('log.html',msg=msg)
    else:
        print("we failed")
        msg="new password & confirm password is not matching"
        return render_template('changepassword1.html',msg=msg)
@app.route('/test',methods=["GET","POST"])               #main test page
def test1():
    try:
        AnswerUser = AnswerInfo.query.filter_by(student_id_id=session['student_id'],exam_id_id=session['exam_id']).first()      #checking answer table
        if AnswerUser is None:
            return render_template('quizJS.html',tdelta=session['tdelta1'], user_id=session['student_id'], stu_name=session['name'],duration_exam=session['duration'],student_email=session['email'],calc=session['calculator'],college=session['college_name'])
        else:
            return render_template('login.html')
    except:
          #checking answer table
    
        return render_template('newquizJS.html',tdelta=15, user_id=322, stu_name='Demo',duration_exam=15,student_email='demo@gmail.com',calc='true',college='Demo college of Engineering')


    return render_template("log.html")    
@app.route('/test1',methods=["GET","POST"])               #main test page
def test():
    AnswerUser = AnswerInfo.query.filter_by(student_id_id=session['student_id'],exam_id_id=session['exam_id']).first()      #checking answer table
    if AnswerUser is None:
        return render_template('test.html',tdelta=session['tdelta1'], user_id=session['student_id'], stu_name=session['name'],duration_exam=session['duration'],student_email=session['email'],calc=session['calculator'],college=session['college_name'])
    else:
        return render_template('login.html')

@app.route('/new/guest', methods=['POST'])          #chat application part
def guestUser():
    data = request.json
    pusher.trigger(u'general-channel', u'new-guest-details', { 
        'name' : data['name'], 
        'email' : data['email']
        })
    return json.dumps(data)

@app.route("/pusher/auth", methods=['POST'])       #chatapplication part
def pusher_authentication():
    auth = pusher.authenticate(channel=request.form['channel_name'],socket_id=request.form['socket_id'])
    return json.dumps(auth)


class QuestionSubmit1(Resource):                  #fetching question from the database and rendering it on the page. (for submission of test)
    def post(self):
        data = request.data.decode('utf-8')
        data = json.loads(data)
        print(data)
        student_id = data['user_id']
        value = data['ans']
        # if len(value)==0:
        #     print("empty dictionary")
        #     value={session['question_id']:'Not Answered'}
        print("ye hai value",value)
        import pandas as pd
        from pandas import DataFrame
        df1=list(value.values())
        df2=list(value.keys())
        df3=[df1,df2]
        # print(df3)
        exam_details = CollegeExam.query.filter_by(college_id_id=1,semester_id_id=113,branch_id_id=180).first()
        df = DataFrame (df3,['answer','question_id_id']).transpose()
        # print(df)
        df['student_id_id']=322
        df['exam_id_id']=382
        import datetime
        x = datetime.datetime.now() 
        df['doc']=x
        new_x=str(x)
        import random
        n = random.randint(1000,100000)
        new_n=str(n)
        df['slug']=new_x+new_n
        import sqlalchemy      #submitting the answer back in to the database.
        engine=sqlalchemy.create_engine('mysql+mysqlconnector://admin2:1234@161.97.79.224/oes')
        con=engine.connect()
        table_name='App_answer'
        df.to_sql(table_name,con,if_exists='append',index=False)
        con.close()
        # print("All is well")
        return({'message':'Test Submitted Successfully'})
        
class QuestionList1(Resource):        #fetching questions from the database
    def post(self):
        data = request.data.decode('UTF-8')
        data = json.loads(data)
        # print(data)
        student_id = data['user_id']
        # print(student_id)
        question = []
        # print(current_user)
        student = UserInformation.query.filter_by(student_id=322).first()
        question = QuestionInfo.query.filter_by(college_id_id=1,exam_id_id=382).all()
        # print( "ye hai questions",question)
        questions = []
        for index, i in enumerate(question):
            q_info = {}
            q_info['question_id'] = i.question_id
            q_info['question'] = i.questions
            q_info['option_a'] = i.option_a
            q_info['option_b'] = i.option_b
            q_info['option_c'] = i.option_c
            q_info['option_d'] = i.option_d
            import random
            import numpy as np
            questions.append(q_info)
        print(questions)
        res = []
        for idx, sub in enumerate(questions, start = 0):
            if idx == 0:
                res.append(list(sub.keys()))
                res.append(list(sub.values()))
            else:
                res.append(list(sub.values()))
        np.random.shuffle(res)
        
        keys=['question_id','question','option_a','option_b','option_c','option_d']
        d = [dict(zip(keys, l)) for l in res ]
        for i in range(len(d)):
            if d[i]['question'] == 'question':
                del d[i]
                break
        
        return d



class QuestionSubmit(Resource):                  #fetching question from the database and rendering it on the page. (for submission of test)
    def post(self):
        data = request.data.decode('utf-8')
        data = json.loads(data)
        print(data)
        student_id = data['user_id']
        value = data['ans']
        # if len(value)==0:
        #     print("empty dictionary")
        #     value={session['question_id']:'Not Answered'}
        print("ye hai value",value)
        import pandas as pd
        from pandas import DataFrame
        df1=list(value.values())
        df2=list(value.keys())
        df3=[df1,df2]
        # print(df3)
        exam_details = CollegeExam.query.filter_by(college_id_id=session['college_id_id'],semester_id_id=session['semester_id'],branch_id_id=session['branch_id']).first()
        df = DataFrame (df3,['answer','question_id_id']).transpose()
        # print(df)
        df['student_id_id']=session['student_id']
        df['exam_id_id']=session['exam_id']
        import datetime
        x = datetime.datetime.now() 
        df['doc']=x
        new_x=str(x)
        import random
        n = random.randint(1000,100000)
        new_n=str(n)
        df['slug']=new_x+new_n
        import sqlalchemy      #submitting the answer back in to the database.
        engine=sqlalchemy.create_engine('mysql+mysqlconnector://admin2:1234@161.97.79.224/oes')
        con=engine.connect()
        table_name='App_answer'
        df.to_sql(table_name,con,if_exists='append',index=False)
        con.close()
        # print("All is well")
        return({'message':'Test Submitted Successfully'})
        
class QuestionList(Resource):        #fetching questions from the database
    def post(self):
        data = request.data.decode('UTF-8')
        data = json.loads(data)
        # print(data)
        student_id = data['user_id']
        # print(student_id)
        question = []
        # print(current_user)
        student = UserInformation.query.filter_by(student_id=session['student_id']).first()
        question = QuestionInfo.query.filter_by(college_id_id=session['college_id_id'],exam_id_id=session['exam_id']).all()
        # print( "ye hai questions",question)
        questions = []
        for index, i in enumerate(question):
            q_info = {}
            q_info['question_id'] = i.question_id
            q_info['question'] = i.questions
            q_info['option_a'] = i.option_a
            q_info['option_b'] = i.option_b
            q_info['option_c'] = i.option_c
            q_info['option_d'] = i.option_d
            q_info['question_type'] = i.question_type


            import random
            import numpy as np
            questions.append(q_info)
        print("These are set of questions we have",questions)
        res = []
        for idx, sub in enumerate(questions, start = 0):
            if idx == 0:
                res.append(list(sub.keys()))
                res.append(list(sub.values()))
            else:
                res.append(list(sub.values()))
        np.random.shuffle(res)
        
        keys=['question_id','question','option_a','option_b','option_c','option_d','question_type']
        d = [dict(zip(keys, l)) for l in res ]
        for i in range(len(d)):
            if d[i]['question'] == 'question':
                del d[i]
                break
        print(d)
        return d
def get_id(self):                                                           
    return str(self.session_token)

@app.route('/logout')                             #for logging out the student
def logout():
    session.clear()
    return render_template('log.html')




api.add_resource(QuestionList, '/question-list')
api.add_resource(QuestionSubmit, '/submit-test')
api.add_resource(QuestionList1, '/question-list1')
api.add_resource(QuestionSubmit1, '/submit-test1')

@app.route('/phpexam', methods=['GET'])
def renderExam():
    return render_template('examphp.html')

@app.route('/phpproctor', methods=['GET'])
def renderProctor():
    return render_template('proexam.html')
@app.route('/new/vdoCall', methods=['POST'])          #vdo call application part
def commonChannel():
    data = request.json
    pusher.trigger(u'vdo-channel', u'new-call-details', { 
        'name' : data['name'], 
        'email' : data['email']
        })
    print('added new channel')
    return json.dumps(data)

@app.route('/newphp/vdoCall', methods=['POST'])          #vdo call application part
def phpChannel():
    data = request.json
    print("this is data",data)
    pusher.trigger(u'vdo-channel', u'new-phpcall-details', { 
        'name' : data['name'], 
        'email' : data['email'],
        'procname': data['procname']
        })
    print('added new channel')
    return json.dumps(data)

@app.route('/getcredential', methods=['POST'])
def generateCredential():
    data = request.json
    print(data)
    print("hjsdhjdfh")
    secretKey = b'3575819665154b268af59efedee8826e'
    unixTimeStamp = int(time.time()) + 24*3600
    username = str(unixTimeStamp) + ':' + data['verifiedName']
    hashed = hmac.new(secretKey, bytes(username, 'utf-8'), sha1).digest()
    password = base64.b64encode(hashed).decode()
    credentials = {
        'username': username,
        'credential' : password
    }
    return json.dumps(credentials)


if __name__ == "__main__":                           #main function call
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(session_token):
        return Session.query.filter_by(session_token=session_token).first()
    login_manager.login_view = 'login'
    app.debug = True
    app.templates_auto_reload = True
    app.run()
