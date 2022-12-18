from typing import Dict,Any,Optional
import logging

import httpx

from app.errors.http import HttpRequestError

class HttpClient:
    def __init__(self, url: str) -> None:
        self._url = url
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin'
        }


    async def _make_request(
        self,
        method: str,
        endpoint: str,
        json: Optional[Dict[str,Any]] = None,
        params: Optional[Dict[str,Any]] = None,
        headers: Optional[Dict[str,Any]] = None,
        timeout: int = 5
    ) -> Dict[str,Any]:
        async with httpx.AsyncClient() as client:
            request = client.build_request(
                method=method,
                url=f'{self._url}{endpoint}',
                json=json,
                params=params,
                headers=headers,
                timeout=timeout,
            )
            try:
                response = await client.send(request)
            except httpx.RequestError as exc:
                logging.error(f"Http call to {exc.request.url!r} failed with: {str(exc)}")
                raise HttpRequestError()
            
            return response

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str,Any]] = None,
        headers: Optional[Dict[str,Any]] = None,
        timeout: int = 10
    ) -> Dict[str,Any]:
        response = await self._make_request(
            method="GET",
            endpoint=endpoint,
            params=params,
            headers=headers,
            timeout=timeout,
        )
        return response

    @property
    def headers(self):
        return self._headers
    
