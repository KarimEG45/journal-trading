from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from db import get_session
from models import Trade
from schemas import TradeCreate, TradeRead
router = APIRouter(prefix="/api/trades", tags=["trades"])

# --- Export CSV (avec filtres) ---
from fastapi.responses import StreamingResponse
import csv, io
from typing import Optional
from sqlmodel import select

@router.get("/export.csv")
def export_csv(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    bias: Optional[str] = None,
    tags: Optional[str] = None,
    session: Session = Depends(get_session),
):
    stmt = select(Trade).order_by(Trade.trade_date, Trade.num_trade)
    if date_from:
        stmt = stmt.where(Trade.trade_date >= date_from)
    if date_to:
        stmt = stmt.where(Trade.trade_date <= date_to)
    if bias:
        stmt = stmt.where(Trade.bias_daily == bias)
    if tags:
        stmt = stmt.where(Trade.tags.ilike(f"%{tags}%"))

    rows = session.exec(stmt).all()

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "id","num_trade","trade_date","analyse_time","bias_daily",
        "mp_bull_low","mp_bull_ll","mp_bull_hl","mp_bull_high",
        "mp_bear_hh","mp_bear_lh",
        "fvg_cible","ob_bullish","ob_bearish",
        "sl","tp","gains_esperes","pnl",
        "liq_buy","liq_sell","reversal","trade_stoppe",
        "rr_planned","rr_realized","setup_notes","emotion","tags",
        "shot_4h_url","shot_1h_url","shot_30m_url","shot_15m_url"
    ])
    for t in rows:
        writer.writerow([
            str(t.id), t.num_trade, t.trade_date, t.analyse_time, t.bias_daily,
            bool(t.mp_bull_low), bool(t.mp_bull_ll), bool(t.mp_bull_hl), bool(t.mp_bull_high),
            bool(t.mp_bear_hh), bool(t.mp_bear_lh),
            t.fvg_cible, bool(t.ob_bullish), bool(t.ob_bearish),
            t.sl, t.tp, t.gains_esperes, t.pnl,
            bool(t.liq_buy), bool(t.liq_sell), bool(t.reversal), bool(t.trade_stoppe),
            t.rr_planned, t.rr_realized, t.setup_notes, t.emotion, t.tags,
            t.shot_4h_url, t.shot_1h_url, t.shot_30m_url, t.shot_15m_url
        ])
    buf.seek(0)
    headers = {"Content-Disposition": 'attachment; filename="trades.csv"'}
    return StreamingResponse(iter([buf.getvalue()]), media_type="text/csv", headers=headers)

@router.post("", response_model=TradeRead)
def create_trade(payload: TradeCreate, session: Session = Depends(get_session)):
    trade = Trade(**payload.model_dump())
    session.add(trade)
    session.commit()
    session.refresh(trade)
    return trade

@router.get("", response_model=List[TradeRead])
def list_trades(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    bias: Optional[str] = None,
    tags: Optional[str] = None,
    session: Session = Depends(get_session),
):
    stmt = select(Trade).order_by(Trade.trade_date.desc(), Trade.num_trade.desc())
    if date_from:
        stmt = stmt.where(Trade.trade_date >= date_from)
    if date_to:
        stmt = stmt.where(Trade.trade_date <= date_to)
    if bias:
        stmt = stmt.where(Trade.bias_daily == bias)
    if tags:
        stmt = stmt.where(Trade.tags.ilike(f"%{tags}%"))
    return session.exec(stmt).all()

@router.get("/{trade_id}", response_model=TradeRead)
def get_trade(trade_id: UUID, session: Session = Depends(get_session)):
    trade = session.get(Trade, trade_id)
    if not trade:
        raise HTTPException(404)
    return trade

@router.patch("/{trade_id}", response_model=TradeRead)
def update_trade(trade_id: UUID, payload: TradeCreate, session: Session = Depends(get_session)):
    trade = session.get(Trade, trade_id)
    if not trade:
        raise HTTPException(404)
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(trade, k, v)
    session.add(trade)
    session.commit()
    session.refresh(trade)
    return trade

# 🚀 NOUVEAU : suppression
@router.delete("/{trade_id}")
def delete_trade(trade_id: UUID, session: Session = Depends(get_session)):
    trade = session.get(Trade, trade_id)
    if not trade:
        raise HTTPException(404)
    session.delete(trade)
    session.commit()
    return {"ok": True}
