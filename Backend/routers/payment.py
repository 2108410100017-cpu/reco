# backend/routers/payment.py
from fastapi import APIRouter, HTTPException, Request
import stripe
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Stripe with your secret key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/payment", tags=["payment"])

@router.post("/create-payment-intent")
async def create_payment_intent(request: Request):
    try:
        data = await request.json()
        amount = data.get('amount')  # Amount in cents
        if not amount:
            raise HTTPException(status_code=400, detail="Amount is required.")

        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={'enabled': True},
        )

        return {"clientSecret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
