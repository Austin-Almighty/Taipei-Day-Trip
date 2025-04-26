import httpx
import os
from fastapi import HTTPException
from dotenv import load_dotenv



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

load_dotenv()

x_api_key = os.getenv("x-api-key")
partner_key = os.getenv("partner_key")
merchant_id = os.getenv("merchant_id")
tappay_url = os.getenv("tappay_URL")

headers = {
        "Content-Type": "application/json",
        "x-api-key": x_api_key  
    }

payload = {
    "partner_key": partner_key,
    "merchant_id": merchant_id,  
    "details": "TapPay Test",
    "cardholder": {
    },
    "remember": False
}

tappay_URL = tappay_url