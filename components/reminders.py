from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from components.models import ComponentCheckout

def send_test_email():
    """Send a test email to verify the email functionality"""
    try:
        send_mail(
            subject='Test Email - IoT Lab Reminder System',
            message='This is a test email to verify the reminder system is working correctly.',
            from_email='dhaked.7248@gmail.com',
            recipient_list=['dhaked.7248@gmail.com'],
            fail_silently=False
        )
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Error sending test email: {str(e)}")

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
            context = {
                'component': checkout.component,
                'quantity': checkout.quantity,
                'user_name': checkout.display_name or checkout.checked_out_by.get_full_name(),
                'expected_return_date': checkout.expected_return_date,
                'days_remaining': days_until_return,
                'is_overdue': days_until_return < 0
            }
            html_message = render_to_string('components/email/return_reminder.html', context)
            plain_message = strip_tags(html_message)
            subject = f"{'OVERDUE' if days_until_return < 0 else 'REMINDER'}: Return {checkout.component.name}"
            try:
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