import asyncio

from socket import AF_INET
from typing import Optional, Any

import aiohttp


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
                               "http_method": "get",
                               "headers": headers,
                               "response_status": f"{response.status}, {response.reason}",
                               "success": False}

                    return payload

                json_result = await response.json()
        except aiohttp.ClientConnectorError:
            payload = {"error": "Cannot connect to host.",
                       "url": url,
                       "http_method": "get",
                       "headers": headers,
                       "success": False}

            return payload
        except Exception as e:
            payload = {"error": str(e),
                       "url": url,
                       "http_method": "get",
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
                               "http_method": "postString",
                               "headers": headers,
                               "response_status": f"{response.status}, {response.reason}",
                               "success": False}

                    return payload

                json_result = await response.json()
        except aiohttp.ClientConnectorError:
            payload = {"error": "Cannot connect to host",
                       "url": url,
                       "http_method": "post",
                       "headers": headers,
                       "success": False}

            return payload
        except Exception as e:
            payload = {"error": str(e),
                       "url": url,
                       "http_method": "post",
                       "headers": headers,
                       "response_status": f"{response.status}, {response.reason}",
                       "success": False}

            return payload

        return json_result


async def on_start_up() -> None:
    Http.get_aiohttp_client()


async def on_shutdown() -> None:
    await Http.close_aiohttp_client()

