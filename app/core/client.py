import httpx
from fastapi import HTTPException, status

from app.core.config import settings

class StreamtapeClient:
    """
    An asynchronous client to interact with the Streamtape API.
    """
    def __init__(self):
        self.base_url = settings.STREAMTAPE_BASE_URL
        self._client = httpx.AsyncClient(base_url=self.base_url)

    async def _make_request(self, method: str, endpoint: str, params: dict | None = None) -> dict:
        """
        A generic method to make requests to the Streamtape API.
        
        It automatically includes authentication and handles standard API responses.
        """
        full_params = {
            "login": settings.STREAMTAPE_API_LOGIN,
            "key": settings.STREAMTAPE_API_KEY,
        }
        if params:
            full_params.update(params)

        try:
            response = await self._client.request(method, endpoint, params=full_params)
            response.raise_for_status()
            
            data = response.json()

            if data.get("status") != 200:
                error_map = {
                    400: status.HTTP_400_BAD_REQUEST,
                    403: status.HTTP_403_FORBIDDEN,
                    404: status.HTTP_404_NOT_FOUND,
                    451: status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
                    509: status.HTTP_503_SERVICE_UNAVAILABLE,
                }
                http_status = error_map.get(data.get("status"), status.HTTP_500_INTERNAL_SERVER_ERROR)
                raise HTTPException(status_code=http_status, detail=data.get("msg", "Unknown API error"))

            return data.get("result")

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error occurred: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Could not connect to Streamtape API: {e}")

    async def close(self):
        """Closes the underlying httpx client to release resources."""
        await self._client.aclose()

streamtape_client = StreamtapeClient()