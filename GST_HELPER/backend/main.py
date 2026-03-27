from fastapi import FastAPI
from routes.invoice_routes import router
from fastapi.middleware.cors import CORSMiddleware
from storage import init_storage

app = FastAPI()

init_storage()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)