from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.widgets import Textarea, HiddenInput
from datetime import datetime
from django_extensions.db.fields.encrypted import EncryptedCharField


# A class to extend Django's User model with additional information
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	birthdate = models.DateField('birthdate')
	sex = models.CharField(max_length=6)
	
	def get_absolute_url(self):
		return ('profiles_profile_detail', (), { 'username': self.user.username })
	
	def __unicode__(self):
		return unicode(self.user)
	
# A class representing a 'good thing' entered by a user.
class GoodThing(models.Model):
	content = EncryptedCharField(max_length=250)
	done = models.BooleanField(default=False)
	date = models.DateTimeField('date submitted')
	author = models.ForeignKey(User)
	
	class Meta:
		ordering = ['-date']
	
	class Admin:
		list_display = ('done', 'date', 'author')
 
	def save(self):
		if not self.id:
			self.date = datetime.now()
		super(GoodThing, self).save()
	
	def dothing(self):
		if self.done:
			btn = "<div id='done_%s'><img class='btn' src='/static/checkon.png' /></div>"
		else:
			btn = "<div id='done_%s'><img class='btn' src='/static/checkoff.png' /></div>"
		return btn % (self.pk)
	
	dothing.allow_tags = True
	
	def __unicode__(self):
		return unicode('Post by %s on %s' % (self.author, self.date))
	
	

# A class to contain the life expectancy table data
class LifeExpectancy(models.Model):
	age = models.IntegerField(unique=True)
	male_yearsleft = models.DecimalField(max_digits=4, decimal_places=2, unique=True)
	female_yearsleft = models.DecimalField(max_digits=4, decimal_places=2, unique=True)
	
	def __unicode__(self):
		return unicode(self.age)

	
