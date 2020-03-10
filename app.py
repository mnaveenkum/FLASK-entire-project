from flask import Flask, render_template,redirect,request,flash,session,url_for
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from createdatabase import *
from flask_login import LoginManager,login_user,current_user,logout_user,login_required
from flask_uploads import IMAGES,UploadSet,configure_uploads
from flask_mail import Mail,Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='****'
app.config['MAIL_PASSWORD']='****'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
photos=UploadSet('photos',IMAGES)
app.config['UPLOADED_PHOTOS_DEST']='static/upload_files'
configure_uploads(app,photos)
app.debug = True
Base = declarative_base()
# Connect to database
engine = create_engine('sqlite:///practice.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind = engine
# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def index():
	return render_template("home.html")
@app.route('/home')
def home():
	return render_template("home.html")


@app.route('/signup',methods=['POST','GET'])
def signup():
	if request.method == 'POST':
		newitem = Voter(
		id = request.form['id'],
		name = request.form['name'],
		email = request.form['email'],
		password = request.form['password'] )
		session.add(newitem)
		session.commit()
		flash("New user added successfully")
		# flash('record added successfully')
		return render_template("/signup.html")
		
	else:
		# flash('')
		return render_template("/signup.html")	


@app.route('/Add_User',methods=["GET","POST"])
def Add_User():
	if request.method=="POST":
		filename=photos.save(request.files['file1'])
		data=Register(Fname=request.form['Fname'],Lname=request.form['Lname'],image=filename,username=request.form['uname'],Email=request.form['email'],Adharno=request.form['adharno'],Password=request.form['pswd'])
		session.add(data)
		session.commit()
		m=request.form['email']
		content=Message('successfully registered',sender="***************",recipients=[m])
		mail.send(content)
		return redirect('/signin')
	else:
		return render_template('/signup')
@app.route('/REVENUE')		
def REVENUE():
	return render_template('/REVENUE.html')

@app.route('/complaintbox',methods=(['POST','GET']))
def complaintbox():
	if request.method=='POST':
	 	 com_a=ComplaintBox(Sector=request.form['sel1'],Sector_area=request.form['sel2'],complaint=request.form['complaint'],image1=photos.save(request.files['image']))
	 	 session.add(com_a)
	 	 session.commit()
	 	 com_aa=session.query(ComplaintBox).all()

	 	 # flash("data added successfully")
	 	 email1=request.form['sel1']
	 	 print(email1)
	 	 email2=request.form['sel2']
	 	 print(email2)
	 	 comments=request.form['complaint']
	 	 # msg= "   URL: http://localhost:5000/"+d
	 	 msg=Message("Complaint",sender="****", recipients=[email1,email2])
	 	 #msg.html=comments
	 	 mail.send(msg)
	 	 return "sent"	 
	 	 # return render(req,"website/mailsent.html",context)
	 	 #return render_template("complaints.html",comp=com_aa)
	 	 # flash("data added successfully")
	else:
		flash('data not inserted')
		return render_template("complaint_mail.html")
	return render_template("complaint_mail.html")
# @app.route('/areas',methods=(['POST','GET']))
# def Areass():
# 	if request.method=='POST':
# 		area_aa=session.query(Areas).all()
# 		return render_template("compl.html",ar=area_aa)
@app.route('/Compl',methods=["GET","POST"])
def compl():
	areas = session.query(Areas).all()
	return render_template("complaint_mail.html", areas=areas)

@app.route('/EDUCATION')		
def EDUCATION():
	return render_template('/EDUCATION.html')

@app.route('/POLICE')
def POLICE():
        return render_template('/POLICE.html')

 
@app.route('/AGRICULTURAL')  
def AGRICULTURAL():
	 return render_template('/AGRICULTURAL.html')
      

            	
@app.route('/kurnool')	
def kurnool():
		return render_template('/kurnool.html')	

@app.route('/kadapa')	
def kadapa():
		return render_template('/kadapa.html')	
@app.route('/chittoor')	
def chittoor():
		return render_template('/chittoor.html')	

@app.route('/about')
def about_info():
	return render_template('/about.html')
@app.route('/contact')
def contacts():
	return render_template('/contact.html')
@app.route('/signup')
def signups():
	return render_template('/signup.html')
@app.route('/signin')
def signin():
	return render_template('/signin.html')
@app.route('/display')
def display():
	usersdata=session.query(Register).all()
	return render_template('/display.html',udata=usersdata)
@app.route('/deletedata/<int:data_id>',methods=["GET"])
def deletedata(data_id):
	deleteRes = session.query(Register).filter_by(id=data_id)
	deleteRes.delete()
	session.commit()
	return redirect('/display')


@app.route('/editdata/<int:data_id>',methods=['GET','POST'])
def editdata(data_id):
	if request.method=="post":
		editRest=session.query(Register).filter_by(id=data_id).one()
		editRest.name=request.form['name']
		session.commit()
		return redirect('/display')
	else:
		editRest=session.query(Register).filter_by(id=data_id).one()
		return render_template("editdata.html",editRest=editRest)
@app.route('/loginpage',methods=['post','GET'])
def loginpage():
	if current_user.is_authenticated:
		return redirect('/compl')
		print("one")
	elif request.method=="POST":
		owner=session.query(Register).filter_by(Email=request.form['email'],Password=request.form['pswd']).first()
		if owner:
			login_user(owner)
			next_page=request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash("login failed")
	else:
		return render_template('/signin.html')
@app.route('/logout')
def logout():
	logout_user()
	return redirect('/')

@app.route('/profile')
def profile():
	return render_template('/profile.html')

@app.route('/Complaints')
def Complaints():
	return render_template('/Complaints.html')





if __name__ == '__main__':
	app.config['SECRET_KEY']="hi"
	login_manager=LoginManager(app)
	login_manager.loginview='login'
	login_manager.login_message_category='info'

	@login_manager.user_loader
	def load_user(user_id):
		return session.query(Register).get(int(user_id))
	app.debug=True
	app.run(host='0.0.0.0',port=5000)