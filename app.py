import asyncio

from socket import AF_INET
from typing import Optional, Any

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import aiohttp

from fastapi import FastAPI

# M-Pesa Client
from mpesa_client.generate_oauth_token import router as generate_token_routes
from mpesa_client.lipa_na_mpesa import router as lipa_na_mpesa_routes
from mpesa_client.simulate_c2b_payment import router as simulate_c2b_routes

# Confirmation:
from mpesa_confirmation.confirmation import router as mpesa_confirmation_routes

# Validation
from mpesa_validation.validation import router as mpesa_validation_routes


SIZE_POOL_AIOHTTP = 200


class Http:
    sem: Optional[asyncio.Semaphore] = None
    aiohttp_client: Optional[aiohttp.ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=50)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)
            cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout, connector=connector)

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def get(cls, url: str, username: str, password: str, headers: Optional[dict] = None,
                  data: Optional[dict] = None) -> Any:
        client = cls.get_aiohttp_client()
        try:

            async with client.get(url, headers=headers, data=data,
                                  auth=aiohttp.BasicAuth(username, password)) as response:
                if response.status != 200:
                    _response = await response.text()
                    payload = {"response": _response,
                               "url": url,
                               "httpmethod": "get",
                               "headers": headers,
                               "response_status": f"{response.status}, {response.reason}",
                               "success": False}

                    return payload

                json_result = await response.json()
        except aiohttp.ClientConnectorError:
            payload = {"error": "Cannot connect to host.",
                       "url": url,
                       "httpmethod": "get",
                       "headers": headers,
                       "success": False}

            return payload
        except Exception as e:
            payload = {"error": str(e),
                       "url": url,
                       "httpmethod": "get",
                       "headers": headers,
                       "response_status": f"{response.status}, {response.reason}",
                       "success": False}

            return payload

        return json_result

    @classmethod
    async def post(cls, url: str, headers: Optional[dict] = None, data: Optional[str] = None) -> Any:
        client = cls.get_aiohttp_client()

        try:
            async with client.post(url, headers=headers, data=data) as response:
                if response.status != 200:
                    _response = await response.text()
                    payload = {"response": _response,
                               "url": url,
                               "httpmethod": "postString",
                               "headers": headers,
                               "response_status": f"{response.status}, {response.reason}",
                               "success": False}

                    return payload

                json_result = await response.json()
        except aiohttp.ClientConnectorError:
            payload = {"error": "Cannot connect to host",
                       "url": url,
                       "httpmethod": "post",
                       "headers": headers,
                       "success": False}

            return payload
        except Exception as e:
            payload = {"error": str(e),
                       "url": url,
                       "httpmethod": "post",
                       "headers": headers,
                       "response_status": f"{response.status}, {response.reason}",
                       "success": False}

            return payload

        return json_result


async def on_start_up() -> None:
    Http.get_aiohttp_client()


async def on_shutdown() -> None:
    await Http.close_aiohttp_client()


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

# Mount the folders:
app.mount("/static", StaticFiles(directory="static"), name="static")

# add the routers:
app.include_router(generate_token_routes)
app.include_router(mpesa_confirmation_routes)
app.include_router(mpesa_validation_routes)
app.include_router(lipa_na_mpesa_routes)
app.include_router(simulate_c2b_routes)


# Page not found exception handler
@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse("/not-found")
