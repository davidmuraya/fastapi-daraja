# M-PESA Daraja APIs with FastAPI
FastAPI Middle Office Ware

This is a FastAPI library based on the Safaricom MPESA daraja API. 

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

For the M-Pesa client, this library uses the python asynchronous client called aiohttp. 
aiohttp is a versatile asynchronous HTTP client/server framework for Python that supports both client and server-side applications.

MPESA Daraja API documentation can be found at https://developer.safaricom.co.ke

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

# Deploy with docker compose
```shell
docker-compose up -d --build
```