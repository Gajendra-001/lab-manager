from django.apps import AppConfig

class ComponentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'components'

    def ready(self):
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from django_apscheduler.jobstores import DjangoJobStore
            from django.utils import timezone
            from django.core.mail import send_mail
            from django.template.loader import render_to_string
            from django.utils.html import strip_tags
            from components.models import ComponentCheckout

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
                                from_email='dhaked1415@gmail.com',
                                recipient_list=[checkout.user_email],
                                html_message=html_message,
                                fail_silently=False
                            )
                            print(f"Sent reminder email for {checkout.component.name} to {checkout.user_email}")
                        except Exception as e:
                            print(f"Error sending email for {checkout.component.name}: {str(e)}")

            scheduler = BackgroundScheduler()
            scheduler.add_jobstore(DjangoJobStore(), "default")
            
            # Reference the function by string path
            scheduler.add_job(
                'components.reminders:send_reminder_emails',
                'cron',
                hour=9,
                minute=00,
                id='send_reminder_emails',
                replace_existing=True,
            )
            
            scheduler.start()
            print("Reminder scheduler started. Will check for due returns daily at 9:00 AM.")
        except Exception as e:
            print(f"Error starting scheduler: {str(e)}")
