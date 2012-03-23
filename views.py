from django import forms
from django.contrib.auth import authenticate, login, urls
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from goodthings.models import UserProfile, LifeExpectancy
from whatgood.forms import GoodThingForm
from goodthings.models import GoodThing
from datetime import date, timedelta, datetime
from django.template import RequestContext
import registration


@login_required
def todaysgood(request):
	"""Get the user's data, list recent good things, and accept newly created good things."""
	#get basic information about the user
	username = request.user
	currentuser = UserProfile.objects.get(user=username)
	#get the user's birthdate	
	birthdate = currentuser.birthdate
	
	#if birthdate is set to default, redirect to profile edit page
	if birthdate == date(1901, 01, 01):
		next = '/todaysgood/'
		return HttpResponseRedirect('/profiles/edit/')
	
	if request.method == 'POST': 	
		newgoodthingform = GoodThingForm(request.POST) 
		newgoodthingform.date = date.today()
		#newgoodthingform.author = request.user
		if newgoodthingform.is_valid():
			newgoodthingform.save()
			return HttpResponseRedirect('/todaysgood/')
	else: 
		newgoodthingform = GoodThingForm(
			initial={'author': request.user, 'date': date.today(), 'done': False }
		) 				

	#get today's date
	today = date.today()
	#calculate how many days the user has lived.
	agetimedelta = today - birthdate
	dayslived = agetimedelta.days
	#calculate the user's current age
	age = today.year - birthdate.year
	if date(2011, today.month, today.day) < date(2011, birthdate.month, birthdate.day):
		age = age - 1
	#caluculate the user's life expectancy
	lifetable = LifeExpectancy.objects.get(age=age)
	if currentuser.sex == 'Male':
		yearsleft = lifetable.male_yearsleft
	if currentuser.sex == 'Female':
		yearsleft = lifetable.female_yearsleft
	#convert years left to days left. Precision within a few days is not so important, so do it the easy way.
	roundedyearsleft = int(yearsleft)
	daysleft = int( 365.24 * float(yearsleft))
	#convert this to timedelta format
	daysleftdelta = timedelta(daysleft)
	#calculate a death date
	deathdate = today + daysleftdelta
	#calculate the percentage of life completed
	lifespan = deathdate - birthdate
	
	def total_seconds(td): 
		return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6
	
	lifecompleted = ( total_seconds(agetimedelta) / total_seconds(lifespan) )
	lifecompletedpercent = 100 * round(lifecompleted, 3)
	lifecompletedpixels = round(lifecompleted * 400)	
	
	goodthingslist = GoodThing.objects.filter(author__exact=username).filter(date__day=today.day).order_by('-date')[:6]
	
	return render_to_response('todaysgood2.html', {'username': username, 'birthdate': birthdate, 'age': age, 'dayslived': dayslived, 'roundedyearsleft': roundedyearsleft, 'daysleft': daysleft, 'deathdate': deathdate, 'lifecompletedpercent': lifecompletedpercent, 'lifecompletedpixels': lifecompletedpixels, 'newgoodthingform': newgoodthingform, 'goodthingslist': goodthingslist}, context_instance=RequestContext(request))


def done(request, action, pk):
	"""Toggle a goodthing's 'Done' status on or off"""
	goodthing = GoodThing.objects.get(pk=pk)
	
	if action == "on":
		goodthing.done = True
	elif action == "off":
		goodthing.done = False
	
	goodthing.save()
	nexturl = request.session['last_visited']
	return HttpResponseRedirect(nexturl)

def about(request):
	"""Display the about page."""
	return render_to_response('about.html')

def landing_page(request):
	"""Display the landing page."""
	return render_to_response('landing.html')

@login_required
def show_allthethings(request):
	"""Display all good things for a given user."""
	
	username = request.user
	today = date.today()

	allgoodthingslist = GoodThing.objects.filter(author__exact=username).order_by('-date')
	number_of_things = len(allgoodthingslist)
	
	return render_to_response('allthings.html', {'username': username, 'allgoodthingslist': allgoodthingslist, 'number_of_things': number_of_things}, context_instance=RequestContext(request))




			