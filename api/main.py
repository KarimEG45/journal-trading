import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from db import init_db, engine   # ⬅️ importer engine (pas get_session ici)
from routers import trades, uploads
from routers import accounts
from models import Account

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
    # crée les tables si besoin
    init_db()

    # Seed des comptes via .env : ACCOUNTS="FTMO,Darwinex,Compte Perso"
    seed = os.getenv("ACCOUNTS", "").strip()
    if seed:
        with Session(engine) as s:    # ⬅️ ouvrir une session avec engine
            existing = {a.name for a in s.exec(select(Account)).all()}
            for name in [x.strip() for x in seed.split(",") if x.strip()]:
                if name not in existing:
                    s.add(Account(name=name))
            s.commit()

# routeurs
app.include_router(accounts.router)
app.include_router(trades.router)
app.include_router(uploads.router)

@app.get("/health")
def health():
    return {"status": "ok"}
