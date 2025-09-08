from fastapi import FastAPI
from send_email.app.routers import router

app = FastAPI()

# Include router
app.include_router(router.router)
