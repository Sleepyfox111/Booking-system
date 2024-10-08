
  #window is second form
import sqlite3
#Import SQL
import os
import os.path
#Import datetime
import datetime
from datetime import datetime # for strptime()
from guizero import *
#global Adult_price
#global Kids_price
#Kids_price == 5
sql = """
CREATE TABLE "UserTbl" ( 
"UserID" INTEGER NOT NULL,
"Username" TEXT,
"Password" TEXT,
"Fname" TEXT,
"Sname" TEXT,
"Email" TEXT,
"Phonenumber" TEXT, 
PRIMARY KEY("UserID" AUTOINCREMENT)
);
CREATE TABLE "BookingTbl" (
"BookingID"  INTEGER NOT NULL,
"BookingDate" DATE,
"BookTime" datetime,
"Adults"  Int,
"Kids"  Int,
"TotalCost"  STRING,
"UserID"  INTEGER,
PRIMARY KEY("BookingID" AUTOINCREMENT),
CONSTRAINT "UserID_fk"  FOREIGN KEY("UserID") REFERENCES "UserTbl"("UserID")
);
insert into UserTbl (Username, Password, Fname, Sname, Email, Phonenumber) values ('Josh','pass', 'Josh', 'Alcott', 'Josh@gmail.com', '0797229124');
insert into UserTbl (Username, Password, Fname, Sname, Email, Phonenumber) values ('Cry','pass', 'Crystal', 'Chan', 'Crystal@gmail.com','079781929');
insert into BookingTbl (BookingDate, BookTime, Adults, Kids, TotalCost, UserID) values ('20/10/22', '12:30', '1', '0', '10', 1);
"""
#
#Global variables here
#
database_file = 'UserApp.db'
LoggedIn_ID = 1 # store customerID when logged in
#
#Delete the database, only if it exists
#
if os.path.exists(database_file):
	os.remove(database_file)
#
    ##Connect to the database
conn = sqlite3.connect(database_file) #My connection is called 'conn'
#Get a cursor pointing to the database
cursor = conn.cursor()
#Create the tables
cursor.executescript(sql) # creates from DDL above, script more than 1 command
#Commit to save everything
conn.commit()
#Close the connection to the database
#
#Queries the database using the database parameter as the database
#to query and the query parameter as the actual query to issue
# for SELECT
def query_database(database, query):
	Lconn = sqlite3.connect(database)
	cur = Lconn.cursor()			# use a local cursor
	cur.execute(query)
	rows = cur.fetchall()
	cur.close()
	return rows
#
#
def execute_sql(database, sql_statement):
	#Executes the sql statement to INSERT and UPDATE rows
	Lconn = sqlite3.connect(database)
	cur = Lconn.cursor()
	cur.execute(sql_statement)
	Lconn.commit()
	return cur.lastrowid
#############
def Login():
	# this will show the user a loggin window and hide the menu
	app.hide()
	login.show()
#############
def Signup():
	# this will show the user a loggin window and hide the menu
	app.hide()
	signup.show()
	login.hide()
#############
def Back():
	#this is used if the user miss click and wants to go back to a different page
	login.hide()
	signup.hide()
	app.show()
##############
def Book():
	# this is show were they can make there booking
	Booking.show()
	login.hide()
#################
def Dark_Mode():
	#this is for accsessiblity for the user incase they struggle to see on a white back round
	app.bg = "#434343"
	app.text_color = "#eef2f3"
#################
def Light_Mode():
	#this is for accsessiblity for the user incase they struggle to see on a Black back round
	app.bg = "#eef2f3"
	app.text_color = "#434343"
################
def Zoom():
	app.text_size = Size.value
###################
def check_date(Mydate): # found on geeks for geeks
	# initializing format
	format = "%d/%m/%Y"
 	# checking if format matches the date
	res = True
 	# using try-except to check for truth value
	try:
		res = bool(datetime.strptime(Mydate, format))
	except ValueError:
		res = False
	return res
#####################
def Conformation(): 
	#this does the math to make sure the user is charged the correct price
	# it also gets the varible ready to be show to the user
	TAdults = int(Adults.value) * 10
	TKids = int(Kids.value) * 5
	Total = TKids + TAdults
	Final.value = Total
	isValidDate = check_date(BookingDate.value) #this is where the date gets validated and make sure its in the correct format
	#
	if (isValidDate):
		#put the user inputs into varible to prep for diplay on confirm window
		FDate.value = BookingDate.value
		FTime.value = BookTime.value
		FAdults.value = Adults.value
		FKids.value = Kids.value
		Booking.hide()
		confirm.show()
	else:
		info("Date Error","must be in  a valid format dd/mm/yyyy ")
###############
def login_user():  #### TEST WITH 'or 1 = 1; -- 
	#this is where we make sure when the user login they are in the database
	global LoggedIn_ID ## variable needed to know who logged in ##
	if login1_name.value == "":#check if textbox is blank
		info("Username Incorect", "you must enter a valid Username")
	elif login1_name.value.isalpha() == False:# check the username is they have ented any special characters
		info("Login Incorrect", "No special character in Username")
	elif Password.value == "":#check if textbox is blank
		info("Password Error", "You must enter a valid Password")
	else:
		username = login1_name.value#check the database for the username
		sqlselect = "SELECT * FROM UserTbl WHERE Username = '"+username+"'"
		rows = query_database(database_file, sqlselect)
		if len(rows) == 0: ### This checks that the user was found ###
			info("Accont Error","Account not Found Please Check Username and Password")
		else:
			# check pw
			DBP = rows[0][2]
			if DBP == Password.value:
				#show info if password is found moving you onto booking
				info("Log in","You have successfully logged in")
				LoggedIn_ID = rows [0][0]
				Book()
			else:
				info("Accont Error","Account not Found Please Check Username and Password")
####################
def signup_user():
	#this is where we validate the sign in window to make sure the user has entered the value for each box
	if Uname.value == "":#check if textbox is blank
		info("Signup Error", "You must enter a valid username")
	elif Uname.value.isalpha() == False:# make sure the username is all letters
		info("Signup Error", "Your UserName must not contain any numbers or special characters")
	elif len(Uname.value) < 3 or len(Uname.value) > 20:#check Username is between 3 and 20 characters
		info("Signup Error", "Please enter a Username between 3 and 20 charaters")
		##
	elif len(Pword.value) < 5 or len(Pword.value) > 20:# check the password length
		info("Signup Error", "Your Password must be between 5 and 20 characters")
		##
	elif Fname.value == "":#check if textbox is empty
		info("Signup Error", "You must enter a First name")
	elif Fname.value.isalpha() == False:#check to make sure there are not number in first name
		info("Signup Error", "Your First Name must not contain any numbers or special characters")
		##
	elif Sname.value == "":#check if textbox is blank
		info("Signup Error", "You must enter a Surname")
	elif Sname.value.isalpha() == False:#check to make sure there are not number in Surname
		info("Signup Error", "Your Surname must not contain any numbers or special characters")
		##
	elif len(Num.value) < 11 and Num.value.isnumeric() == False:#check that the phone number is british standared length
		info("Signup Error", "You must enter a Valid phone number")
		##
	elif "@" not in Email.value and ".com" not in Email.value or ".co" not in Email.value:# check the email for a @ sign 
		info("Signup Error", "You must enter a Valid Email address For Example: Foxy@gmail.com")
	else:
		# if they are all valid it will exacute and insert them into the database
		Insert_Data_SQL = ("INSERT INTO UserTbl(Username, Password, Fname, Sname, Email, Phonenumber ) VALUES ('"+ str(Uname.value) + "', '" + str(Pword.value) + "', '" + str(Fname.value) + "', '" +str(Sname.value)+ "', '" +str(Email.value) + "', '" +str(Num.value)+ "')")
		execute_sql(database_file, Insert_Data_SQL)
		info("Success","You are now registered as:" + Uname.value)
		login.show()
		signup.hide()
##########################
def do_this():
	info("Term and conditions", "According to all known laws of aviation, there is no way a bee should be able to fly.Its wings are too small to get its fat little body off the ground.The bee, of course, flies anyway because bees don't care what humans think is impossible.Yellow, black. Yellow, black. Yellow, black. Yellow, black.Ooh, black and yellow!Let's shake it up a little.Barry! Breakfast is ready!Coming!Hang on a second.Can you believe this is happening?I can't.I'll pick you up.Looking sharp.Use the stairs, Your father paid good money for those.Sorry. I'm excited.Here's the graduate.We're very proud of you, son.A perfect report card, all B's.Very proud.Ma! I got a thing going here.You got lint on your fuzz.Three days college. I'm glad I took a day and hitchhiked around The Hive.You did come back different.Hi, Barry. Artie, growing a mustache? Looks good.Hear about Frankie?Yeah.You going to the funeral? No, I'm not going. Everybody knows, sting someone, you die.Don't waste it on a squirrel.Such a hothead.I guess he could have just gotten out of the way.I love this incorporating an amusement park into our day.That's why we don't need vacations.Boy, quite a bit of pomp under the circumstances.Well, Adam, today we are men.We are!Bee-men.Amen!Hallelujah!Students, faculty, distinguished bees,please welcome Dean Buzzwell.Welcome, New Hive City graduating class of 9:15.That concludes our ceremonies And begins your career at Honex Industries. Will we pick our job today?I heard it's just orientation.Heads up! Here we go.Keep your hands and antennas inside the tram at all times.Wonder what it'll be like?A little scary.Welcome to Honex, a division of Honesco and a part of the Hexagon Group.This is it!Wow.Wow.We know that you, as a bee, have worked your whole life to get to the point where you can work for your whole life.Honey begins when our valiant Pollen Jocks bring the nectar to The Hive.Our top-secret formula is automatically color-corrected, scent-adjusted and bubble-contoured into this soothing sweet syrup with its distinctive golden glow you know as... Honey!That girl was hotShe's my cousin!She is?Yes, we're all cousins.Right. You're right.At Honex, we constantly strive to improve every aspect of bee existence.These bees are stress-testing a new helmet technology.What do you think he makes?Not enough.Here we have our latest advancement, the Krelman.")
#########################
def Confirm_Booking():
	#inserts the user details about the booking into data base
	Insert_Data_SQL = ("INSERT INTO Bookingtbl(BookingDate, BookTime, Adults, Kids, TotalCost, UserID) VALUES ('"+ str(BookingDate.value) + "', '" + str(BookTime.value) + "', '" + str(Adults.value) + "', '" + str(Kids.value) + "', '" + str(Final.value) +"', '" +str(LoggedIn_ID)+"')")	
	execute_sql(database_file,Insert_Data_SQL)
	info("Success","You are now booked for the: " + BookingDate.value)
	confirm.hide()
	app.show()
######################################
def Exit():
	app.destroy()
##########################################
#####		Makeing windows		##########
##########################################
#this builds the main window where the user can choose to login or sign up
app = App(title="TPC Northwind Main Menu", height = 600, width=600)
login = Window(app, title="TPC Northwind login", height=400, width=500)
signup = Window(app, title ="TPC Northwind sign up", height=700, width=550)
Booking = Window(app, title ="TPC Northwind Booking", height=500, width=550, layout="grid")
confirm = Window(app, title="TPC Northwind Confirm Booking",  height=200, width=400)
#####################
signup.hide()
login.hide()
Booking.hide()
confirm.hide()
app.bg = "#eef2f3"
app.text_color = "#434343"
#################################
# build main window             #
#################################
Accsesibllity = Box(app, width="fill", align="top")
text_blank = Text(app, text="--------------------------------------------------------------------------------------------------------------------------")
text_blank = Text(app, text="Welcome to TPC Northwind")
text_blank = Text(app, text="")

#
#
user_textbox = PushButton(app, text="Login", command=Login, width=15)
Text_blank = Text(app, text="")
#
signup1 = PushButton(app, text="Sign Up", command=Signup, width=15)
#
picture = Picture(app, image="TPC.JFIF", width=400, height=250)
#
Lightmode = PushButton(Accsesibllity, text="Light Mode", command=Light_Mode, width =8,  align ="left")
Darkmode = PushButton(Accsesibllity, text="Dark Mode", command=Dark_Mode, width =8, align ="left")
Size = Slider(Accsesibllity, command=Zoom, start = 8, end=14, align="right")
#
Exit = PushButton(app, text="Exit", align="bottom", command=Exit, width=15)
############################################
##########	 login window   ################
############################################
Accsesibllity = Box(login, width="fill", align="top")
#
text_blank = Text(login, text="Welcome to TPC Northwind")
text_blank = Text(login, text="Please Please login to your account")
#
text = Text(login, text= "Enter Username")
login1_name = TextBox(login, text="")
#
text_blank = Text(login, text="")
text = Text(login, text= "Enter Password")
Password = TextBox(login, text="")
#
open_button = PushButton(login, text="log in", command=login_user) # button on app, main window
#
Back_box = Box(login, width="fill", align="bottom")
Back_button = PushButton(Back_box, text="Back",command=Back, align="right")

text_blank = Text(login, text="")
text_blank = Text(login, text="No account:\n Join us now")
signup1 = PushButton(login, text="Sign Up", command=Signup, width=15)
#
Lightmode = PushButton(Accsesibllity, text="Light Mode", command=Light_Mode,align="left",width =8)
Darkmode = PushButton(Accsesibllity, text="Dark Mode", command=Dark_Mode, align="left",width =8)
##################################
## build Sign Up window         ##
##################################
Accsesibllity = Box(signup, width="fill", align="top")
Back_box = Box(signup, width="fill", align="bottom")
#
text_blank = Text(signup, text="")
text_blank = Text(signup, text="TPC Northwind")
text_blank = Text(signup, text="")
#
text = Text(signup, text= "Enter a User name")
Uname = TextBox(signup, text="")
#
text = Text(signup, text= "Enter a Password")
Pword = TextBox(signup)
#
text = Text(signup, text= "Enter a First Name")
Fname = TextBox(signup)
#
text = Text(signup, text= "Enter a Surname")
Sname = TextBox(signup)
#
text = Text(signup, text= "Enter Phone number")
Num = TextBox(signup)
#
text = Text(signup, text= "Enter Email")
Email = TextBox(signup)
#
text_blank = Text(signup, text="")
#
Terms = CheckBox(signup, text="Agree Terms and Conditions")
Terms.when_clicked = do_this
#
Sign_button = PushButton(signup, text="Sign up",command=signup_user) # button on app, main window
#
picture = Picture(signup, image="TPC South.JPG", width=300, height = 250)

Back_button = PushButton(Back_box, text="Back", align="right" ,command=Back, width=15)
#
Lightmode = PushButton(Accsesibllity, text="Light Mode", command=Light_Mode,align="left" ,width =7)
Darkmode = PushButton(Accsesibllity, text="Dark Mode", command=Dark_Mode, align="left", width =7)
#
############################
####	Booking window	####
############################
Date_txt = Text(Booking, text="Please enter a Date:", grid=[0,0])
BookingDate = TextBox(Booking, text="", grid=[1,0])
#
Time_txt = Text(Booking, text="Please enter a Time:", grid=[0,1])
BookTime = Combo(Booking, options=["9:00", "9:30","10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30"], grid=[1,1])
#
adults = Text(Booking, text="How many adults are playing:", grid=[0,2])
#
Adults = Combo(Booking,  options=[1, 2, 3, 4], grid=[1,2])
#
kid = Text(Booking, text="How many Kids are playing:", grid=[0,3])
Kids = Combo(Booking, options=[0, 1, 2, 3, 4], grid=[1,3])
#
price = Text(Booking, text="Price for adults and children", grid=[2,0])
Adult_price = Text(Booking, text="Adult: £10 per person", grid=[2,1])
Kid_price = Text(Booking, text="Kid: £5 per person", grid=[2,2])
#
Confirm = PushButton(Booking, text="Confirm Booking", command=Conformation, grid=[1,8])
#
############################
####	Booking window	####
############################
Overview = Box(confirm, layout="grid", border = True)
Booking_confirm = Text(Overview, text="Please check that all your detail are correct", grid=[0,0], align="left")
text = Text(Overview, text="You are booked to play at:", grid=[0,1], align="left")
FTime = Text(Overview, grid=[1,1], align="left")
#
text = Text(Overview,  text="You are booked for the:", grid=[0,2], align="left")
FDate = Text(Overview, grid=[1,2], align="left")
#
text = Text(Overview, text="Adults Playing:", grid=[0,3], align="left")
FAdults = Text(Overview, grid=[1,3], align="left")
#
text = Text(Overview, text="Kids Playing:", grid=[0,4], align="left")
FKids = Text(Overview, grid=[1,4], align="left")
#
text = Text(Overview,  text="That will cost a total of: £", grid=[0,5], align="left")
Final = Text(Overview,grid=[1,5], align="left")
#
Booking_Conformation = PushButton(Overview, text="Book", command=Confirm_Booking, align="left", grid=[1,6])
#
app.display()
