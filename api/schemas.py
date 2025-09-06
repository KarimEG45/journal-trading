from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import date

class AccountCreate(BaseModel):
    name: str

class AccountRead(BaseModel):
    id: UUID
    name: str

class TradeCreate(BaseModel):
    account_id: Optional[UUID] = None
    num_trade: Optional[int] = None
    trade_date: Optional[date] = None
    analyse_time: Optional[str] = None
    bias_daily: Optional[str] = None

    mp_bull_low: Optional[bool] = None
    mp_bull_ll: Optional[bool] = None
    mp_bull_hl: Optional[bool] = None
    mp_bull_high: Optional[bool] = None
    mp_bear_hh: Optional[bool] = None
    mp_bear_lh: Optional[bool] = None

    fvg_cible: Optional[str] = None
    ob_bullish: Optional[bool] = None
    ob_bearish: Optional[bool] = None

    sl: Optional[float] = None
    tp: Optional[float] = None
    gains_esperes: Optional[float] = None
    pnl: Optional[float] = None

    liq_buy: Optional[bool] = None
    liq_sell: Optional[bool] = None
    reversal: Optional[bool] = None
    trade_stoppe: Optional[bool] = None

    rr_planned: Optional[float] = None
    rr_realized: Optional[float] = None

    setup_notes: Optional[str] = None
    emotion: Optional[str] = None
    tags: Optional[str] = None
    comments: Optional[str] = None   

class TradeRead(TradeCreate):
    id: UUID
