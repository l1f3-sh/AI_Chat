# AI Chat System - REST API

This repository contains the backend REST API for an AI Chat System, built with Django and Django REST Framework. The API provides endpoints for user registration, login, token-based authentication, and interaction with a simulated AI chatbot.

## Features

- **User Authentication**: Secure user registration and token-based login.

- **Token Management**: Users are assigned a starting balance of 4,000 tokens.

- **Chat Interaction**: Authenticated users can send messages to the chatbot.

- **Token Deduction**: Each chat message costs 100 tokens, which are deducted from the user's balance.

- **Chat History**: All interactions are saved to the database.

- **Balance Check**: Users can check their remaining token balance at any time.

## Technology Stack

- **Backend**: Python, Django

- **API Framework**: Django REST Framework (DRF)

- **Database**: SQLite3 (for development)

## Setup and Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

- Python 3.13+

- `pip` and `venv`

### Installation Steps

1. **Clone the repository:**

    ```
    git clone <your-repository-url>
    cd <repository-name>
    
    ```

2. **Create and activate a virtual environment:**

    ```
    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    ```

3. **Install the required dependencies:**

    ```
    pip install -r requirements.txt
    
    ```

    _(Note: If you don't have a `requirements.txt` file, you can install the packages directly: `pip install django djangorestframework`)_

4. **Apply database migrations:** This will create the necessary database tables based on the models.

    ```
    python manage.py migrate
    
    ```

5. **Run the development server:**

    ```
    python manage.py runserver
    
    ```

    The API will now be running at `http://127.0.0.1:8000/`.

## API Endpoints

The base URL for all endpoints is `/api/`.

### 1. User Registration

Creates a new user account and returns an authentication token.

- **Endpoint**: `POST /api/register/`

- **Method**: `POST`

- **Body**:

    ```
    {
        "username": "newuser",
        "password": "strongpassword123",
        "email": "user@example.com"
    }
    
    ```

- **Success Response (201 CREATED)**:

    ```
    {
        "message": "User registered successfully",
        "token": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
    }
    
    ```

### 2. User Login

Authenticates a user and returns their session token.

- **Endpoint**: `POST /api/login/`

- **Method**: `POST`

- **Body**:

    ```
    {
        "username": "newuser",
        "password": "strongpassword123"
    }
    
    ```

- **Success Response (200 OK)**:

    ```
    {
        "token": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
    }
    
    ```

### 3. Chat Interaction

Sends a message to the chatbot. Requires token authentication.

- **Endpoint**: `POST /api/chat/`

- **Method**: `POST`

- **Headers**: `Authorization: Token <your_auth_token>`

- **Body**:

    ```
    {
        "message": "Hello, how does this work?"
    }
    
    ```

- **Success Response (200 OK)**:

    ```
    {
        "message": "Hello, how does this work?",
        "response": "This is a dummy AI response to your message: 'Hello, how does this work?'",
        "timestamp": "2025-08-19T00:48:00.123456Z"
    }
    
    ```

- **Error Response (402 PAYMENT REQUIRED)**:

    ```
    {
        "error": "Insufficient tokens"
    }
    
    ```

### 4. Check Token Balance

Retrieves the current user's token balance. Requires token authentication.

- **Endpoint**: `GET /api/token-balance/`

- **Method**: `GET`

- **Headers**: `Authorization: Token <your_auth_token>`

- **Success Response (200 OK)**:

    ```
    {
        "tokens": 3900
    }
    
    ```

## Challenges and Refactoring Decisions

The initial implementation, while functional, had significant security and design flaws. The project was refactored to align with modern best practices for Django and DRF.

1. **Challenge: Manual Password Hashing**

    - **Initial Approach**: The original `User` model overrode the `save()` method to manually hash passwords using `make_password`. This is not standard practice and can be error-prone.

    - **Refactored Solution**: Switched to inheriting from Django's `AbstractUser`. This leverages Django's built-in, secure authentication system. The `User.objects.create_user()` helper function now handles password hashing automatically and correctly.

2. **Challenge: Custom Token Authentication**

    - **Initial Approach**: A custom `AuthToken` model and a manual authentication view were created. This reinvents the wheel and misses out on the security features and integrations provided by DRF.

    - **Refactored Solution**: Removed the custom token logic and integrated DRF's built-in `TokenAuthentication`. The login endpoint now uses DRF's `obtain_auth_token` view, which is robust and secure. Protected endpoints now use the simple `permission_classes = [IsAuthenticated]` decorator, making the code cleaner and more declarative.

## Suggestions for Future Improvement

- **JWT Authentication**: For more advanced security, replace the basic Token Authentication with JSON Web Tokens (JWT). JWTs can carry expiration dates and other claims, making them suitable for more complex applications.

- **Rate Limiting**: Implement rate limiting on sensitive endpoints like login and chat to prevent brute-force attacks and API abuse.

- **Real AI Integration**: Replace the hardcoded dummy response in the `ChatView` with an API call to a real AI service like OpenAI's GPT or Google's Gemini.

- **API Documentation**: Integrate a library like `drf-spectacular` or `drf-yasg` to automatically generate interactive API documentation (Swagger/OpenAPI).

- **Comprehensive Testing**: Expand the unit tests to cover more edge cases and ensure long-term reliability.
