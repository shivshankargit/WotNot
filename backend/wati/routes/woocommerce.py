#  there are the webhooks routes for integration with woocommerce


from fastapi import FastAPI, Depends, HTTPException, Request,APIRouter
from sqlalchemy.orm import Session
from ..database import database  # Your database connection
from ..models import User 
import json # Your models
import requests
from ..Schemas import user
from ..oauth2 import get_current_user

router=APIRouter(tags=['woocommerce'])



# Function to verify API key from request headers or query params
def verify_api_key(request: Request, db: Session ):
    api_key = request.headers.get("Authorization")
    
    # If the API key is passed as a query parameter
    if not api_key:
        api_key = request.query_params.get("api_key")
        
    # Remove "Bearer " if passed in the Authorization header
    if api_key and api_key.startswith("Bearer "):
        api_key = api_key[7:]
    
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    # Check if API key exists in the database
    user = db.query(User.User).filter(User.User.api_key == api_key).first()
    
    if not user:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return user


# function to send order confirmation
def send_order_confirmation_message(order_data, whatsapp_token,phone_id):
    """
    Sends a user-specific message template when a new order is created in WooCommerce.
    """
    customer_phone = order_data["billing"]["phone"]
    customer_name = order_data["billing"]["first_name"]
    order_id = order_data["id"]
    order_total = order_data["total"]
    

    # Define the message template data
    message_data = {
        "messaging_product": "whatsapp",
        "to": customer_phone,
        "type": "template",
        "template": {
            "name": "wotnot_order_confirmation",  # Use the user's template
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": customer_name},
                        {"type": "text", "text": order_id},
                        {"type": "text", "text": order_total}
                    ]
                }
            ]
        }
    }

    # WhatsApp API endpoint and headers
    API_URL = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
    API_HEADERS = {
        "Authorization": f"Bearer {whatsapp_token}",  # Use user-specific token
        "Content-Type": "application/json"
    }

    # Send message to WhatsApp API
    response = requests.post(API_URL, headers=API_HEADERS, json=message_data)

    if response.status_code == 200:
        print(f"Message sent successfully to {customer_phone}")
    else:
        print(f"Failed to send message. Response: {response.text}")

    

# webhook for the order cofirmation
@router.post("/webhook/woocommerce")
async def handle_woocommerce_webhook(request: Request, db: Session = Depends(database.get_db)):
    # Verify API key
    user = verify_api_key(request, db)



    body = await request.body()
    print(f"Webhook received: {body.decode('utf-8')},user id is {user.id}")  # Log the raw body for debugging
    
    # Try to parse the body as JSON
    try:
        payload = await request.json()
        send_order_confirmation_message(payload, user.PAccessToken,user.Phone_id)
    except Exception as e:
        return {"error": "Invalid JSON", "detail": str(e)}

    # Continue processing the webhook data

    print(payload)
    return {"status": "success"}
    




# route for fetchapi key

@router.get("/webhooklink")
def apikey(request:Request,get_current_user: user.newuser=Depends(get_current_user)):
    apikey=get_current_user.api_key

    link="http://localhost:8000"

    webhooklink=f"{link}//webhook/woocommerce/{apikey}"

    return{"webkook_link":webhooklink}
    



# route for the woocommerce integration form
# @router.post("/woocommerce-configuration")
