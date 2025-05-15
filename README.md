# IoT Lab Manager

A Django-based web application for managing IoT lab components, equipment, and student checkouts.

## Features

- User authentication and authorization
- Component and equipment management
- Checkout and return tracking
- Automatic email reminders for overdue items
- Daily email notifications at 10:20 PM
- Email notifications for component returns
- Admin dashboard for managing users and inventory

## Prerequisites

- Python 3.8 or higher
- Django 4.2 or higher
- PostgreSQL database
- SMTP server for email notifications

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd lab-manager
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/lab_manager
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Email Configuration

The application uses Gmail SMTP for sending emails. To set up email notifications:

1. Enable 2-factor authentication in your Gmail account
2. Generate an App Password:
   - Go to Google Account Settings > Security
   - Under "2-Step Verification", click on "App passwords"
   - Generate a new app password for "Mail"
3. Update the `.env` file with your email credentials:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Email Reminder System

The application includes an automated email reminder system that:
- Sends daily reminders at 10:20 PM
- Notifies users about components due for return
- Sends reminders for overdue items
- Includes component details and return instructions in emails

To test the email functionality:
```bash
python manage.py test_email
```

## Usage

1. Access the admin interface at `/admin` to:
   - Manage users and permissions
   - Add/edit components and equipment
   - View checkout history

2. Regular users can:
   - Browse available components
   - Check out components
   - Return components
   - View their checkout history
   - Receive email notifications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django Documentation
- Bootstrap Documentation
- AWS Documentation
- All contributors and maintainers

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Roadmap

- [ ] Add API endpoints for mobile app integration
- [ ] Implement barcode/QR code scanning
- [ ] Add data export functionality
- [ ] Implement advanced reporting features
- [ ] Add email notifications for maintenance schedules
- [ ] Multi-language support
- [ ] API documentation
- [ ] Performance optimization
- [ ] Database migration to PostgreSQL (for larger scale deployment) 
