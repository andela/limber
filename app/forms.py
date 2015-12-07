from django import forms

class LoginForm(forms.Form):
	"""Fields for the login form"""
	email = forms.EmailField( max_length=100, widget=forms.EmailInput(attrs={'class':'input_field'}))
	password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':'input_field'}))

class RegistrationForm(forms.Form):
	"""Fields for the registration form"""
	username = forms.CharField( max_length=100, widget=forms.TextInput(attrs={'class':'input_field'}))
	email = forms.EmailField( max_length=100, widget=forms.EmailInput(attrs={'class':'input_field'}))
	password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':'input_field' }))
