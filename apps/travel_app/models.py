from __future__ import unicode_literals
import datetime, bcrypt
from dateutil.relativedelta import relativedelta
from django.db import models


# Create your models here.
class UserManager(models.Manager):
	def validate_login(self, data):
		users = User.objects.filter(username=data['username'])
		if len(users)<1:
			return 'username does not match any records'
		else:
			user = User.objects.get(username=data['username'])
			if bcrypt.hashpw(data['password'].encode(), user.password.encode()) == user.password.encode():
				print user
				return user
			return'incorrect password'
				

	def validate_register(self, data):
		errors = []
		if (len(data['name'])<3) or (not data['name'].isalpha()):
			errors.append("Names must be at least 3 characters and only letters")
		if len(data['username'])<3:
			errors.append("Names must be at least 3 characters")
		try:
			User.objects.get(username=data['username'])
			errors.append("username already registered")
		except:
			pass
		if len(data['password'])<8:
			errors.append("Password must be greater than 8 characters")
		if data['password']!=data['confirm_password']:
			errors.append("Passwords must match")
		if len(errors)>0:
			print errors
			return errors
		hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
		result = User.objects.create(name=data['name'], username=data['username'], password=hashed)
		print result
		return result       

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=28)
	created_at = models.DateTimeField(auto_now_add=True)
	objects = UserManager()

class TripManager(models.Manager):
	def validate_trip(self, data, session):
		errors = []
		print data
		print data['start_date']
		print type(data['start_date'])

		if len(data['destination'])<1:
			print 'destination was empty'
			errors.append("destination cannot be empty")
		if len(data['description'])<1:
			print 'description emtpy'
			errors.append("Description cannot be empty")
		if data['start_date']=='' or data['end_date']=='':
			errors.append("Dates cannot be empty")
		else:
			start = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d')
			end = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d')
			today = datetime.datetime.today()
			if start < today:
				errors.append('start date cannot be in the past')
			if start > end:
				errors.append('start date cannot be after end date')
		if len(errors)>0:
			print errors
			return errors
		result = Trip.objects.create(destination=data['destination'], description=data['description'], start_date=data['start_date'], end_date=data['end_date'], created_by=User.objects.get(id=session['id']))
		print result
		return result



class Trip(models.Model):
	destination = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	start_date = models.DateField()
	end_date = models.DateField()
	created_by = models.ForeignKey(User, related_name='trips_created')
	buddies = models.ManyToManyField(User, related_name='joined_trips')
	objects = TripManager()



