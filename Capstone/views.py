import os,json,string
from flask import render_template, request, redirect, url_for, flash, session, abort,send_from_directory,Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='secretkey'
data = [] 
db = SQLAlchemy(app)
app.app_context().push()    

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key= True)
    username=db.Column(db.String(50))
    password=db.Column(db.String(50))

    def __init__(self,password,username):
        self.username= username
        self.password= password


f = open('Course.json')
p=open('Codes.json')

data = json.load(f)
codes=json.load(p)


@app.route("/", methods= ['POST','GET'])
def login():
    print(session.get('username'))
    if request.method== 'POST':
        info=[]
        thisusername=request.form["email"]
        print(thisusername)
        thispassword=request.form["password"]
        dbusername=db.session.query(User).filter(User.username==thisusername).first()
        dbpassword=User.query.filter_by(password=thispassword).first()
        info.append(dbusername)
        info.append(dbpassword)
        print(dbusername,dbpassword)
        if info[0] != None and info[1] != None:
            print(info)
            session['username']=thisusername
            session['password']=thispassword
            print(session.get('username'))
            return redirect("/home")
        else:   
            return render_template("frontpage.html")
    else:
        return render_template("frontpage.html")

@app.route("/signup",methods=['POST','GET'])
def signup():
    if request.method =='POST':
        username=request.form["new-username"]
        password=request.form["new-password"]
        dbusername=db.session.query(User).filter(User.username==username).first()
        print (dbusername)

        if dbusername !=None:
            return redirect("/signup")
        else:
            with open('Users.json','r+') as m:
                CreateNewUser=json.load(m)
                CreateNewUser['Users'].append({"username":username,"major":"",'courses':[]})
                m.seek(0)
                json.dump(CreateNewUser,m,indent=4)
                m.truncate()
            new_user =User(password,username)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/")
    return render_template("sign-up.html")

@app.route("/home", methods=['POST','GET'])
def main():
    if request.method =='POST':
        session['path']=request.path
        return render_template("dashboard.html")
    return render_template("dashboard.html")

@app.route("/major", methods=['POST','GET'])
def major():
    exists= False
    if request.method =='POST':
        major=request.form["major"]
        minor=request.form["minor"]
        print(major,minor)
        session['major']= major
        session['minor']=minor

        print(session.get('major'))
        print(exists)
        if session['username'] is not None:
            with open('Users.json','r+') as k:
                ChangeUserMajor = json.load(k)
                for q in ChangeUserMajor['Users']:
                    if q['username'] == session.get('username'):
                        exists= True
                if exists == False:
                    k.seek(0)
                    print("wrong")
                    ChangeUserMajor['Users'].append({"username":session.get('username'),"major":session.get('major'),"courses":[]})
                    json.dump(ChangeUserMajor,k,indent=4)
                    k.truncate()
                if exists ==True:
                    for x in ChangeUserMajor['Users']:
                        if x['username'] == session['username']:
                            x['major'] = major
                            k.seek(0)
                            json.dump(ChangeUserMajor,k,indent = 4)
                            k.truncate()

                                        
        for i in data['Courses']:
                if i['name'] == major:
                    proxy = i['credits'][0] + i['credits'][1]
                    total = int(proxy)
                    session['total']=total
                    proxy = ""
                    proxy = i['credits'][3]+i['credits'][4]
                    elective = int(proxy)
                    session['elective']=elective
                    required = i['required']
                    session['required']=required
                    faculty= i['faculty']
                    session['faculty']=faculty
                    print(faculty)
                    print(elective,total)
        return redirect("/courses")
    return render_template("MajorMinor.html")

@app.route("/courses", methods=['GET','POST'])
def courses():
    major = session.get("major")
    if request.method=='POST':
        print("post")
        data = request.get_json()
        courses = data.get('courses', [])
        print(courses)
        session['courses']=courses
        for x in courses:
            if x[:4] not in codes['Codes'] or len(x) != 8:
                #print(x)
                print("this is the problem")
                return redirect("/")
        with open('Users.json','r+') as l:
            UpdateUserCourses= json.load(l)
            for x in UpdateUserCourses['Users']:
                if x['username'] == session['username']:
                    print("enter")
                    x['courses']=courses
                    l.seek(0)
                    json.dump(UpdateUserCourses,l,indent = 4)
                    l.truncate()
        #for i in data['Courses']:
            #if (course1 and course2 and course3) in i['required'] and i['name'] == major:
                #print(course1)
                #print(course2)
                #print(course3)
                #print(session.get("major"))
            #else:
                #return redirect("/tracker")*
        return redirect("/tracker")
    if session.get('path')!= "/courses":
        return render_template("CompletedCourses.html")

@app.route("/tracker",methods=['POST','GET'])
def tracker():
    if request.method=="POST":
        return redirect("/")
    courses= session.get('courses')
    required=session.get('required')
    if session.get('courses') is None:
        if session.get('username') is None:
            print("Guest User")
            session.pop('courses')
        else:
            required=session.get('required')
            try:
                with open('Users.json','r+') as k:
                    t = json.load(k)
                    for x in t['Users']:
                        print(x['username'])
                        if x['username'] == session.get('username'):
                            bruh = x['courses']
                            print(bruh)
                            remainingCourses = [ele for ele in required if ele not in bruh]
                            print(remainingCourses)
                            print(session.get('elective'))
                            print(session.get('total'))    
                            session['total']=session['total'] - (len(session.get('courses')*3))
                            for i in session['courses']:
                                        if i[:4] in session.get('faculty') or session.get('faculty')=="none":
                                            session['elective'] = session['elective'] - 3
                            print(session.get('total'))
                            print(session.get('elective'))                       
            except:
                print("User does not exist in system")
        print("testtestsetstst")
    else:
        courses= session.get('courses')
        required=session.get('required')
        remainingCourses = [ele for ele in required if ele not in courses]
        print(remainingCourses)
        #print(session.get('courses'))
        print(session.get('elective'))
        print(session.get('total'))
        session['total']=session['total'] - (len(session.get('courses')*3))
        for i in session['courses']:
            if i[:4] in session.get('faculty') or session.get('faculty') == "none":
                session['elective'] = session['elective'] - 3
        print(session.get('total'))
        print(session.get('elective'))
    try:
        session.pop('courses')
    except:
        print("No courses to pop")
    return render_template("progress.html", credits=session['total'], required=required,elective=session['elective'])



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)