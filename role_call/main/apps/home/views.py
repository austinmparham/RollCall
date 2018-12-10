from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
import face_recognition
import numpy as np
import datetime
import cv2

date = datetime.datetime.now()
def index(request):
	return render(request, "rolecall/portal.html")

def login(request):
	if request.method == "POST":
		school_length= School.objects.filter(email=request.POST['email'])
		if len(school_length) < 1:
			messages.add_message(request, messages.ERROR, "Invalid email")
			return redirect('/')
		else:
			school = School.objects.get(email=request.POST['email'])
			if bcrypt.checkpw(request.POST['password'].encode(), school.password.encode()):
				request.session['id'] = school.id
				return redirect('/home')
			else:
				messages.add_message(request, messages.ERROR, "Invalid password")
				return redirect('/')

def home(request):
	context = {
		'user': School.objects.get(id=request.session['id']),
	}
	return render(request, "rolecall/home.html", context)

def new_day(request):
	print("******* VISTED NEW DAY*********")
	user = School.objects.get(id=request.session['id'])
	children = user.children.all()
	for child in children:
		child.status = "Absent"
		child.save()
	return redirect("/new_roster")

def new_roster(request):
	date = datetime.datetime.now()
	date_today = date.strftime("%x")
	check_in_time = date.strftime("%I:%M %p")
	user = School.objects.get(id=request.session['id'])
	children = user.children.all()
	context = {
		'date_today': date_today,
		'check_in_time': check_in_time,
		'user': user,
		'children': children
	}
	return render(request,"rolecall/new_roster.html", context)

def check_in(request, id):
	this_child = Child.objects.get(id=id)
	this_child.status = "Present" #Need to add time
	this_child.save()
	return redirect("/new_roster")

def photo_check(request):
	user = School.objects.get(id=request.session['id'])
	children = user.children.all()
	check_image = face_recognition.load_image_file(request.POST['check_face'])
	check_encode = face_recognition.face_encodings(check_image)[0]
	for child in children:
		a = child.face_code[1:len(child.face_code)-1]
		a = a.split(",")
		a = np.array(a)
		a = a.astype(float)
		check_result = face_recognition.compare_faces([a], check_encode, tolerance=0.4)
		print("*****This is the result of the FACE CHECK-->",check_result)
		if check_result == [True]:
			child.status = "Present"
			child.save()
	return redirect("/new_roster")

def live_check(request):
	video_capture = cv2.VideoCapture(0)
	face_locations = []
	face_encodings = []
	process_this_frame = True

	while face_locations == []:
		ret, frame = video_capture.read()
		small_frame = cv2.resize(frame,(0,0),fx=1,fy=1)
		rgb_small_frame = small_frame[:,:,::-1]
		cv2.imshow('frame',rgb_small_frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		if process_this_frame:
			face_locations = face_recognition.face_locations(rgb_small_frame)
	print("Face has been located")
	video_capture.release()
	cv2.destroyAllWindows()
	small_frame = cv2.resize(frame,(0,0),fx=1,fy=1)
	rgb_small_frame = small_frame[:,:,::-1]
	face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)[0]
	print("Face has been encoded.")
	print(type(face_encodings),"<----THIS IS LIVE CHECK'S DATA TYPE")
	print(face_encodings)
	user = School.objects.get(id=request.session['id'])
	children = user.children.all()
	for child in children:
		if child.status == "Absent":
			if len(child.face_code) > 0: 
				print("CHECKING ",child.first_name)
				a = child.face_code[1:len(child.face_code)-1]
				a = a.split(",")
				a = np.array(a)
				a = a.astype(float)
				print(type(a),"<---THIS IS CHILD CODE DATA TYPE")
				check_result = face_recognition.compare_faces([a], face_encodings, tolerance=0.69)
				print("*****This is the result of the LIVE CHECK FOR ",child.first_name,"-->",check_result)
				if check_result == [True]:
					child.status = "Present"
					child.save()
					return redirect("/new_roster")
	return redirect("/new_roster")


def remove(request,id):
	this_child = Child.objects.get(id=id)
	this_child.status = "Absent" #Need to add time
	this_child.save()
	return redirect("/new_roster")

def back(request):
	return redirect("/home")

def submit_roster(request):
	this_school = School.objects.get(id=request.session['id'])
	Attendance.objects.create(school=this_school)
	today = Attendance.objects.filter(school=this_school).last()
	children = this_school.children.all()
	for child in children:
		if child.status != "Absent":
			today.children.add(child)
	messages.add_message(request, messages.ERROR, "*Roster submitted.*")
	return redirect('/home')

def roster_list(request):
	this_school = School.objects.get(id=request.session['id'])
	rosters = Attendance.objects.filter(school=this_school)
	context={
		'rosters': rosters,
		'school': this_school
	}
	return render(request, "rolecall/roster_list.html", context)

def view_roster(request, id):
	roster= Attendance.objects.get(id=id)
	children= roster.children.all()
	school = School.objects.get(id=request.session['id'])
	all_children= school.children.all()
	context = {
		'roster': roster,
		'children': children,
		'all_children': all_children
	}
	return render(request,"rolecall/view_roster.html", context)

def view_kids(request):
	this_school = School.objects.get(id=request.session['id'])
	children = this_school.children.all()
	context = {
		'school': this_school,
		'children': children,
	}
	return render(request,"rolecall/view_kids.html", context)

def register_child(request):
	this_school = School.objects.get(id=request.session['id'])
	parents = this_school.parents.all
	context={
		'school': this_school,
		'parents': parents
	}
	return render(request, "rolecall/register_child.html", context)

def submit_child(request):
	school= School.objects.get(id=request.session['id'])
	parent= Parent.objects.get(id=request.POST['parent'])
	# image = face_recognition.load_image_file(request.POST['face_code'])
	# try:
	# 	face_code= face_recognition.face_encodings(image)[0]
	# 	face_code = face_code.tolist()
	# 	print(face_code)
	# except:
	# 	messages.add_message(request, messages.ERROR, "No faces found in submitted picture.\n Please try again.")
	# 	return redirect("/register_child")
	Child.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],parent=parent,school=school,age=request.POST['age'],grade=request.POST['grade'],allergies=request.POST['allergies'],conditions=request.POST['conditions'],face_code="",status="Absent")
	# profile_image="/static/rolecall/css/"+request.POST['face_code'] -- "Use something like this when a full picture path is able to be used."
	return redirect("/face_code")

def face_code(request):
	school = School.objects.get(id=request.session['id'])
	child = school.children.last()
	video_capture = cv2.VideoCapture(0)
	face_locations = []
	face_encodings = []
	process_this_frame = True

	while face_locations == []:
		ret, frame = video_capture.read()
		small_frame = cv2.resize(frame,(0,0),fx=1,fy=1)
		rgb_small_frame = small_frame[:,:,::-1]
		cv2.imshow('frame',rgb_small_frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		if process_this_frame:
			face_locations = face_recognition.face_locations(rgb_small_frame)
	print("Face has been located")
	video_capture.release()
	cv2.destroyAllWindows()
	small_frame = cv2.resize(frame,(0,0),fx=1,fy=1)
	rgb_small_frame = small_frame[:,:,::-1]
	face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)[0]
	face_encodings = face_encodings.tolist()
	print("Face has been encoded.")
	print(type(face_encodings),"<----THIS IS LIVE CHECK'S DATA TYPE")
	print(face_encodings)
	child.face_code = face_encodings
	child.save()
	return redirect("/view_kids")


def logout(request):
	request.session.clear()
	return redirect('/')
