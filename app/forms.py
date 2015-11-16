from django import forms

class LoginForm(forms.Form):
	"""Fields for the login form"""
	username = forms.CharField( max_length=100, widget=forms.TextInput(attrs={'class':'validate','type':'text', 'id' : 'icon_prefix'}))
	password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':'mdl-textfield__input'}))

class RegistrationForm(forms.Form):
	"""Fields for the registration form"""
	username = forms.CharField( max_length=100, widget=forms.TextInput(attrs={'class':'mdl-textfield__input'}))
	email = forms.EmailField( max_length=100, widget=forms.EmailInput(attrs={'class':'mdl-textfield__input'}))
	password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':'mdl-textfield__input' }))
		