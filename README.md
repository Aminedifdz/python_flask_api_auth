# Flask Authentication App

This Flask application demonstrates basic authentication using JWT tokens and refresh tokens, providing a secure method for handling user authentication and session management in web applications. It utilizes Flask for the backend and Flask-JWT-Extended for managing JWT tokens, including access and refresh tokens, and implementing logout functionality by invalidating these tokens.

## Features

- User registration and login
- JWT access token generation for authenticated sessions
- Refresh tokens for safely regenerating access tokens
- Endpoint protection requiring valid JWT tokens for access
- Logout functionality that invalidates both access and refresh tokens

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have Python 3.6 or later installed on your system. This application has been tested with Python 3.11.

### Installation

1. **Clone the repository**

git clone https://github.com/Aminedifdz/python_flask_api_auth

cd "FlaskAuthenticationAppDirectory"

2. **Set up a virtual environment**

python -m venv env

source env/bin/activate # On Windows use env\Scripts\activate

3. **Install required packages**

pip install -r requirements.txt

4. **Environment Variables**

Create a `.env` file in the root directory of the project and add the following variables:

SECRET_KEY=your_secret_key

FLASK_APP=main.py

FLASK_ENV=development

Replace `your_secret_key` with a strong secret key.

5. **Initialize the Database**

flask shell

>>> from main import User

>>> from main import TokenBlockList

>>> db.create_all()

>>> exit()

6. **Run the Application**

flask run

The application should now be running on `http://127.0.0.1:5000/`.

## Usage

- **Register a new user**

Send a POST request to `/auth/register` with a JSON body containing `username`, `email`, and `password`.

- **Log in**

Send a POST request to `/auth/login` with a JSON body containing `email` and `password`. You'll receive an access token and a refresh token.

- **Access Protected Endpoints**

Use the access token received from login as a Bearer token in the Authorization header of your request to access protected endpoints.

- **Refresh Token**

Send a POST request to `/auth/refresh` with the refresh token to receive a new access token.

- **Logout (Invalidate Tokens)**

To securely log out, send a POST request to `/auth/revoke_token` with the access and/or refresh token you wish to invalidate. This will add the tokens to a blocklist, effectively logging the user out.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

