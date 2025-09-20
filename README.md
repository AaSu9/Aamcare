# AamCare - Maternal Health Support System

A Django web application designed to reduce infant and maternal mortality in rural Nepal by providing personalized health support, guidance, and digital care for pregnant women and new mothers.

## Features

### For Pregnant Women
- **Registration & Profile Management**: Create personalized profiles with pregnancy details
- **Diet Plans**: Access trimester-specific nutrition guidance
- **Individual Vaccination Tracking**: Track personal vaccination status (Tdap, Influenza, COVID-19)
- **Vaccination Schedule**: Get timely reminders and information about essential vaccinations
- **Exercise Guidance**: Safe pregnancy exercise routines and tips
- **Health Progress Tracking**: Submit and monitor monthly checkup progress
- **Mental Health Support**: Emotional well-being resources

### For New Mothers
- **Postpartum Recovery**: Exercise and recovery guidance
- **Breastfeeding Support**: Nutrition and technique guidance
- **Baby Vaccination Tracking**: Track baby's vaccination schedule (Birth to 12 months)
- **Mental Health Resources**: Postpartum emotional support
- **Recovery Progress Tracking**: Monitor postpartum health progress

## Tech Stack

- **Backend**: Python Django
- **Frontend**: HTML + CSS + Bootstrap 5
- **Database**: SQLite
- **Authentication**: Django's built-in user system

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone or download the project**
   ```bash
   # If you have the project files, navigate to the project directory
   cd AamCare
   ```

2. **Install dependencies**
   ```bash
   pip install django
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Setup sample data**
   ```bash
   python manage.py setup_sample_data
   ```

5. **Create admin user (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
     - Username: admin
     - Password: admin123

## Usage Guide

### For Users

1. **Home Page**: Visit the homepage to learn about AamCare and choose your user type
2. **Registration**: 
   - Pregnant women: Click "Register as Pregnant Woman"
   - New mothers: Click "Register as New Mother"
3. **Dashboard**: After registration, access your personalized dashboard
4. **Health Tracking**: Submit monthly checkup progress
5. **Content Access**: Browse diet plans, exercise guidance, and health information

### For Administrators

1. **Admin Access**: Login at http://127.0.0.1:8000/admin/
2. **User Management**: View and manage user profiles
3. **Content Management**: Add, edit, or remove health information content
4. **Progress Monitoring**: View user checkup submissions

## Project Structure

```
AamCare/
├── aamcare/                 # Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI configuration
├── core/                   # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── forms.py            # Form definitions
│   ├── urls.py             # App URL routing
│   ├── admin.py            # Admin panel configuration
│   └── templates/core/     # HTML templates
├── manage.py               # Django management script
└── README.md               # This file
```

## Models

- **PregnantWomanProfile**: User profile for pregnant women
- **NewMotherProfile**: User profile for new mothers
- **CheckupProgress**: Health progress tracking
- **VaccinationRecord**: Individual vaccination tracking and status
- **InfoContent**: Health information articles

## Admin Credentials

- **Username**: admin
- **Password**: admin123
- **Email**: admin@aamcare.com

## Development

### Adding New Content

1. Access the admin panel
2. Navigate to "Info contents"
3. Add new content with appropriate category

### Customizing Styles

Edit the CSS in `core/templates/core/base.html` to modify the application's appearance.

### Database Changes

If you modify models:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Features for Hackathon Demo

✅ **Complete User Registration System**
✅ **Personalized Dashboards**
✅ **Individual Vaccination Tracking**
✅ **Health Progress Tracking**
✅ **Content Management System**
✅ **Responsive Design**
✅ **Admin Panel**
✅ **Sample Data**

## Contributing

This is a hackathon project demonstrating maternal health support technology. For production use, additional security measures, testing, and deployment configurations would be needed.

## License

This project is created for educational and demonstration purposes.

---

**AamCare** - Supporting maternal and infant health in rural Nepal through digital care and guidance. 