from typing import Optional
from sqlmodel import SQLModel, Field, Column, JSON
from datetime import date, time
from uuid import uuid4, UUID

class Trade(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    # --- Excel-like fields ---
    num_trade: Optional[int] = Field(default=None, index=True)
    trade_date: Optional[date] = Field(default=None, index=True)
    analyse_time: Optional[time] = None

    bias_daily: Optional[str] = Field(default=None)  # 'bullish'|'bearish'|'neutral'

    # Market Profile
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
    pnl: Optional[float] = Field(default=None, index=True)

    liq_buy: bool = False
    liq_sell: bool = False

    reversal: Optional[bool] = None
    trade_stoppe: Optional[bool] = None

    # Screenshots URLs (local paths)
    shot_4h_url: Optional[str] = None
    shot_1h_url: Optional[str] = None
    shot_30m_url: Optional[str] = None
    shot_15m_url: Optional[str] = None

    rr_planned: Optional[float] = None
    rr_realized: Optional[float] = None
    setup_notes: Optional[str] = None
    emotion: Optional[str] = None
    tags: Optional[str] = Field(default=None, index=True)

    extras: dict = Field(default_factory=dict, sa_column=Column(JSON))
