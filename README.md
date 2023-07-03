# M-PESA Daraja APIs with FastAPI
FastAPI Middle Office Ware

This is a FastAPI library based on the Safaricom MPESA daraja API. 

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

For the M-Pesa client, this library uses the python asynchronous client called aiohttp. 
aiohttp is a versatile asynchronous HTTP client/server framework for Python that supports both client and server-side applications.

MPESA Daraja API documentation can be found at https://developer.safaricom.co.ke

The technology stack used to create the backend of this application is as follows:

- Framework
    - FastAPI and Starlette
- ASGI Server
    - Uvicorn and Gunicorn
- Containerization
    - Docker
- Database
    - tbc
- Authentication
    - Bcrypt
    - Passlib
    - JWT Tokens with Pyjwt
- Testing
    - Pytest
- Development
    - PyCharm


# Configuration
Please create a .env file in the app folder with your configuration:
```shell
# M-Pesa Settings:
C2B_CONSUMER_KEY="xxx"
C2B_CONSUMER_SECRET="xxx"
LIPA_NA_MPESA_CONSUMER_KEY="xx"
LIPA_NA_MPESA_CONSUMER_SECRET="xxx"
LIPA_NA_MPESA_PASSKEY="xxx"
C2B_CONFIRMATION_URL=""
C2B_VALIDATION_URL=""
LIPA_NA_MPESA_CALLBACK_URL="xxxx"
LIPA_NA_MPESA_BUSINESS_SHORT_CODE="xxx"
```

### Python/FastAPI Daraja App
Project structure:
```
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── app
    ├── main.py
    ├── __init__.py

```

[_docker-compose.yml_](docker-compose.yml)
```
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fastapi-daraja
    command: uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
    env_file:
      - .env
    ports:
      - "8000:8000"
    restart: "always"

```



# Deploy with docker compose
```shell
docker-compose up -d --build
```

## Expected result

Listing containers must show one container running and the port mapping as below:
```
$ docker ps
CONTAINER ID   IMAGE          COMMAND       CREATED              STATUS              PORTS                                               NAMES
7087a6e79610   5c1778a60cf8   "/start.sh"   About a minute ago   Up About a minute   80/tcp, 0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   fastapi-daraja
```

After the application starts, navigate to `http://localhost:8000` in your web browser and you should see the swagger ui.