from django import forms
from .models import JournalEntry, Contact, Settings

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'user']
        
class IntegrationSettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = [
            'telegram_enabled', 'discord_enabled', 'facebook_enabled', 'computer_enabled',
            'rh_access_token', 'fb_email', 'fb_pass', 'dc_email', 'dc_pass', 'groq_api_key',
            'text_sid', 'text_username', 'text_csrf'
        ]