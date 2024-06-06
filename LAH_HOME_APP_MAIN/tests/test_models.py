from django.test import TestCase
from LAH_USER.models import User
from LAH_HOME_APP_MAIN.models import JournalEntry, Contact

class JournalEntryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')

    def test_create_journal_entry(self):
        entry = JournalEntry.objects.create(
            title='My Journal Entry',
            content='This is my journal entry.',
            user=self.user
        )
        self.assertEqual(entry.title, 'My Journal Entry')
        self.assertEqual(entry.content, 'This is my journal entry.')
        self.assertEqual(entry.user, self.user)

    def test_create_journal_entry_missing_fields(self):
        with self.assertRaises(ValidationError):
            entry = JournalEntry.objects.create(user=self.user)

    def test_user_journal_entries_relationship(self):
        entry1 = JournalEntry.objects.create(title='Entry 1', content='Content 1', user=self.user)
        entry2 = JournalEntry.objects.create(title='Entry 2', content='Content 2', user=self.user)
        self.assertEqual(list(self.user.journal_entries.all()), [entry1, entry2])

class ContactModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')

    def test_create_contact(self):
        contact = Contact.objects.create(
            name='John Doe',
            email='john@example.com',
            user=self.user
        )
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.email, 'john@example.com')
        self.assertEqual(contact.user, self.user)

    def test_create_contact_invalid_email(self):
        with self.assertRaises(ValidationError):
            contact = Contact.objects.create(name='John Doe', email='invalid_email', user=self.user)

    def test_user_contacts_relationship(self):
        contact1 = Contact.objects.create(name='John Doe', email='john@example.com', user=self.user)
        contact2 = Contact.objects.create(name='Jane Doe', email='jane@example.com', user=self.user)
        self.assertEqual(list(self.user.contacts.all()), [contact1, contact2])
