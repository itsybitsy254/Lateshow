# Late Show Flask Application

This is a Flask application that manages episodes, guests, and their appearances on a Late Show. The API provides functionalities to create, read, update, and delete episodes, retrieve guests, and associate them with their appearances on specific episodes using a relational database.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)

## Features
- Create, read, and delete episodes.
- Retrieve information about guests.
- Associate guests with episodes by creating appearances with ratings.
- Input validation for creating associations.
- Detailed error handling with informative messages.

## Technologies
- **Flask**: Web framework for building the API.
- **Flask-SQLAlchemy**: ORM for database management.
- **Flask-Migrate**: For handling database migrations.
- **Marshmallow**: For serialization and validation.
- **SQLite**: Database management system.
- **Python**: Programming language.

## Installation

1. **Clone the repository:**
    ```bash
    git clone git@github.com:itsybitsy254/Lateshow.git
    cd lateshow
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Setup

1. **Run database migrations to set up the database schema:**
    ```bash
    flask db upgrade
    ```

2. **Start the application:**
    ```bash
    python app.py
    ```

   Alternatively:
    ```bash
    flask run
    ```

3. The application will start running on `http://127.0.0.1:5000`.

## Usage

You can use tools like **Postman** or **curl** to interact with the API endpoints. Below are the available endpoints.

## API Endpoints

### Episodes:
- **GET /episodes**: Retrieve all episodes.
  - **Response**: List of episodes with details.
  
- **GET /episodes/<int:id>**: Retrieve a specific episode by ID.
  - **Response**: Details of the episode.
  
- **DELETE /episodes/<int:id>**: Delete a specific episode by ID.
  - **Response**: Success message or error if the episode is not found.

### Guests:
- **GET /guests**: Retrieve all guests.
  - **Response**: List of guests.
  
- **GET /guests/<int:id>**: Retrieve a specific guest by ID.
  - **Response**: Details of the guest.

### Appearances:
- **POST /appearances**: Create a new appearance.
  - **Request Body**:
    ```json
    {
      "rating": 4,
      "episode_id": 1,
      "guest_id": 2
    }
    ```
  - **Response**: Success message or validation errors.

## Error Handling
The application provides detailed error handling:
- If an episode or guest is not found, a 404 error with a message is returned.
- Input validation ensures that data is correctly formatted (e.g., rating between 1 and 5).
- Any server-side errors return a 500 error with a detailed message for troubleshooting.
