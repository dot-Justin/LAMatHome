from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import JournalEntry, Contact, Settings
from .forms import IntegrationSettingsForm

def base(request):
    return render(request, 'base.html')

class JournalEntryListView(ListView):
    model = JournalEntry
    template_name = 'journal_entries/list.html'

class ContactListView(ListView):
    model = Contact
    template_name = 'contacts/list.html'


def settings_view(request):
    if request.method == 'POST':
        form = IntegrationSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:settings')
    else:
        form = IntegrationSettingsForm()
    return render(request, 'settings.html', {'form': form})