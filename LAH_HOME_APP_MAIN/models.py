from django.db import models
from LAH_USER.models import User

class JournalEntry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')

# models.py
from django.db import models

class Settings(models.Model):
    telegram_enabled = models.BooleanField(default=False)
    discord_enabled = models.BooleanField(default=False)
    facebook_enabled = models.BooleanField(default=False)
    computer_enabled = models.BooleanField(default=False)
    # Add other integrations as needed

    rh_access_token = models.CharField(max_length=255, blank=True, null=True)
    fb_email = models.CharField(max_length=255, blank=True, null=True)
    fb_pass = models.CharField(max_length=255, blank=True, null=True)
    dc_email = models.CharField(max_length=255, blank=True, null=True)
    dc_pass = models.CharField(max_length=255, blank=True, null=True)
    groq_api_key = models.CharField(max_length=255, blank=True, null=True)
    text_sid = models.CharField(max_length=255, blank=True, null=True)
    text_username = models.CharField(max_length=255, blank=True, null=True)
    text_csrf = models.CharField(max_length=255, blank=True, null=True)
    # Add other environment variables as needed