from django.core.management.base import BaseCommand
from components.reminders import send_test_email

class Command(BaseCommand):
    help = 'Test the email sending functionality'

    def handle(self, *args, **options):
        self.stdout.write('Testing email sending...')
        send_test_email()