from fastapi import FastAPI
from send_email.routers import email_router

app = FastAPI()

app.include_router(email_router.router)
