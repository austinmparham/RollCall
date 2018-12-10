from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class Account(models.Model):
	company_name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	email = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	def __repr__(self):
		return "<Account object: {}, {}, {}, {}>".format(self.id, self.company_name, self.username, self.password)

class School(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	state = models.CharField(max_length=255)
	account = models.ForeignKey(Account, related_name="schools")
	def __repr__(self):
		return "<School object: {}, {}, {}, {}>".format(self.id, self.name, self.username, self.password)

class Parent(models.Model):
	first_name= models.CharField(max_length=255)
	last_name= models.CharField(max_length=255)
	phone_number = models.IntegerField()
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	state = models.CharField(max_length=255)
	school = models.ForeignKey(School, related_name="parents")
	def __repr__(self):
		return "<Parent object: {}, {}, {}, {}, {}>".format(self.id, self.first_name, self.last_name, self.email, self.password)

class Child(models.Model):
	first_name= models.CharField(max_length=255)
	last_name= models.CharField(max_length=255)
	parent = models.ForeignKey(Parent, related_name="children")
	school = models.ForeignKey(School, related_name="children")
	age = models.IntegerField()
	grade = models.CharField(max_length=30)
	allergies = models.CharField(max_length=255)
	conditions = models.CharField(max_length=255)
	profile_image = models.TextField()
	face_code = models.TextField()
	status = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __repr__(self):
		return "<Child object: {}, {}, {}, {}, {}>".format(self.id, self.first_name, self.last_name, self.grade, self.profile_image)

class Attendance(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	children = models.ManyToManyField(Child, related_name="date_attended")
	school = models.ForeignKey(School, related_name="attendances")




