from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
import json
import os
import asyncio
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

producer = None

@router.on_event("startup")
async def startup_event():
    global producer
    for i in range(10):
        try:
            print(f"Kafka bootstrap servers: {os.getenv('KAFKA_BOOTSTRAP_SERVERS')}")
            producer = KafkaProducer(
                bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("Kafka Producer initialized.")
            break
        except Exception as e:
            print(f"Kafka not ready yet, retrying in 5 seconds... ({i+1}/10) — {e}")
            await asyncio.sleep(5)
    else:
        raise Exception("Kafka is not available after multiple retries.")


@router.get("/")
def read_root():
    return {"status": "FastAPI is running"}


def load_email_list():
    df = pd.read_excel("send_email/app/email_list.xlsx")
    return df.to_dict(orient="records")


async def send_email_message(person):
    personalized_message = f"""
Dear {person['Name']},

Congratulations!!

We are delighted to have you on board with us.

Role: {person['Role']}
Offer Amount: {person['Offer_amount']}
Start Date: {person['Starting_date']}
Location: {person['Location']}

Regards,
HR Team
"""
    payload = {
        "Email": person["Email"],
        "Name": person["Name"],
        "Role": person["Role"],
        "Offer_amount": person["Offer_amount"],
        "Starting_date": person["Starting_date"],
        "Location": person["Location"],
        "has_passed": person.get("has_passed", "no"),
        "message": personalized_message
    }

    print(f"Queuing message for: {person['Email']}")
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: producer.send("offer_topic", value=payload))


@router.post("/send-emails")
async def send_bulk_emails():
    email_list = load_email_list()
    tasks = [send_email_message(person) for person in email_list]
    await asyncio.gather(*tasks)
    producer.flush()
    return JSONResponse({"status": "Emails queued successfully"})
