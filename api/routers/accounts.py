from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from uuid import UUID
from typing import Optional
from sqlalchemy import func

from db import get_session
from models import Account, Trade
from schemas import AccountCreate, AccountRead

router = APIRouter(prefix="/api/accounts", tags=["accounts"])

@router.get("", response_model=list[AccountRead])
def list_accounts(session: Session = Depends(get_session)):
    return session.exec(select(Account).order_by(Account.name)).all()

@router.post("", response_model=AccountRead)
def create_account(payload: AccountCreate, session: Session = Depends(get_session)):
    exists = session.exec(select(Account).where(Account.name == payload.name)).first()
    if exists:
        raise HTTPException(400, "Account name already exists")
    acc = Account(name=payload.name)
    session.add(acc); session.commit(); session.refresh(acc)
    return acc

# PATCH pour renommer un compte
@router.patch("/{account_id}", response_model=AccountRead)
def rename_account(account_id: UUID, payload: AccountCreate, session: Session = Depends(get_session)):
    acc = session.get(Account, account_id)
    if not acc:
        raise HTTPException(404, "Account not found")
    if not payload.name.strip():
        raise HTTPException(400, "Name cannot be empty")
    exists = session.exec(select(Account).where(Account.name == payload.name, Account.id != account_id)).first()
    if exists:
        raise HTTPException(400, "Another account already uses this name")
    acc.name = payload.name.strip()
    session.add(acc); session.commit(); session.refresh(acc)
    return acc

# Stats simples (nb de trades)
@router.get("/{account_id}/stats")
def account_stats(account_id: UUID, session: Session = Depends(get_session)):
    if not session.get(Account, account_id):
        raise HTTPException(404, "Account not found")
    count = session.exec(select(func.count(Trade.id)).where(Trade.account_id == account_id)).one()
    return {"trade_count": int(count[0])}

# Suppression: bloquée si des trades existent
@router.delete("/{account_id}")
def delete_account(account_id: UUID, session: Session = Depends(get_session)):
    acc = session.get(Account, account_id)
    if not acc:
        raise HTTPException(404, "Account not found")
    count = session.exec(select(func.count(Trade.id)).where(Trade.account_id == account_id)).one()
    if int(count[0]) > 0:
        raise HTTPException(400, f"Cannot delete: {int(count[0])} trades linked to this account.")
    session.delete(acc); session.commit()
    return {"ok": True}
