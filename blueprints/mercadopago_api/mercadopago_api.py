import os
from fastapi import APIRouter, HTTPException, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv
from services.user_service.user_service_postgres import UserServicePostgres
from database import get_db

load_dotenv()

MERCADO_PAGO_ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
user_service = UserServicePostgres()
mercadopago_router = APIRouter()


@mercadopago_router.post("/mercadopago/webhook")
async def mercadopago_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON"})

    payment_id = body.get("data", {}).get("id")
    if not payment_id:
        return JSONResponse(status_code=400, content={"error": "Invalid payload"})

    # Consultar el pago en MercadoPago
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.mercadopago.com/v1/payments/{payment_id}",
            headers={"Authorization": f"Bearer {MERCADO_PAGO_ACCESS_TOKEN}"},
        )

    if response.status_code != 200:
        return JSONResponse(
            status_code=500, content={"error": "No se pudo consultar el pago"}
        )

    payment_data = response.json()

    if payment_data.get("status") == "approved":
        metadata = payment_data.get("metadata", {})
        user_id = metadata.get("user_id")
        tokens = metadata.get("tokens", 0)

        if not user_id:
            return JSONResponse(
                status_code=400, content={"error": "Falta user_id en metadata"}
            )

        print(f"Acreditando tokens: {tokens} para usuario {user_id} ✅✅✅✅✅✅")

        user_service = UserServicePostgres()

        # Ejecutar en transacción
        async with db.begin():
            await user_service.add_user_token(db, uuid=user_id, amount_of_tokens=tokens)

        return JSONResponse(status_code=200, content={"message": "Tokens acreditados"})

    return JSONResponse(status_code=200, content={"message": "Pago no aprobado"})


# Modelo para recibir el user_id
class PreferenceRequest(BaseModel):
    user_id: str


# Nuevo endpoint para generar preferencia
@mercadopago_router.post("/mercadopago/preference")
async def create_preference(data: PreferenceRequest):
    # Construimos la preferencia
    payload = {
        "items": [
            {"id": "message", "unit_price": 500, "quantity": 1, "title": "1 Token"}
        ],
        "metadata": {"user_id": data.user_id, "tokens": 1},
        "back_urls": {
            "success": "https://aprendiendoconpersonajes.duckdns.org/",
            "pending": "https://aprendiendoconpersonajes.duckdns.org/",
            "failure": "https://aprendiendoconpersonajes.duckdns.org/",
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.mercadopago.com/checkout/preferences",
            headers={
                "Authorization": f"Bearer {MERCADO_PAGO_ACCESS_TOKEN}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

    if response.status_code != 201:
        return JSONResponse(
            status_code=500, content={"error": "Error creando preferencia"}
        )

    preference = response.json()
    return {"init_point": preference["init_point"]}
