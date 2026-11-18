from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  password_confirm = forms.CharField(widget=forms.PasswordInput)
  role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
  contact_number = forms.CharField(max_length=20, required=False)

  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'password']

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError(
          'This email address is already registered.'
      )
    return email

  def clean(self):
    cleaned_data = super().clean()
    pwd = cleaned_data.get('password')
    pwd_confirm = cleaned_data.get('password_confirm')
    if pwd and pwd_confirm and pwd != pwd_confirm:
      self.add_error('password_confirm', 'Passwords do not match.')
    return cleaned_data


class UserProfileUpdateForm(forms.ModelForm):

  class Meta:
    model = UserProfile
    fields = ['contact_number', 'profile_photo']