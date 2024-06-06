from django.test import TestCase, Client
from django.urls import reverse
from LAH_USER.models import User
from LAH_HOME_APP_MAIN.models import JournalEntry, Contact

class JournalEntryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_journal_entry_list_view(self):
        entry1 = JournalEntry.objects.create(title='Entry 1', content='Content 1', user=self.user)
        entry2 = JournalEntry.objects.create(title='Entry 2', content='Content 2', user=self.user)
        response = self.client.get(reverse('journal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journal_entry_list.html')
        self.assertContains(response, 'Entry 1')
        self.assertContains(response, 'Entry 2')

    def test_create_journal_entry(self):
        response = self.client.post(reverse('journal-create'), {
            'title': 'New Entry',
            'content': 'New Content'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(JournalEntry.objects.count(), 1)
        entry = JournalEntry.objects.first()
        self.assertEqual(entry.title, 'New Entry')
        self.assertEqual(entry.content, 'New Content')
        self.assertEqual(entry.user, self.user)

    def test_update_journal_entry(self):
        entry = JournalEntry.objects.create(title='Entry', content='Content', user=self.user)
        response = self.client.post(reverse('journal-update', args=[entry.id]), {
            'title': 'Updated Entry',
            'content': 'Updated Content'
        })
        self.assertEqual(response.status_code, 302)
        entry.refresh_from_db()
        self.assertEqual(entry.title, 'Updated Entry')
        self.assertEqual(entry.content, 'Updated Content')

    def test_delete_journal_entry(self):
        entry = JournalEntry.objects.create(title='Entry', content='Content', user=self.user)
        response = self.client.post(reverse('journal-delete', args=[entry.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(JournalEntry.objects.count(), 0)

class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_contact_list_view(self):
        contact1 = Contact.objects.create(name='John Doe', email='john@example.com', user=self.user)
        contact2 = Contact.objects.create(name='Jane Doe', email='jane@example.com', user=self.user)
        response = self.client.get(reverse('contact-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_list.html')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Jane Doe')

    def test_create_contact(self):
        response = self.client.post(reverse('contact-create'), {
            'name': 'New Contact',
            'email': 'new@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.name, 'New Contact')
        self.assertEqual(contact.email, 'new@example.com')
        self.assertEqual(contact.user, self.user)

    def test_update_contact(self):
        contact = Contact.objects.create(name='Contact', email='contact@example.com', user=self.user)
        response = self.client.post(reverse('contact-update', args=[contact.id]), {
            'name': 'Updated Contact',
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 302)
        contact.refresh_from_db()
        self.assertEqual(contact.name, 'Updated Contact')
        self.assertEqual(contact.email, 'updated@example.com')

    def test_delete_contact(self):
        contact = Contact.objects.create(name='Contact', email='contact@example.com', user=self.user)
        response = self.client.post(reverse('contact-delete', args=[contact.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.count(), 0)
