from django.core.management.base import BaseCommand
from django.utils import timezone
import threading
import schedule
import time
from components.models import ComponentCheckout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_reminder_emails():
    today = timezone.now().date()
    
    # Get all active checkouts
    active_checkouts = ComponentCheckout.objects.filter(
        actual_return_date__isnull=True  # Only get unreturned items
    ).select_related('component', 'checked_out_by')
    
    for checkout in active_checkouts:
        days_until_return = (checkout.expected_return_date - today).days
        
        # Send reminder if due in 2 days or overdue
        if days_until_return <= 2:
            # Prepare email context
            context = {
                'component': checkout.component,
                'quantity': checkout.quantity,
                'user_name': checkout.display_name or checkout.checked_out_by.get_full_name(),
                'expected_return_date': checkout.expected_return_date,
                'days_remaining': days_until_return,
                'is_overdue': days_until_return < 0
            }
            
            # Render email template
            html_message = render_to_string('components/email/return_reminder.html', context)
            plain_message = strip_tags(html_message)
            
            # Set email subject based on whether it's overdue
            subject = f"{'OVERDUE' if days_until_return < 0 else 'REMINDER'}: Return {checkout.component.name}"
            
            try:
                # Send email
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email='dhaked.7248@gmail.com',
                    recipient_list=[checkout.user_email],
                    html_message=html_message,
                    fail_silently=False
                )
                print(f"Sent reminder email for {checkout.component.name} to {checkout.user_email}")
            except Exception as e:
                print(f"Error sending email for {checkout.component.name}: {str(e)}")

def run_scheduler():
    # Schedule the reminder check to run daily at 9:40 PM
    schedule.every().day.at("22:00").do(send_reminder_emails)
    
    print("Reminder scheduler started. Will check for due returns daily at 10:00 PM.")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

class Command(BaseCommand):
    help = 'Starts the component return reminder scheduler'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting reminder scheduler...'))
        
        # Start the scheduler in a separate thread
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        self.stdout.write(self.style.SUCCESS('Reminder scheduler is running in the background')) 