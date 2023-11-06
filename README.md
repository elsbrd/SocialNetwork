# Social Network API

This project implements a basic social network API with Django REST Framework. Users can sign up, log in, create posts, and like/unlike posts. Additionally, it provides analytics for likes and tracks user activity.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

- Python 3.8+
- pip
- Virtualenv (optional but recommended)

### Installing

A step-by-step series of examples that tell you how to get a development environment running:

Clone the repository:
```
git clone https://github.com/elsbrd/SocialNetwork.git
cd SocialNetwork
```

Create a virtual environment and activate it (optional):
```
virtualenv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required packages:
```
pip install -r requirements.txt
```

Migrate the database:
```
python manage.py migrate
```

Run the development server:
```
python manage.py runserver
```

The API should now be accessible at `http://127.0.0.1:8000/`.

## Features

- **User Signup**: `POST /api/signup/`
- **User Login**: `POST /api/login/` returns a JWT token for authentication.
- **Post Creation**: `POST /api/posts/` (auth required)
- **Post Like**: `POST /api/posts/<id>/like/` (auth required)
- **Post Unlike**: `DELETE /api/posts/<id>/like/` (auth required)
- **Analytics**: `GET /api/analytics/?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD` shows likes aggregated by day.
- **User Activity**: `GET /api/users/<id>/activity/` shows last login and last request date.

## Automated Bot

The automated bot is a Python script that simulates user interaction with the social network.

### Configuration

The bot's behavior is defined in a `config.json` file. Example:

```json
{
      "number_of_users": 3,
      "max_posts_per_user": 4,
      "max_likes_per_user": 2
}
```

The bot will:
- Sign up the specified number of users.
- Create a random number of posts for each user.
- Like posts randomly across the user base.

## Development Notes

- Authentication is handled using JWT tokens.
- The project structure follows Django's best practices.
- Error handling is implemented for common scenarios (invalid requests, authentication failures, etc.).

