# Library Management Web Application

## Overview
The Library Management Web app is a personal project aimed at providing basic library functionality to help with book management in a web format, built with Django and Nuxt.js. 

## Features

Authentication and User Management
- User authentication
- Role based access
- User profiles

Book Management
- Pre-populated book data from Google Books API
- Book availability tracking
- Detailed book information
- Search and filter for books

Loan System *WIP*
- Book borrowing system
- Due date tracking
- Loan history

## Technology Stack

Backend:
- Django
- SQLite
- Python

Frontend:
- Nuxt 3
- Vue 3
- TypeScript
- Vuetify 3
- Yarn

## Getting Started

### Prerequisites
- Python 3.12 or higher
- Node.js 16 or higher
- Yarn package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/library-app.git
cd library-app
```

2. Set Up the Backend
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver

3. Set Up the Frontend
# Install dependencies
yarn install

# Start the development server
yarn dev

