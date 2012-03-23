from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import Textarea, RadioSelect, HiddenInput
from django.forms.extras.widgets import SelectDateWidget
from goodthings.models import UserProfile, GoodThing
import datetime

SEX_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
YEARS = (range(2010, 1910, -1))

# A form class that allows users to edit user information from their profile pages by linking the django-profiles app and the built-in user app.

class UserProfileForm(ModelForm):
 
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            # self.fields['first_name'].initial = self.instance.user.first_name
            # self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass
 
    email = forms.EmailField(label="Email",help_text='')
 
    class Meta:
    	model = UserProfile
    	exclude = ('user',)
    	#fields = {'birthdate', 'sex',}
    	widgets = {
      	'sex': RadioSelect(choices=SEX_CHOICES),
      	'birthdate' : SelectDateWidget(years=YEARS, attrs={'class': 'span3'}),
      }        
 
    def save(self, *args, **kwargs):
        """
        Update the primary email address on the related User object as well.
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.save()
        profile = super(UserProfileForm, self).save(*args,**kwargs)
        return profile

# A form linked to the 'good thing' model.
class GoodThingForm(ModelForm):
	class Meta:
		model = GoodThing
		#fields = {'content', 'date', 'author', 'done',}
		widgets = {
				'content': Textarea(attrs={'rows':4,}),
				'date': HiddenInput(),
				'author': HiddenInput(),
				'done': HiddenInput(),
		}
				