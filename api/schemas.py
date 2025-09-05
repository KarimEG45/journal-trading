from typing import Optional
from pydantic import BaseModel
from datetime import date, time
from uuid import UUID

class TradeCreate(BaseModel):
    num_trade: Optional[int] = None
    trade_date: Optional[date] = None
    analyse_time: Optional[time] = None
    bias_daily: Optional[str] = None
    mp_bull_low: bool = False
    mp_bull_ll: bool = False
    mp_bull_hl: bool = False
    mp_bull_high: bool = False
    mp_bear_hh: bool = False
    mp_bear_lh: bool = False
    fvg_cible: Optional[str] = None
    ob_bearish: bool = False
    ob_bullish: bool = False
    sl: Optional[float] = None
    tp: Optional[float] = None
    gains_esperes: Optional[float] = None
    pnl: Optional[float] = None
    liq_buy: bool = False
    liq_sell: bool = False
    reversal: Optional[bool] = None
    trade_stoppe: Optional[bool] = None
    shot_4h_url: Optional[str] = None
    shot_1h_url: Optional[str] = None
    shot_30m_url: Optional[str] = None
    shot_15m_url: Optional[str] = None
    rr_planned: Optional[float] = None
    rr_realized: Optional[float] = None
    setup_notes: Optional[str] = None
    emotion: Optional[str] = None
    tags: Optional[str] = None
    extras: dict = {}

class TradeRead(TradeCreate):
    id: UUID
