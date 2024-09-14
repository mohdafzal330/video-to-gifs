# app/routes/subscription.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import stripe
from ..database import get_db
from ..models import Subscription

router = APIRouter(
    prefix="/subscription",
    tags=["subscriptions"]
)

stripe.api_key = "sk_test_51PysspP0YIgmInaDYCab8mQlneNo0xNC67l7UFCg4AJyp3fbt2kwO3FpYicXct2PuapYRks87kgZAvWJWplORpak00aejjP5uB"  # Replace with your Stripe secret key

@router.post("/")
def create_subscription(user_id: int = 1, plan: str = 'basic', db: Session = Depends(get_db)):
    try:
        # Placeholder Stripe subscription logic
        stripe_subscription = stripe.Subscription.create(
            customer="customer_id_placeholder",
            items=[
                {"price": "price_id_placeholder"},
            ],
        )

        db_subscription = Subscription(user_id=user_id, plan=plan, is_active=True)
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return db_subscription
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
