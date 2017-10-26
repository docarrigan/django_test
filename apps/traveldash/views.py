# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def index(request):
	return render(request, 'traveldash/index.html')

def trips(request):

	mytrips 	= Trip.objects.filter(joined__id=request.session['id']).all()
	trips		= Trip.objects.exclude(joined__id=request.session['id'])
	user 		= Person.objects.get(id=(request.session['id']))
	context = {
		'mytrips': mytrips,
		'trips': trips,
		'users': user
		}

	return render(request, 'traveldash/trips.html', context)

def add(request):
	return render(request, 'traveldash/add.html')


def register(request):

	result = Person.objects.register(request.POST)
	
	if 'errors' in result:
		print (result)
		for i in result['errors']:
			messages.error(request, i)
		return redirect('/')
	
	else:
		print "New user registered"
		result = Person.objects.login(request.POST)
		messages.success(request, "You successfully registered")
		return redirect('/trips')

	return redirect('/')


def login(request):

	login = Person.objects.login(request.POST)

	if login['result'] == 'success':
		request.session['id'] = login['user'].id
		print "User logged in"
		messages.success(request, "You successfully logged in")
		return redirect('/trips')

	else:
		print "login errors detected"
		for err in login['errors']:
			messages.error(request, err)
		return redirect('/')


def logout(request):
	del request.session['id']
	return redirect('/')


def addtrip(request):
	trip = Trip.objects.add_trip(request.POST, request.session['id'])
	return redirect('/trips')

def jointrip(request, trip_id):
	trip = Trip.objects.get(id=trip_id)
	user = Person.objects.get(id=request.session['id'])
	trip.joined.add(user)
	print trip.joined.all()
	print user.joined_trips.all()
	return redirect('/trips')


