import httpx
from fastapi import HTTPException


async def connect_to_tappay(url, headers, payload):

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return response.json()