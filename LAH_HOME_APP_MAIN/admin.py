from django.contrib import admin
from .models import JournalEntry, Contact, Settings


admin.site.register([JournalEntry, Contact, Settings])
