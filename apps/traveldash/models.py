# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt
from datetime import datetime

class PersonManager(models.Manager):

	def login(self, form_data):
	
		errors = []

		try:

			user = Person.objects.get(username = form_data['username'])
			print user.username
			
			if bcrypt.checkpw(form_data['password'].encode(), user.password.encode()):
				print "in the success user/pass"
				return {'result': 'success', 'user': user}
			
			else:
				errors.append("Invalid login credentials")
				print bcrypt.checkpw(form_data['password'].encode(), user.password.encode())
				print user.password
				print "in the invalid check"
				return {'result': 'fail', 'errors': errors}

		except:
			print "in the username error check"
			errors.append("No account associated with that username")
			return {'result': 'fail', 'errors': errors}


	def register(self, form_data):

		errors=[]

		if len(form_data['name']) < 3:
			errors.append("The first name must be at least three characters")
		
		if len(form_data['username']) < 3:
			errors.append("The last name must be at least three characters")

		if len(form_data['password']) < 8:
			errors.append("The password must be at least two characters")

		if form_data['password'] != form_data['confirm_password']:
			errors.append("The passwords do not match")

		try:
			user = Person.objects.get(username = form_data['username'])
			errors.append("Username already in use")
		except:
			pass

		if errors:
			print "Registration form errors detected"
			return {'errors':errors}
		else:
			print "No errors in registration form"
			person = Person.objects.create(\
				name = form_data['name'],\
				username = form_data['username'],\
				password = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
				)
			print person.id
			return {'success':person}


class Person(models.Model):
	name			= models.CharField(max_length=100)
	username		= models.CharField(max_length=100)
	password		= models.CharField(max_length=255)
	created_at		= models.DateTimeField(auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)
	objects			= PersonManager()




class TripManager(models.Manager):

	def add_trip(self, form_data, owner_id):
		
		errors = []

		#no blank entries
		if len(form_data['destination']) < 1 \
		or len(form_data['description']) < 1 \
		or len(form_data['start']) < 1 \
		or len(form_data['end']) < 1:
			print "Blank fields detected"
			errors.append("Fill in all fields")


		#start not after end


		#end not before start
		
		if errors:
			return {'errors':errors}
			return redirect('/add')

		else: 
			trip = Trip.objects.create(\
				destination = form_data['destination'], \
				description = form_data['description'], \
				start = form_data['start'], \
				end = form_data['end'], \
				owner = Person.objects.get(id = owner_id)
				)
			trip.joined.add(owner_id)
			return {'success':trip}

class Trip(models.Model):
	destination		= models.CharField(max_length=55)
	description		= models.CharField(max_length=255)
	start			= models.DateTimeField()
	end				= models.DateTimeField()
	owner			= models.ForeignKey(Person, related_name="created_trips")
	joined			= models.ManyToManyField(Person, related_name="joined_trips")
	created_at		= models.DateTimeField(auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)
	objects			= TripManager()