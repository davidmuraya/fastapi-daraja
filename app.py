
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from http_client import on_start_up, on_shutdown

from fastapi import FastAPI

# M-Pesa Client
from mpesa_client.generate_oauth_token import router as generate_token_routes
from mpesa_client.lipa_na_mpesa_stkpush import router as lipa_na_mpesa_routes
from mpesa_client.lipa_na_mpesa_query_transaction import router as lipa_na_mpesa_query_status
from mpesa_client.simulate_c2b_payment import router as simulate_c2b_routes

# Confirmation:
from mpesa_confirmation.confirmation import router as mpesa_confirmation_routes

# Validation
from mpesa_validation.validation import router as mpesa_validation_routes


api_description = """
This is a FastAPI library based on the Safaricom M-PESA daraja API.

M-Pesa is a mobile phone-based digital payment and money transfer service widely used in Kenya.

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

For the M-Pesa client, this library uses the python asynchronous client called aiohttp. 
aiohttp is a versatile asynchronous HTTP client/server framework for Python that supports both client and server-side applications.
"""

app = FastAPI(docs_url="/", on_startup=[on_start_up], on_shutdown=[on_shutdown], title="FastAPI Daraja",
              description=api_description, version="1.0.0", swagger_ui_parameters={"defaultModelsExpandDepth": -1})

# Hide the models by adding the parameter: swagger_ui_parameters={"defaultModelsExpandDepth": -1}

# Mount the folders: Add your files when creating jinja2 templates
# app.mount("/static", StaticFiles(directory="static"), name="static")

# add the routers:
app.include_router(generate_token_routes)
app.include_router(mpesa_confirmation_routes)
app.include_router(mpesa_validation_routes)
app.include_router(lipa_na_mpesa_routes)
app.include_router(lipa_na_mpesa_query_status)
app.include_router(simulate_c2b_routes)


# Page not found exception handler
@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse("/not-found")
