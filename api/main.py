import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import init_db               # ⬅ ABSOLU (pas de point)
from routers import trades, uploads  # ⬅ ABSOLU

app = FastAPI(title="Journal Trading API")

origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(trades.router)
app.include_router(uploads.router)

@app.get("/health")
def health():
    return {"status": "ok"}
