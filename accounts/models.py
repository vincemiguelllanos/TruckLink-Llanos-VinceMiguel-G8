from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
  ROLE_CHOICES = (
      ('admin', 'Administrator'),
      ('dispatcher', 'Fleet Dispatcher'),
      ('driver', 'Truck Driver'),
      ('client', 'Client / Cargo Owner'),
  )

  user = models.OneToOneField(
      User, on_delete=models.CASCADE, related_name='profile'
  )
  role = models.CharField(
      max_length=20, choices=ROLE_CHOICES, default='client'
  )
  contact_number = models.CharField(max_length=20, blank=True, null=True)
  profile_photo = models.ImageField(
      upload_to='profiles/', blank=True, null=True
  )

  def __str__(self):
    return f'{self.user.username} ({self.get_role_display()})'