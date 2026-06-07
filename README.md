Django-Chat Application

A real-time messaging application built with Django, Django Channels, and WebSocket technology. This application allows users to create chat rooms, exchange messages and images in real-time with other connected users.

Table of Contents

- Features
- Project Structure
- Technology Stack
- Installation
- Configuration
- Usage
- Database Models
- API Endpoints
- WebSocket Implementation
- Development

Features

- User Authentication: Register and login with username/email or Google OAuth
- Chat Rooms: Create and manage public chat rooms
- Real-time Messaging: Send text messages instantly using WebSockets
- Image Sharing: Share images in chat rooms with base64 encoding
- Room Management: Delete rooms (creator only)
- Message History: View previous messages with timestamps
- Pagination: Browse rooms with pagination support
- User Sessions: Track message authors and timestamps
- Responsive Design: Mobile and desktop friendly interface

Project Structure

```
Django-chat/
├── chatApp/                          # Main project directory
│   ├── manage.py                    # Django management script
│   ├── chatApp/
│   │   ├── settings.py              # Project configuration
│   │   ├── urls.py                  # Main URL routing
│   │   ├── wsgi.py                  # WSGI configuration
│   │   └── asgi.py                  # ASGI configuration (WebSocket)
│   ├── chat/                         # Chat application
│   │   ├── models.py                # Room and Message models
│   │   ├── views.py                 # Chat views
│   │   ├── urls.py                  # Chat URL routes
│   │   ├── forms.py                 # Room creation form
│   │   ├── consumers.py             # WebSocket consumer
│   │   └── templates/chat/
│   │       ├── home.html            # Room listing and creation
│   │       ├── room.html            # Chat room interface
│   │       └── delete_room.html     # Room deletion confirmation
│   ├── authentication/              # Authentication application
│   │   ├── models.py                # User models
│   │   ├── views.py                 # Login and signup views
│   │   ├── forms.py                 # SignUp form
│   │   └── templates/authentication/
│   │       ├── index.html           # Login page
│   │       └── signup.html          # Registration page
│   ├── templates/                   # Base templates
│   │   ├── base.html                # Base template
│   │   ├── navbar.html              # Navigation bar
│   │   ├── google_login.html        # Google OAuth button
│   │   └── socialaccount/
│   │       └── login.html           # Social login template
│   ├── static/                      # Static files
│   │   ├── app.css                  # Main stylesheet
│   │   ├── js/chat/
│   │   │   ├── main.js              # Chat room WebSocket handler
│   │   │   ├── signin.js            # Login page script
│   │   │   └── signup.js            # Signup page script
│   │   └── favicon/
│   └── db.sqlite3                   # SQLite database
└── requirements.txt                 # Python dependencies
```

Technology Stack

Backend:
- Django 5.0.3 - Web framework
- Django Channels 4.0.0 - WebSocket support
- Django REST Framework - API development
- Redis 5.0.3 - Message broker for WebSocket
- SQLite - Database

Frontend:
- HTML5 - Markup
- CSS3 - Styling
- JavaScript (Vanilla) - Interactivity
- Toastify - Notifications

Authentication:
- Django Allauth - User authentication and OAuth
- Google OAuth 2.0 - Social login
- Django JWT - Token authentication

Additional Libraries:
- Pillow 10.2.0 - Image processing
- python-dotenv - Environment variables
- Werkzeug - WSGI utilities

Installation

Prerequisites:
- Python 3.10+
- pip (Python package installer)
- Redis server (for WebSocket message broker)

Clone the Repository

git clone https://github.com/DMV242/Django-chat.git
cd Django-chat

Create Virtual Environment

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

Configuration

Create Environment Variables

Create a .env file in the chatApp directory:

SECRET_KEY=your-django-secret-key-here
DEBUG=True
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_SECRET=your-google-client-secret

Database Setup

cd chatApp
python manage.py makemigrations
python manage.py migrate

Create Superuser

python manage.py createsuperuser

Run Redis Server

# On Windows (requires Redis installation or WSL)
redis-server

# On macOS/Linux
redis-server

Start Development Server

python manage.py runserver

Ensure you also start Daphne (ASGI server) for WebSocket support:

daphne -b 0.0.0.0 -p 8001 chatApp.asgi:application

Access Application

- Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

Usage

User Registration

1. Click "Inscrivez-vous" (Sign up)
2. Enter username and email
3. Create a password
4. Click "Créer un compte" (Create account)
5. Alternatively, use "Connexion avec Google" (Connect with Google)

Login

1. Enter username and password
2. Click "Se connecter" (Connect)
3. Or use Google OAuth login

Create Chat Room

1. Click "Créer un sallon discussion" (Create a discussion room)
2. Enter room name (alphanumeric characters only)
3. Click "créer un salon" (Create room)

Join and Chat

1. Click on a room to enter
2. Type message in the input field
3. Click "Envoyer" (Send) or press Enter
4. Share images using the file upload button

Delete Room

1. Go to home page
2. Click "Supprimer" (Delete) on rooms you created
3. Confirm deletion

Logout

1. Click "Se déconnecter" (Disconnect)

Database Models

Room Model

from django.db import models
from django.contrib.auth import get_user_model

class Room(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[RegexValidator(regex=r"^[a-zA-Z0-9]+$")]
    )
    slug = models.SlugField(default="")
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return "Room " + self.name

Message Model

class Message(models.Model):
    content = models.CharField(max_length=500, blank=True, null=True)
    author = models.ForeignKey(get_user_model(), models.CASCADE)
    room = models.ForeignKey(Room, models.CASCADE)
    sended_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images/", blank=True)

    def __str__(self):
        return "Message de " + self.author.get_username()

API Endpoints

Chat Routes

- GET /home/ - List all chat rooms
- POST /home/ - Create new room
- GET /room/<room_name>/ - View room messages
- GET /room/<slug>/delete/ - Delete room

Authentication Routes

- GET/POST / - Login page
- GET/POST /signup/ - Registration page
- POST /logout/ - Logout user
- GET/POST /accounts/ - Django-allauth endpoints
- GET/POST /accounts/google/login/ - Google OAuth

Admin Routes

- GET/POST /admin/ - Django admin panel

WebSocket Implementation

The application uses Django Channels for real-time messaging via WebSocket.

WebSocket URL

ws://localhost:8001/ws/chat/<room_name>/

ChatConsumer Class

Location: chatApp/chat/consumers.py

Key Methods:
- connect(): Establishes WebSocket connection and joins room group
- disconnect(): Closes connection and leaves room group
- receive(): Handles incoming messages and images
- chat_message(): Broadcasts text messages to room group
- chat_image(): Broadcasts images to room group
- save_message(): Saves message to database
- get_room(): Retrieves room from database

Message Format

Text Message:
{
    "message": "Hello everyone!",
    "type": "chat.message",
    "user": "username",
    "time": "14:30:45"
}

Image Message:
{
    "image": "data:image/png;base64,iVBORw0KGgo...",
    "name": "image.png",
    "type": "chat.image",
    "user": "username",
    "time": "14:30:45"
}

Frontend WebSocket Handler

Location: chatApp/static/js/chat/main.js

Handles:
- Opening WebSocket connection
- Sending messages and images
- Receiving and displaying messages
- Real-time message updates

Development

Running Tests

python manage.py test

Django Admin

Access at http://localhost:8000/admin

Manage:
- Users and permissions
- Rooms and messages
- Django Allauth settings

Making Migrations

python manage.py makemigrations
python manage.py migrate

Collecting Static Files

python manage.py collectstatic

Troubleshooting

WebSocket Connection Failed

- Ensure Redis is running
- Check Daphne server is started
- Verify firewall settings

Messages Not Appearing

- Check browser console for errors
- Verify WebSocket URL is correct
- Ensure user is authenticated

Database Errors

- Run migrations: python manage.py migrate
- Check database permissions
- Verify database configuration in settings.py

Contributing

1. Fork the repository
2. Create feature branch (git checkout -b feature/amazing-feature)
3. Commit changes (git commit -m 'Add amazing feature')
4. Push to branch (git push origin feature/amazing-feature)
5. Open Pull Request

License

This project is open source and available under the MIT License.

Author

Created by DMV242

Contact & Support

For issues, questions, or suggestions, please open an issue on GitHub.
