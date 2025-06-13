from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
import json
import asyncio
from kafka import KafkaProducer
import os
from dotenv import load_dotenv
from functools import partial

load_dotenv()

router = APIRouter()

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def load_email_list():
    df = pd.read_excel("send_email/app/email_list.xlsx")
    return df.to_dict(orient="records")


def send_to_kafka(topic, payload):
    producer.send(topic, value=payload)


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
    await asyncio.get_running_loop().run_in_executor(None, lambda: producer.send("offer_topic", value=payload))  #(gives error)

    #producer.send("offer_topic", value=payload)


    # loop = asyncio.get_running_loop()
    # await loop.run_in_executor(None, send_to_kafka, "offer_topic", payload)
   

@router.post("/send-emails")
async def send_bulk_emails():
    email_list = load_email_list()
    tasks = [send_email_message(person) for person in email_list]
    await asyncio.gather(*tasks)
    producer.flush()
    return JSONResponse({"status": "Emails queued successfully"})

