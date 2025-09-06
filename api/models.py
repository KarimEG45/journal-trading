from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import date

class Account(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True, unique=True)
    trades: List["Trade"] = Relationship(back_populates="account")

class Trade(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    # --- Multi-comptes ---
    account_id: UUID | None = Field(default=None, foreign_key="account.id", index=True)
    account: Optional[Account] = Relationship(back_populates="trades")

    # --- Champs existants ---
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

    shot_4h_url: Optional[str] = None
    shot_1h_url: Optional[str] = None
    shot_30m_url: Optional[str] = None
    shot_15m_url: Optional[str] = None
