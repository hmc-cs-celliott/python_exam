from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, UserManager, Trip, TripManager
from django.db.models import Count, Prefetch
import time
import datetime


def index(request):
	#listy = User.objects.all()
	#for item in listy:
	#	item.delete()
	if 'id' in request.session and 'name' in request.session:
		return redirect('/travels')
	else:
		return render(request, 'travel_app/homepage.html')

def login_attempt(request):
	valid = User.objects.validate_login(request.POST)
	print valid
	if isinstance(valid, basestring):
		messages.add_message(request, messages.ERROR, valid)
		print messages
		return redirect('/')
	else:
		request.session['id']=valid.id
		request.session['name']=valid.name
		return redirect('/travels')

def register_attempt(request):
	valid = User.objects.validate_register(request.POST)
	if isinstance(valid, list):
		for item in valid:
			messages.add_message(request, messages.ERROR, item)
		return redirect('/')
	else:
		request.session['id']=valid.id
		request.session['name']=valid.name
		return redirect('/travels')

def travels(request):
	#listy = Book.objects.all()
	#for item in listy:
	#	item.delete()
	#listy = Author.objects.all()
	#for item in listy:
	#	item.delete()
	context = {
		'my_trips':Trip.objects.filter(created_by__id=request.session['id'])|Trip.objects.filter(buddies__id=request.session['id']),
		'other_trips':Trip.objects.exclude(created_by__id=request.session['id']).exclude(buddies__id=request.session['id']).select_related('created_by'),
	}
	return render(request, 'travel_app/travels.html', context)




def trip(request, trip_id): #individual trip page
	context ={
		'trip': Trip.objects.filter(id=trip_id).prefetch_related('buddies')[0],
	}
	return render(request, 'travel_app/trip.html', context)


def join_trip(request, trip_id): #attempt to join a trip
	trip = Trip.objects.get(id=trip_id)
	user = User.objects.get(id=request.session['id'])
	trip.buddies.add(user)
	return redirect('/')


def add_trip(request): #serve the form to add a trip
	return render(request, 'travel_app/add_trip.html')

def add_attempt(request): #form has been submitted, validate the trip
	result = Trip.objects.validate_trip(request.POST, request.session)
	if isinstance(result, list):
		for item in result:
			messages.add_message(request, messages.ERROR, item)
		return redirect('/add_trip')
	return redirect('/travels')


def logout(request):
	request.session.pop('id')
	request.session.pop('name')
	return redirect('/')














