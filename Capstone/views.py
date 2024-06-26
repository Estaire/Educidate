import os,json,string,base64
from flask import render_template, request, redirect, url_for, flash, session, abort,send_from_directory,Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from cryptography.fernet import Fernet
from dataclasses import dataclass

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Ilovemlp123@localhost/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='secretkey'
data = [] 
db = SQLAlchemy(app)
app.app_context().push()    

@dataclass
class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key= True)
    username=db.Column(db.String(50))
    password=db.Column(db.String(50))

    def __init__(self,password,username):
        self.username= username
        self.password= password
my_password = b"secret_AES_key_string_to_encrypt/decrypt_with"

f = open('Course.json')
p=open('Codes.json')

data = json.load(f)
codes=json.load(p)

def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data

def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding

def get_json(password):
    return jsonify(password)

@app.route("/", methods= ['POST','GET'])
def login():
    print(session.get('username'))
    if request.method== 'POST':
        info=[]
        thisusername=request.form["email"]
        thispassword=request.form["password"]
        dbusername=db.session.query(User).filter(User.username==thisusername).first()
        dbpassword=User.query.filter_by(password=thispassword).first()
        decrypted=decrypt(my_password,(dbusername.password))
        print(decrypted)
        info.append(dbusername)
        info.append(dbpassword)
       #-- npassword=decrypt(my_password,password['password'])
        if info[0] != None and thispassword.encode('ASCII')==decrypted:
            print(info[0])
            session['username']=thisusername
            session['password']=thispassword
            print(session.get('username'))
            return redirect("/home")
        else:   
            flash("Credentials incorrect","login")
            return redirect("/home")
    else:
        return render_template("frontpage.html")

@app.route("/logout",methods=['GET'])
def logout():
    session.pop('username',None)
    session.pop('password',None)
    session.pop('major',None)
    session.pop('minor',None)
    session.pop('total',None)
    session.pop('required',None)
    session.pop('elective',None)
    session.pop('courses',None)

    return redirect("/")
@app.route("/signup",methods=['POST','GET'])
def signup():
    if request.method =='POST':
        username=request.form["email"]
        password=request.form["password"]
        password=encrypt(my_password,bytes(password,'utf-8'))
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
    return render_template("signUp.html")

@app.route("/home", methods=['POST','GET'])
def main():
    if not session.get('username'):
        return redirect(url_for('login'))
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
        if(session['minor']):
            flash("Cannot have this major/minor combination",'major')
            return redirect('/major')

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
        return redirect("/tracker")
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
    if session.get('path')!= "/courses":
        return render_template("CompletedCourses.html")

@app.route("/tracker",methods=['POST','GET'])
def tracker():
    if request.method=="POST":
        return redirect("/")
    courses= session.get('courses')
    required=session.get('required')
    if session.get('username'):
        with open('Users.json','r+') as l:
            helper= json.load(l)
            for x in helper['Users']:
                if x['username'] == session['username']:
                    with open('Course.json','r+') as k:
                        coursehelper= json.load(k)
                        for m in coursehelper['Courses']:
                            if m['name'] == x['major']:
                                proxy = m['credits'][0] + m['credits'][1]
                                total = int(proxy)
                                session['total']=total
                                proxy = ""
                                proxy = m['credits'][3]+m['credits'][4]
                                elective = int(proxy)
                                session['elective']=elective
                                required = m['required']
                                session['required'] = required
                                courses = x['courses']
                                session['courses'] = courses
                                session['faculty'] = m['faculty'] 
                                session['courses'] = courses
                                remainingCourses = [ele for ele in required if ele not in courses]
                                print("LOOK HERE",remainingCourses)
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
            if i[:4] in session.get('faculty') or session.get('faculty') == "none" and session['elective'] > 0:
                session['elective'] = session['elective'] - 3
        print(session.get('total'))
        print(session.get('elective'))
    try:
        session.pop('courses')
    except:
        print("No courses to pop")
    percentage=int(((total-session['total'])/total)*100)
    return render_template("progress.html", credits=session['total'], required=remainingCourses,elective=session['elective'],percentage=percentage)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)